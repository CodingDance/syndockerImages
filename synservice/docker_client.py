__author__ = 'hzyiting'

import os

class DockerClient:



    def __init__(self):
        pass


    def pullDockerRepo(self,reponame,version):
        success=os.system("docker pull "+reponame+":"+version)
        if success==0:
            return True
        return False


    def loginDocker(self,username,password,email,url):
        success=os.system("docker login -u "+username+" -p "+password+" -e "+email+" " +url)
        if success==0:
            return True
        return False

    def tagDockerRepo(self,reponame,version,url,nickname):
        success=os.system("docker tag "+reponame+":"+version+" "+url+"/"+nickname+"/"+reponame+":"+version)
        if success==0:
            return True
        return False

    def pushDockerRepo(self,imageUrl):
        success=os.system("docker push "+imageUrl)
        if success==0:
            return True
        return False

    def getDockerImages(self,url):
        value=os.popen("docker images")
        """跳过第一行的表头信息"""
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



