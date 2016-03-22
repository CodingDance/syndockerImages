__author__ = 'hzyiting'

import httplib
import string

class HttpService:


    ShortDescStarter = "{\"shortDescription\":\""
    ShortDescEnder   = "\"},\"fields\":{\"shortDescription"
    LongDescStarter = "\"longDescription\":\""
    LongDescEnder   = "\"},\"fields\""

    def __init__(self):
        pass

    def getRepoDesc(self,repoName):
        httpClient = None
        try:
            httpClient = httplib.HTTPSConnection(host='hub.docker.com',timeout=30)
            httpClient.request('GET', '/r/library/' + repoName + '/')
            response = httpClient.getresponse()
            print response.status
            print response.reason
            value= response.read()
            shortDescStart=string.find(value,self.ShortDescStarter)+len(self.ShortDescEnder)
            shortDescEnd=string.find(value,self.ShortDescEnder)
            shortDesc=value[shortDescStart:shortDescEnd]
            print(shortDesc)

            longDescStart=string.find(value,self.LongDescStarter)+len(self.LongDescEnder)
            longDescEnd=string.find(value,self.LongDescEnder)
            longDesc=value[longDescStart:longDescEnd]
            longDesc=string.replace(longDesc, "\\n", "\n", -1)
            longDesc = string.replace(longDesc, "\\t", "\t", -1)
            longDesc = string.replace(longDesc, "\\u002F", "/", -1)
            longDesc = string.replace(longDesc, "\\u003E", ">", -1)
            longDesc = string.replace(longDesc, "\\u003C", "<", -1)
            print(longDesc)

        except Exception, e:
            print e
        finally:
            if httpClient:
                httpClient.close()



if __name__ == '__main__':
    service=HttpService()
    service.getRepoDesc("ubuntu")











