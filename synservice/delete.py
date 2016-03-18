from docker_client import DockerClient

__author__ = 'hzyiting'



def main():
    dockerClient = DockerClient()
    dockerClient.startDockerService()
    dockerIdsList=dockerClient.getDockerImageIds()
    for imageId in dockerIdsList:
        print("imageId: "+imageId)
        dockerClient.rmiDockerImage(imageId)
    print("rmi all images")





if __name__ == '__main__':
    main()