from pathlib import Path
from git import Repo   

def main():
    tbaGitUrl = 'https://github.com/the-blue-alliance/the-blue-alliance-data.git'
    tbaPath = '../tba/'
    tbaDir = Path(tbaPath)

    if not tbaDir.exists():
        tbaDir.mkdir()
    
    dotGitExists = Path(tbaPath + '.git/').exists()

    if dotGitExists:
        repo = Repo('../tba/')
        isBehind = (sum(1 for c in repo.iter_commits('master..origin/master')) > 0)
        
        if isBehind:
            repo.git.pull()
    
    if not dotGitExists:
        repo.clone_from(tbaGitUrl, tbaPath)
    else:
        print('Up to date!')
    
if __name__ == '__main__':
    main()