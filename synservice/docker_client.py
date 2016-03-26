__author__ = 'hzyiting'

import os

class DockerClient:



    def __init__(self):
        pass

    def startDockerService(self):
        success=os.system("service docker start")
        if success==0:
            return True
        return False

    def pullDockerRepo(self,reponame,version):
        success=os.system("docker pull "+reponame+":"+version)
        if success==0:
            return True
        return False

    # make sure you install the daocloud's speed service
    def pullDockerRepoFromDaoCloud(self,reponame,version):
        success=os.system("dao pull "+reponame+":"+version)
        if success==0:
            return True
        return False


    def loginDocker(self,username,password,email,url):
        success=os.system("docker login -u "+username+" -p "+password+" -e "+email+" " +url)
        if success==0:
            return True
        return False

    def tagDockerRepo(self,reponame,version,url,nickname):
        repoUrl = url + "/" + nickname + "/" + reponame + ":" + version
        success = os.system("docker tag " + reponame + ":" + version + " " + repoUrl)
        # if success==0:
        #     return repoUrl
        return repoUrl

    def pushDockerRepo(self,imageUrl):
        success=os.system("docker push "+imageUrl)
        if success==0:
            return True
        return False

    #get docker images and version like :  ubuntu:12.04
    def getDockerImages(self,url):
        value=os.popen("docker images")
        #skip first line
        value.readline();
        lines=value.readlines();
        imageList=[]
        for line in lines:
            line = line.strip()
            if (len(line) == 0):
                    continue
            imageInfo=line.split()
            if(imageInfo[0].startswith(url)):
                repoUrl=imageInfo[0]+":"+imageInfo[1]
                imageList.append(repoUrl)
            else:
                pass
        return imageList

    # get all images Ids
    def getDockerImageIds(self):
        value=os.popen("docker images")
        #skip first line
        value.readline();
        lines=value.readlines();
        imageIdsList=[]
        for line in lines:
            line = line.strip()
            if (len(line) == 0):
                    continue
            imageInfo=line.split()
            imageId=imageInfo[2]
            print(imageId)
            imageIdsList.append(imageId)
        return set(imageIdsList)  # use set to delete some same imageids


    #rmi docker images by Id
    def rmiDockerImage(self,imageId):
        success=os.system("docker rmi -f "+imageId)
        if success==0:
            return True
        return False




