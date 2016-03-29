__author__ = 'hzyiting'

import httplib
import string
import json


class HttpService:
    ShortDescStarter = "{\"shortDescription\":\""
    ShortDescEnder = "\"},\"fields\":{\"shortDescription"
    LongDescStarter = "\"longDescription\":\""
    LongDescEnder = "\"},\"fields\""

    def __init__(self):
        pass

    def getRepoDesc(self, repoName):

        desc_result = {}

        httpClient = None
        try:
            httpClient = httplib.HTTPSConnection(host='hub.docker.com', timeout=200)
            httpClient.request('GET', '/r/library/' + repoName + '/')
            response = httpClient.getresponse()
            print response.status
            if response.status!=200:
                print "=====dockerhub get desc ERROR========"
                return desc_result

            value = response.read()
            shortDescStart = string.find(value, self.ShortDescStarter) + len(self.ShortDescStarter)
            shortDescEnd = string.find(value, self.ShortDescEnder)
            shortDesc = value[shortDescStart:shortDescEnd]


            desc_result["shortDesc"] = shortDesc

            longDescStart = string.find(value, self.LongDescStarter) + len(self.LongDescStarter)
            longDescEnd = string.find(value, self.LongDescEnder)
            longDesc = value[longDescStart:longDescEnd]
            longDesc = string.replace(longDesc, "\\n", "\n", -1)
            longDesc = string.replace(longDesc, "\\t", "\t", -1)
            longDesc = string.replace(longDesc, "\\u002F", "/", -1)
            longDesc = string.replace(longDesc, "\\u003E", ">", -1)
            longDesc = string.replace(longDesc, "\\u003C", "<", -1)

            desc_result["longDesc"] = longDesc
            return desc_result

        except Exception, e:
            print e
            return ""
        finally:
            if httpClient:
                httpClient.close()


    def synRepoDescHttp(self,url,username,repoName,basicDesc,detailDesc):
        httpClient = None
        try:
            index=url.index("/")
            print(index)
            hostname=url[0:index]
            requesturl=url[index:]
            httpClient = httplib.HTTPConnection(host=hostname, timeout=200)
            headers = {"Content-type": "application/json", "Accept": "text/plain"}
            object={"username":username,"repoName":repoName,"basicDesc":basicDesc,"detailDesc":detailDesc}
            jsonValue=json.dumps(object)
            httpClient.request("POST", requesturl, jsonValue, headers)
            response=httpClient.getresponse()
            print response.status
            if response.status==200:
                print "update desc sucess for :"+repoName
                print response.read()
                return True
            else:
                print "=====update desc to netease ERROR========"
                return False
        except Exception, e:
            print e
            return False
        finally:
            if httpClient:
                httpClient.close()

    def synRepoDescHttps(self,url,username,repoName,basicDesc,detailDesc):
        httpClient = None
        try:
            index=url.index("/")
            print(index)
            hostname=url[0:index]
            requesturl=url[index:]
            httpClient = httplib.HTTPSConnection(host=hostname, timeout=200)
            headers = {"Content-type": "application/json", "Accept": "text/plain"}
            object={"username":username,"repoName":repoName,"baseDesc":basicDesc,"detailDesc":detailDesc}
            jsonValue=json.dumps(object)
            httpClient.request("POST", requesturl, jsonValue, headers)
            response=httpClient.getresponse()
            print response.status

            if response.status==200:
                print "update desc sucess for :"+repoName
                print response.read()
                return True
            else:
                print "=====update desc to netease ERROR========"
                return False
        except Exception, e:
            print e
            return False
        finally:
            if httpClient:
                httpClient.close()





if __name__ == '__main__':
    service = HttpService()
    # result=service.getRepoDesc("ubuntu")
    # result=service.getRepoDesc("ubuntu")
    # print(result["shortDesc"])
    service.synRepoDescHttp("10.180.148.95:10089/api/internal/repo/desc","nce_dev","busybox","hello","helloworld")











