__author__ = 'hzyiting'

import os


class GitClient:
    filelist = ()


    def __init__(self):
        """
        :return:
        """


    def cloneRepo(self, gitpath):
        os.system('git clone ' + gitpath)

    def pullRepo(self, gitpath, filename):
        pwd = os.getcwd()
        print(pwd)
        if os.path.exists(filename) == False:
            self.cloneRepo(gitpath)
        else:
            os.chdir(filename)
            os.system('git pull')
        os.chdir(pwd)


    def getUpdateRepoFileList(self, filename):
        pwd = os.getcwd()
        print(pwd)
        updateRepoFileList = []
        if os.path.exists(filename) == True:
            os.chdir(filename)
            value = os.popen("git diff --name-status HEAD~1 HEAD~2")
            value.readline()
            lines = value.readlines()
            for line in lines:
                temp = line.rpartition("/")
                updateRepoFileList.append(temp[3])
        os.chdir(pwd)
        return updateRepoFileList;


    def getDockerRepoList(self, directory):
        self.filelist = os.listdir(directory)


    def getDockerRepoVersion(self, directory):
        self.getDockerRepoList(directory)

        dockerRepoVersionMaps = {}
        for fileName in self.filelist:
            fp = open(directory + '/' + fileName, "r")
            versions = []
            for line in fp:
                line = line.strip()
                if (len(line) == 0):
                    continue
                if line.startswith("#"):
                    continue
                info = line.split(':')
                version = info[0]
                versions.append(version)
                dockerRepoVersionMaps[fileName] = versions
        return dockerRepoVersionMaps;






