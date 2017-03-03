# coding=utf-8
import urllib2
import urllib
import json
import os
import sys
import mySqlOrm
import soup_seek
import requests
import imghdr
import string
from time import ctime


class spy:
    def __init__(self, imgFolder):
        self._offset = 0
        self._page = 1
        self._endPage = 30
        self._imgFolder = imgFolder
        self._targetPath = ''
        self._fileIndex = 1
        self.createFolder()

    def scanPage(self):

        params = {'offset': self._offset, 'order': 'created', 'math': 1}
        response = urllib2.urlopen('http://tu.duowan.com/m/meinv', urllib.urlencode(params))

        result = response.read()
        obj = json.loads(result)
        reader = soup_seek.HtmlReader(obj['html'])
        imgs = reader.readImgs()
        self.downloadImage(imgs, None)
        print 'scan for offset ', self._offset
        print 'current scan end '

    def downloadImage(self, imgs, folder):

        for img in imgs:
            url = img['src']
            items = string.split(url, '/')
            if folder:
                folderPath = os.path.join(self._targetPath, folder)
                if not os.path.exists(folderPath):
                    os.mkdir(folderPath)
                fileName = os.path.join(self._targetPath, folder, items[-1])
            else:
                fileName = os.path.join(self._targetPath, items[-1])
            if os.path.exists(fileName):
                print fileName, 'already exists'
                continue
            response = requests.get(url)
            content = response.content
            imgType = imghdr.what('', h=content)
            if imgType:
                with open(fileName, 'wb') as f:
                    f.write(content)
                    print 'finish download'
                    self._fileIndex += 1
                    parentUrl = img.parent['href']
                    parentUrl = parentUrl.replace('gallery', 'scroll')
                    mySqlOrm.insertImage(items[-1], ctime(),
                                         response.headers['Date'], parentUrl, url)
            else:
                print 'error file type'

    def getAllList(self):
        for i in range(0, self._endPage):
            self.scanPage()
            self._offset += 30

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
        # read img info from my sql
        self._imageInfos = mySqlOrm.queryImage()
        for item in self._imageInfos:
            print item.file_name

    def scanDetailPage(self):
        if self._imageInfos:
            for item in self._imageInfos:
                print item.main_site_url
                response = requests.get(item.main_site_url)
                content = response.content
                reader = soup_seek.HtmlReader(content)
                print reader.getSoup().head.title.string
                imgs = reader.readImgs()
                self.downloadImage(imgs, reader.getSoup().head.title.string)


if __name__ == '__main__':
    s = spy('beauty')
    s.getAllList()
    s.readImgInfo()
    s.scanDetailPage()
    mySqlOrm.closeSession()
