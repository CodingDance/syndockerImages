__author__ = 'hzyiting'
from configobj import ConfigObj
from docker_client import DockerClient


def main():
    config = ConfigObj("config.conf")
    docker_registry=config["docker"]["docker_registry"]
    docker_username=config["docker"]["docker_username"]
    docker_password=config["docker"]["docker_password"]
    docker_email=config["docker"]["docker_email"]
    docker_nickname=config["docker"]["docker_nickname"]
    docker_dest_registry=config["docker"]["docker_dest_registry"]

    dockerClient =DockerClient()
    dockerClient.loginDocker(docker_username,docker_password,docker_email,docker_registry)















if __name__ == '__main__':
    main()
