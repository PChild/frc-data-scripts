import os
import cv2
import numpy
import picode
import madmom
import librosa
import subprocess
import pandas as pd
from git import Repo
from PIL import Image
from tqdm import tqdm
from mutagen.mp4 import MP4
from cv2 import VideoWriter, VideoWriter_fourcc

def updateRepoData(repoData, file=None):
    if file is None:
        file = 'mountainSettings.csv'
    pd.DataFrame([repoData], columns=['Repo']).to_csv(file, index=False)
    
def getRepoPath(file=None):
    if file is None:
        file = 'mountainSettings.csv'
        
    defaultRepoLocation = '../SnakeSkin/'
    if not os.path.isfile(file):
        updateRepoData(defaultRepoLocation, file)

    return pd.read_csv(file)['Repo'].values[0]     

def gitIsBehind(repoPath):
    repo = Repo(repoPath) 
    return (sum(1 for c in repo.iter_commits('master..origin/master')) > 0)

def updateGit(repoPath):
    if gitIsBehind(repoPath):
        repo = Repo(repoPath)
        repo.git.pull()
        print('Updated git repo.')
    else:
        print('Repo is up to date.')

def handleRepo(url='https://github.com/team401/SnakeSkin.git'):
    repoPath = getRepoPath()
    if not os.path.isdir(repoPath):
        os.mkdir(repoPath)
    
    dotGitExists = os.path.isdir(repoPath + '.git/')    
    if dotGitExists:        
        updateGit(repoPath)    
    if not dotGitExists:
        Repo.clone_from(url, repoPath)

def fetchCodeFileData(directory):
    fileList = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ending) for ending in ['.kt', '.gradle']):
                filePath = os.path.abspath(os.path.join(root, file))
                fileLength = sum(1 for line in open(filePath, encoding='utf8'))
                fileList.append({'Path': filePath, 'Name': file, 'Length': fileLength})
    return fileList

def updateImages(force=False):
    repoPath = getRepoPath()
    wasBehind = gitIsBehind(repoPath)
    updateGit(repoPath)
    
    if wasBehind or force:
        createImages()
        print('Updated base images.')
        createFrames()
        print('Updated frmaes.')
        
def getImageFiles(directory):
    return [directory + child for child in os.listdir(directory)]

def wipeImages(folder='./baseImages/'):
    if os.path.isdir(folder):
        for item in os.listdir(folder):
            os.remove(folder + item)
        os.rmdir(folder)
    
def prepOutput(folder):
    wipeImages(folder)    
    os.mkdir(folder)

def readCode(file):
    fileContents = ""
    with open(file, encoding='utf8') as file:
        fileContents = file.read()
    return fileContents

def createImages(codeDirectory='../SnakeSkin/', imageDirectory='./baseImages/'):    
    prepOutput(imageDirectory)
    
    fileList = fetchCodeFileData(codeDirectory)
    for file in fileList:
        try:
            fileImage = picode.to_pic(file_path=file['Path'], language='kotlin', margin=0, line_numbers_padding=20, font_size=24, show_line_numbers=True)
        except:
            fileCode = readCode(file['Path'])
            fileImage = picode.to_pic(code=fileCode, language='kotlin', margin=0, line_numbers_padding=20, font_size=24, show_line_numbers=True)
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

def createFrames(inputFolder='./baseImages/', outputFolder='./videoFrames/'):
    prepOutput(outputFolder)
    
    for idx, file in enumerate(getImageFiles(inputFolder)):
        prepFrame(file).save(outputFolder + str("1%03d" % idx)+'.png')

def getFrames(frameFolder):
    return [Image.open(file) for file in getImageFiles(frameFolder)]

def getBeatTimes(file, fps=100):
    proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=fps)
    act = madmom.features.beats.RNNBeatProcessor()(file)
    
    return proc(act)

def testMusic(musicFile, fps):
    baseAudio, sampleRate = librosa.load(musicFile)
    mmBeats = getBeatTimes(musicFile, fps)
    print("Madmom found", len(mmBeats), "beats.") 
    mmClicks = librosa.clicks(mmBeats, sr=sampleRate, length=len(baseAudio))
    librosa.output.write_wav('BEAT_TEST_' + musicFile, baseAudio + mmClicks, sampleRate)

def buildVideo(outFile, musicFile, framesFolder='./videoFrames/', fps=60):    
    codec = VideoWriter_fourcc(*'MP4V')
    frames = getFrames(framesFolder)
    print("Image frames:", str(len(frames)))
    beats = getBeatTimes(musicFile)
    print("Audio beats:", str(len(beats)))
    baseAudio, sampleRate = librosa.load(musicFile)
    duration = librosa.core.get_duration(baseAudio)
    print("Audio duration:", str(round(duration)), "seconds")
    
    if os.path.isfile(outFile):
        os.remove(outFile)
    
    if len(frames) > len(beats):
        print("Too many images for sound file!")
    else:
        firstFrame = cv2.cvtColor(numpy.array(frames[0]), cv2.COLOR_RGB2BGR)
        size = firstFrame.shape[1], firstFrame.shape[0]
        print("Video:", str(firstFrame.shape[1])+"x"+str(firstFrame.shape[0]), '@', fps, 'FPS')
        
        vidFile = 'VIDEO_' + outFile
        vid = VideoWriter(vidFile, codec, fps, size)
        
        timePerFrame = 1 / fps
        currentTime = 0
        
        #beatsDiffSplit = int((len(beats) - len(frames)) / 2)
        beatsDiffSplit = 0
        
        print('Processing video frames:')
        for idx, frame in enumerate(tqdm(frames)):
            transitionTime = beats[idx + beatsDiffSplit]
            image = cv2.cvtColor(numpy.array(frame), cv2.COLOR_RGB2BGR)
            
            if idx + 1 == len(frames):
                transitionTime = duration
            
            while currentTime < transitionTime:
                vid.write(image)
                currentTime += timePerFrame
        vid.release()
        print('Muxing video.')
        muxVideo(musicFile, vidFile, outFile)
        print('Updating video metadata.')
        
        props = {'©ART': 'Copperhead Robotics',
                 '©day': '2018',
                 '©gen': 'Techno',
                 '©cmt': 'Code at github.com/team401',
                 '©alb': '2018 Offseason Code',
                 '©wrt': 'FRC Team 401',
                 '©nam': 'Code Release'}
        
        metaData = MP4(outFile)
        for prop in props:
            metaData[prop] = props[prop]
        metaData.save()
        
        print('Saved video:', outFile)
        os.remove(vidFile)

def muxVideo(audioFile, videoFile, outFile):
    cmd = 'ffmpeg -i ' + audioFile + ' -i ' + videoFile + ' -c:v copy -c:a aac -strict experimental ' + outFile
    subprocess.call(cmd, shell=True)

def main():   
    musicFile = 'MountainBase.wav'
    
    updateImages(False)
    buildVideo('MountainMeme.mp4', musicFile)

if __name__ == '__main__':
    main()
