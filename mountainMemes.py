import os
import cv2
import picode
import madmom
import librosa 
from PIL import Image
from pathlib import Path

def fetchFileList(directory):
    fileList = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ending) for ending in ['.kt', '.gradle']):
                filePath = os.path.abspath(os.path.join(root, file))
                fileLength = sum(1 for line in open(filePath, encoding='utf8'))
                fileList.append({'Path': filePath, 'Name': file, 'Length': fileLength})
    return fileList
    
def prepOutput(folder):
    output = Path(folder)
    
    if output.exists():
        for item in output.iterdir():
            item.unlink()
        output.rmdir()
    output.mkdir()

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
    
def getBeatTimes(file):
    proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
    act = madmom.features.beats.RNNBeatProcessor()(file)
    
    return proc(act)

def prepFrame(image, width=3840, height=2160):
    base = Image.open(image)
    imWidth, imHeight = base.size
    
    res = base
    
    #This code checks if the image is too tall for the frame, if it is then
    #The image is split into columns to get it closer to the correct aspect ratio
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
        
    final = Image.new("RGB", (width, height))
    
    
    return res
    
def getImages(directory):
    return [directory + child for child in os.listdir(directory)]
    
def buildVideo(fileName, length, beats, images, fps=30):
    print('memes')

def main():   
    codeDirectory = '../SnakeSkin/'
    imageDirectory = './MountainImages/'
    musicFile = 'mountain.wav'
    
    #createImages(codeDirectory, imageDirectory)
    
    #mmBeats = getBeatTimes(musicFile)
    #print("Madmom found", len(mmBeats), "beats.") #289 beats
    #mmClicks = librosa.clicks(mmBeats, sr=sampleRate, length=len(baseAudio))
    #librosa.output.write_wav('madmomMountain.wav', baseAudio + mmClicks, sampleRate)
    
if __name__ == '__main__':
    main()
