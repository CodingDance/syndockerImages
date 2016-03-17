from docker_client import DockerClient
from git_cmd import GitClient

#import configparser
from configobj import ConfigObj

__author__ = 'hzyiting'


def main():

    # read config file
    # cp=configparser.RawConfigParser()
    # cp.read("config.conf")
    #
    # #read docker config
    # docker_repo=cp.get("docker","docker_repo")
    # docker_username=cp.get("docker","docker_username")
    # docker_password=cp.get("docker","docker_password")
    # docker_email=cp.get("docker","docker_email")
    # docker_nickname=cp.get("docker","docker_nickname")
    #
    # #read git config
    # git_repo=cp.get("git","git_repo")
    # git_dir=cp.get("git","git_dir")

    config = ConfigObj("config.conf")
    docker_repo=config["docker"]["docker_repo"]
    docker_username=config["docker"]["docker_username"]
    docker_password=config["docker"]["docker_password"]
    docker_email=config["docker"]["docker_email"]
    docker_nickname=config["docker"]["docker_nickname"]
    git_repo=config["git"]["git_repo"]
    git_dir=config["git"]["git_dir"]



    #git pull the git_repo,if no repo exist,git clone the git_repo
    gitClient = GitClient()
    gitClient.pullRepo(git_repo, git_dir)

    #read docker repo version map from the git_pro file
    dockerRepoVersionMaps = gitClient.getDockerRepoVersion(git_dir+"/library")

    #docker client
    dockerClient = DockerClient()
    dockerClient.startDockerService()
    for key in dockerRepoVersionMaps.keys():
        versions = dockerRepoVersionMaps[key]
        for version in versions:
            if dockerClient.pullDockerRepo(key, version):
                dockerClient.tagDockerRepo(key, version,  docker_repo,docker_nickname)
            else:
                print("docker pull repo failed: " + key + ":" + version)

    imageList = dockerClient.getDockerImages(docker_repo)
    if len(imageList) > 0:
        if dockerClient.loginDocker(docker_username, docker_password, docker_email, docker_repo):
            for image in imageList:
                dockerClient.pushDockerRepo(image)
        else:
            print("login error")


print("update success")

if __name__ == '__main__':
    main()