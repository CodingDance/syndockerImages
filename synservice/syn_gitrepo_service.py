from docker_client import DockerClient
from git_cmd import GitClient
import os

#import configparser
from configobj import ConfigObj
from http_service import HttpService


__author__ = 'hzyiting'


def main():

    # read config file
    # cp=configparser.RawConfigParser()
    # cp.read("config.conf")
    #
    # #read docker config
    # docker_registry=cp.get("docker","docker_registry")
    # docker_username=cp.get("docker","docker_username")
    # docker_password=cp.get("docker","docker_password")
    # docker_email=cp.get("docker","docker_email")
    # docker_nickname=cp.get("docker","docker_nickname")
    #
    # #read git config
    # git_repo=cp.get("git","git_repo")
    # git_dir=cp.get("git","git_dir")

    config = ConfigObj("config.conf")
    docker_registry=config["docker"]["docker_registry"]
    docker_username=config["docker"]["docker_username"]
    docker_password=config["docker"]["docker_password"]
    docker_email=config["docker"]["docker_email"]
    docker_nickname=config["docker"]["docker_nickname"]

    git_repo=config["git"]["git_repo"]
    git_dir=config["git"]["git_dir"]

    netease_info=config["info"]["netease_info"]
    netease_test=config["info"]["netease_test"]
    netease_liantiao=config["info"]["netease_liantiao"]

    #git pull the git_repo,if no repo exist,git clone the git_repo
    gitClient = GitClient()
    gitClient.pullRepo(git_repo, git_dir)

    #read docker repo version map from the git_pro file
    dockerRepoVersionMaps = gitClient.getDockerRepoVersion(git_dir+"/library")


    imageFile=open('image.txt')
    imageNames={}
    for imageName in imageFile.readlines():
        imageName = imageName.strip()
        imageNames[imageName]=imageName


    #docker client
    dockerClient = DockerClient()

    # start docker service
    dockerClient.startDockerService()

    # login docker
    if dockerClient.loginDocker(docker_username, docker_password, docker_email, docker_registry) is not True:
        print("login error")
        exit(1)

    for key in dockerRepoVersionMaps.keys() :
        if imageNames.has_key(key)==False:
            print key +"is not exist in image.txt file"
            continue
        versions = dockerRepoVersionMaps[key]
        for version in versions:
            #pull image from offcial
            #if dockerClient.pullDockerRepo(key, version):

            #pull image from daocloud,be sure you install the dao cmd from daocloud
            if dockerClient.pullDockerRepoFromDaoCloud(key,version):
                imageUrl = dockerClient.tagDockerRepo(key, version, docker_registry, docker_nickname)
                print "imagesURL========"+imageUrl
                if imageUrl != "":
                    dockerClient.pushDockerRepo(imageUrl)
            else:
                print("docker pull repo failed: " + key + ":" + version)

                # imageList = dockerClient.getDockerImages(docker_registry)
                # if len(imageList) > 0:
                # if dockerClient.loginDocker(docker_username, docker_password, docker_email, docker_registry):
                # for image in imageList:
                # dockerClient.pushDockerRepo(image)
                #     else:
                #         print("login error")
        # service=HttpService()
        # desc_result=service.getRepoDesc(key)
        #
        # shortdesc=""
        # if desc_result.has_key("shortDesc"):
        #     shortdesc=desc_result["shortDesc"]
        # print("shortdesc:"+shortdesc)
        #
        # longdesc=""
        # if desc_result.has_key("longDesc"):
        #     longdesc=desc_result["longDesc"]
        # print("longdesc:"+longdesc)
        #
        # # service.synRepoDescHttp(netease_test,"library",key,shortdesc,longdesc)
        # service.synRepoDescHttp(netease_liantiao,"library",key,shortdesc,longdesc)


print("update success")

if __name__ == '__main__':
    main()