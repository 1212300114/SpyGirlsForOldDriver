import urllib2
from bs4 import BeautifulSoup


class HtmlReader:
    def __init__(self, html):
        self.__html = html
        self.__soup = BeautifulSoup(html, 'html.parser')

    def readImgs(self):
        return self.__soup.findAll('img')

    def readLinks(self):
        return self.__soup.findAll('a')

    def prettify(self):
        return self.__soup.prettify()

    def getSoup(self):
        return  self.__soup

if __name__ == '__main__':
    response = urllib2.urlopen("http://tu.duowan.com/scroll/132376.html")

    reader = HtmlReader(response.read())

    imgs = reader.readImgs()

    print imgs

    links = reader.readLinks()

    for link in links:
        for string in link.strings:
            print string.encode('utf-8')


