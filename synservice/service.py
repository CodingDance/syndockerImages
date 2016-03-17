from docker_client import DockerClient
from git_cmd import GitClient
import configparser

__author__ = 'hzyiting'


def main():
    # read config file
    cp=configparser.RawConfigParser()
    cp.read("config.conf")
    docker_repo=cp.get("docker","docker_repo")
    docker_username=cp.get("docker","docker_username")
    docker_password=cp.get("docker","docker_password")
    docker_email=cp.get("docker","docker_email")
    docker_nickname=cp.get("docker","docker_nickname")


    gitClient = GitClient()
    gitClient.pullRepo("https://github.com/yiting1122/official-images.git", "official-images")
    dockerRepoVersionMaps = gitClient.getDockerRepoVersion("official-images/library")

    # nickname = "nce_dev"
    # url = "localhost:5000"

    dockerClient = DockerClient()

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