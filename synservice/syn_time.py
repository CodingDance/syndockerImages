from docker_client import DockerClient
from git_cmd import GitClient

# import configparser
from configobj import ConfigObj
from http_service import HttpService
import time


__author__ = 'hzyiting'


def main():
    logFile=open('log.txt','w+')
    logFile.write("======starting=======:")
    logFile.write(time.strftime("%Y-%m-%d %X", time.localtime()))
    logFile.write("\n")
    logFile.flush()
    config = ConfigObj("config.conf")
    docker_registry = config["docker"]["docker_registry"]
    docker_username = config["docker"]["docker_username"]
    docker_password = config["docker"]["docker_password"]
    docker_email = config["docker"]["docker_email"]
    docker_nickname = config["docker"]["docker_nickname"]

    git_repo = config["git"]["git_repo"]
    git_dir = config["git"]["git_dir"]

    netease_info = config["info"]["netease_info"]
    netease_test = config["info"]["netease_test"]
    netease_liantiao = config["info"]["netease_liantiao"]

    # git pull the git_repo,if no repo exist,git clone the git_repo
    gitClient = GitClient()
    gitClient.pullRepo(git_repo, git_dir)

    #read docker repo version map from the git_pro file
    dockerRepoVersionMaps = gitClient.getDockerRepoVersion(git_dir + "/library")
    needToUpdateRepoFlieList = gitClient.getUpdateRepoFileList(git_dir)

    imageFile = open('image_desc.txt')
    imageNames = {}
    for imageName in imageFile.readlines():
        imageName = imageName.strip()
        imageNames[imageName] = imageName


    # #docker client
    dockerClient = DockerClient()
    #
    # # start docker service
    dockerClient.startDockerService()
    #
    # # login docker
    if dockerClient.loginDocker(docker_username, docker_password, docker_email, docker_registry) is not True:
        print("login error")
        exit(1)

    print "yeah!"
    for updateRepoName in needToUpdateRepoFlieList:
        print("update:" + updateRepoName)
        if imageNames.has_key(updateRepoName) == True:
            print updateRepoName + "is  exist in image_desc file,no need to update"
            continue

        versions = dockerRepoVersionMaps[updateRepoName]
        if "latest" in versions:
            index = versions.index("latest")
            print index
            if index < len(versions) / 2:
                versions.reverse()
        for version in versions:
            if dockerClient.pullDockerRepo(updateRepoName, version):
                imageUrl = dockerClient.tagDockerRepo(updateRepoName, version, docker_registry, docker_nickname)
                print "imagesURL========" + imageUrl
                if imageUrl != "":
                    dockerClient.pushDockerRepo(imageUrl)
            else:
                print("docker pull repo failed: " + updateRepoName + ":" + version)

        service = HttpService()
        desc_result = service.getRepoDesc(updateRepoName)

        shortdesc = ""
        if desc_result.has_key("shortDesc"):
            shortdesc = desc_result["shortDesc"]
        print("shortdesc:" + shortdesc)

        longdesc = ""
        if desc_result.has_key("longDesc"):
            longdesc = desc_result["longDesc"]
        print("longdesc:" + longdesc)

        # service.synRepoDescHttp(netease_test,"library",key,shortdesc,longdesc)
        service.synRepoDescHttps(netease_info, "library", updateRepoName, shortdesc, longdesc)
        logFile.write("======update success=======:")
        logFile.write(time.strftime("%Y-%m-%d %X", time.localtime()))
        logFile.write("\n")
        logFile.flush()

print("update success")

if __name__ == '__main__':
    main()
