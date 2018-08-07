import os
import picode
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

def main():    
    codeDirectory = '../SnakeSkin/'
    outputDirectory = './MountainImages/'
    
    prepOutput(outputDirectory)
    
    fileList = fetchFileList(codeDirectory)
    for file in fileList:
        try:
            fileImage = picode.to_pic(file_path=file['Path'], language='kotlin', margin=0, show_line_numbers=True)
        except:
            fileCode = readCode(file['Path'])
            fileImage = picode.to_pic(code=fileCode, language='kotlin', margin=0, show_line_numbers=True)
        fileImage.save(outputDirectory + str(file['Length']) + "_" + file['Name'] + '.png')
    
if __name__ == '__main__':
    main()
