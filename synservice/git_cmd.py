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
        ret = False
        pwd = os.getcwd()
        print(pwd)
        if os.path.exists(filename) == False:
            self.cloneRepo(gitpath)
        else:
            os.chdir(filename)
            value = os.popen('git pull')
            lines = value.readlines()
            print(lines)
            for line in lines:
                if line.strip().find("Already up-to-date") != -1:
                    print("this git repo is the latest repo")
                    ret = True;

        os.chdir(pwd)
        return ret

    def getUpdateRepoFileList(self, filename):
        pwd = os.getcwd()
        print(pwd)
        print(filename)
        updateRepoFileList = []
        if os.path.exists(filename) == True:
            os.chdir(filename)
            value = os.popen("git diff --name-status HEAD~1 HEAD~10")
            lines = value.readlines()
            print(lines)
            for line in lines:
                print(line)
                if line.__contains__("library/"):
                    line = line.strip()
                    temp = line.rpartition("/")
                    updateRepoFileList.append(temp[2])
        os.chdir(pwd)
        print "over!"
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
                if line.__contains__("git://github.com")==True and line.__contains__("GitRepo")==False:
                    info = line.split(':')
                    version=info[0]
                    versions.append(version)

                if line.startswith("Tags"):
                    info =line.split(':')
                    versionArray=info[1].split(',')
                    for version in versionArray:
                        versions.append(version.strip())
                dockerRepoVersionMaps[fileName] = versions
        return dockerRepoVersionMaps;






