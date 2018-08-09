import os
import picode
import madmom
import librosa 
from PIL import Image
from cv2 import VideoWriter, VideoWriter_fourcc, imread

def fetchFileList(directory):
    fileList = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ending) for ending in ['.kt', '.gradle']):
                filePath = os.path.abspath(os.path.join(root, file))
                fileLength = sum(1 for line in open(filePath, encoding='utf8'))
                fileList.append({'Path': filePath, 'Name': file, 'Length': fileLength})
    return fileList

def getImages(directory):
    return [directory + child for child in os.listdir(directory)]
    
def prepOutput(folder):    
    if os.path.isdir(folder):
        for item in os.listdir(folder):
            os.remove(folder + item)
        os.rmdir(folder)
    os.mkdir(folder)

def readCode(file):
    fileContents = ""
    with open(file, encoding='utf8') as file:
        fileContents = file.read()
    return fileContents

def createImages(codeDirectory, imageDirectory):    
    prepOutput(imageDirectory)
    
    fileList = fetchFileList(codeDirectory)
    for file in fileList:
        try:
            fileImage = picode.to_pic(file_path=file['Path'], language='kotlin', margin=0, show_line_numbers=True)
        except:
            fileCode = readCode(file['Path'])
            fileImage = picode.to_pic(code=fileCode, language='kotlin', margin=0, show_line_numbers=True)
        fileImage.save(imageDirectory + str("%03d" % file['Length']) + "_" + file['Name'] + '.png')

def prepFrame(image, width=3840, height=2160):
    base = Image.open(image)
    imWidth, imHeight = base.size
    
    res = base
    
    #Checks if the image is too tall for the frame, if it is then split the
    #image into columns to get it closer to the correct aspect ratio
    if imHeight > height:
        desiredRatio = width / height
        
        bestRatio = imWidth / imHeight
        columns = 1
        
        for i in range(1,6):
            newWidth = imWidth * i
            newHeight = imHeight / i
            
            newRatio = newWidth / newHeight
            
            if abs(desiredRatio - newRatio) < abs(desiredRatio - bestRatio):
                bestRatio = newRatio
                columns = i
        
        newHeight = int(imHeight / columns)
        
        res = Image.new("RGB", (int(columns * imWidth) + 1, newHeight + 1), None)
        
        i = 1
        while i <= columns:
            imgSlice = base.copy().crop((0, (i - 1) * newHeight, imWidth, i * newHeight))
            res.paste(imgSlice, ((i - 1) * imWidth, 0))
            i += 1
    
    #Scales image to fit in the specified frame size while maintaining the
    #chopped image aspect ratio to make sure things aren't distorted.
    newWidth, newHeight = res.size
    if newWidth > width or newHeight > height:
        widthRatio = newWidth / width
        heightRatio = newHeight / height
        
        scaler = heightRatio
        if widthRatio > heightRatio:
            scaler = widthRatio
    
        resizeWidth = round(newWidth / scaler)
        resizeHeight = round(newHeight / scaler)
        res = res.resize((resizeWidth, resizeHeight))
    
    #Calculates offsets to center image on screen
    newWidth, newHeight = res.size    
    widthOffset = int((width - newWidth) / 2)
    heightOffset = int((height - newHeight) / 2)
    
    final = Image.new("RGB", (width, height))
    final.paste(res, (widthOffset, heightOffset))
    
    return final

def getFrames(folder):
    return [prepFrame(file) for file in getImages(folder)]
 
def getBeatTimes(file):
    proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
    act = madmom.features.beats.RNNBeatProcessor()(file)
    
    return proc(act)

def testMusic(musicFile):
    baseAudio, sampleRate = librosa.load(musicFile)
    mmBeats = getBeatTimes(musicFile)
    print("Madmom found", len(mmBeats), "beats.") 
    mmClicks = librosa.clicks(mmBeats, sr=sampleRate, length=len(baseAudio))
    librosa.output.write_wav('BEAT_TEST_' + musicFile, baseAudio + mmClicks, sampleRate)
    
def buildVideo(outFile, imageFolder, musicFile, fps=30):
    codec = VideoWriter_fourcc('MJPG')
    frames = getFrames(imageFolder)
    beats = getBeatTimes(musicFile)
    baseAudio, sampleRate = librosa.load(musicFile)
    duration = librosa.core.get_duration(baseAudio)
    
    if len(frames) > len(beats):
        print("Too many images for sound file!")
    else:
        firstFrame = imread(frames[0])
        size = firstFrame.shape[1], firstFrame.shape[0]
        vid = VideoWriter(outFile, codec, float(fps), size, is_color=True)
        
        timePerFrame = 1 / fps
        currentTime = 0
        for idx, frame in enumerate(frames):
            transitionTime = beats[idx]
            image = imread(frame)
            
            if idx + 1 == len(frames):
                transitionTime = duration
            
            while currentTime < transitionTime:
                vid.write(image)
                currentTime += timePerFrame
        vid.release()

def main():   
    codeFolder = '../SnakeSkin/'
    imageFolder = './MountainImages/'
    musicFile = 'mountain.wav'
    
    #buildVideo('MountainMeme.mjpg', imageFolder, musicFile)
    #createImages(codeFolder, imageFolder)
    

    
if __name__ == '__main__':
    main()
