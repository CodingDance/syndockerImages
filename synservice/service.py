from docker_client import DockerClient
from git_cmd import GitClient

__author__ = 'hzyiting'


def main():
    gitClient = GitClient()
    gitClient.pullRepo("https://github.com/yiting1122/official-images.git", "official-images")
    dockerRepoVersionMaps = gitClient.getDockerRepoVersion("official-images/library")

    nickname = "nce2"
    url = "localhost:5000"

    dockerClient = DockerClient()

    for key in dockerRepoVersionMaps.keys():
        versions = dockerRepoVersionMaps[key]
        for version in versions:
            if dockerClient.pullDockerRepo(key, version):
                dockerClient.tagDockerRepo(key, version, nickname, url)
            else:
                print("docker pull repo failed: " + key + ":" + version)

    imageList = dockerClient.getDockerImages(url)
    if len(imageList) > 0:
        """qaqance_dev@163.com/qa1234  qaqance_dev@163.com"""
        if dockerClient.loginDocker("qaqance_dev@163.com", "qa1234", "qaqance_dev@163.com", url):
            for image in imageList:
                dockerClient.pushDockerRepo(image)
        else:
            print("login error")


print("update success")

if __name__ == '__main__':
    main()