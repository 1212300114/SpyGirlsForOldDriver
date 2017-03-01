# coding=utf-8
import urllib2
import urllib
import json
import re
import os
import sys
import imghdr
import string

class spy:
    def __init__(self, imgFolder):
        self._offset = 0
        self._page = 1
        self._endPage = 30
        self._imgFolder = imgFolder
        self._targetPath = ''
        self._fileIndex = 1
        self.createFolder()
        self.readImgInfo()



    def scanPage(self):
        try:
            params = {'offset': self._offset, 'order': 'created', 'math': 1}
            response = urllib2.urlopen('http://tu.duowan.com/m/meinv', urllib.urlencode(params))

            result = response.read()
            obj = json.loads(result)
            # print obj['html']

            imgList = re.findall("<img.*?src=\"(.*?\.(jpg|png))\".*?/>", obj['html'])
            for imgUrl in imgList:
                print imgUrl[0]
                response = urllib2.urlopen(imgUrl[0])
                content = response.read()
                imgType = imghdr.what('', h=content)
                headers = response.headers
                # print headers
                if imgType:
                    print self._targetPath
                    items = string.split(imgUrl[0], '/')
                    print items
                    fileName = os.path.join(self._targetPath, str(self._fileIndex) + '.jpg')
                    with open(fileName, 'wb') as f:
                        f.write(content)
                        print 'finish download'
                        self._fileIndex += 1
                else:
                    print 'error file type'

        except:
            print 'error'

    def createFolder(self):
        path = sys.path[0]
        if os.path.isdir(path):
            print path
        elif os.path.isfile(path):
            path = os.path.dirname(path)
        self._targetPath = os.path.join(path, self._imgFolder)
        if not os.path.exists(self._targetPath):
            os.mkdir(self._targetPath)
        else:
            self._fileIndex = len(os.listdir(self._targetPath))

    def readImgInfo(self):
        #read img info from my sql
        pass

if __name__ == '__main__':
    s = spy('beauty')
    s.scanPage()
