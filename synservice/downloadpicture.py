from git_cmd import GitClient

__author__ = 'hzyiting'
import os
from configobj import ConfigObj

def main():
    downloadAll()


def downloadFromFile():
    imageFile=open('picture.txt')
    url="https://hub.docker.com/public/images/official/"
    dirname="pictures"
    if os.path.exists(dirname)==False:
        os.mkdir(dirname)
    os.chdir(dirname)
    for imageName in imageFile.readlines():
        imageName = imageName.strip()
        imageUrl=url+imageName+".png"
        os.system("wget "+imageUrl)

def downloadAll():
    config = ConfigObj("config.conf")
    gitClient = GitClient()
    git_dir=config["git"]["git_dir"]
    dockerRepoVersionMaps = gitClient.getDockerRepoVersion(git_dir+"/library")

    url="https://hub.docker.com/public/images/official/"
    dirname="pictures"
    if os.path.exists(dirname)==False:
        os.mkdir(dirname)
    for key in dockerRepoVersionMaps.keys():
        print key
        imageUrl=url+key+".png"
        os.system("wget "+imageUrl)



if __name__ == '__main__':
    main()