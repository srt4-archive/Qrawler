import urllib
from lxml import etree

class Spider:

    # seed is the set of initial input that given
    # to spider when crawling
    seed = ()

    # newly found users will be pushed into stack
    stack = ()

    def __init__(self, seed):
        self.seed = seed
        self.stack = self.seed

    def crawl(self, hasProcessed):
        while len(self.stack) != 0:

            # get username from stack
            currName = self.stack[-1]

            # parse html page to element tree
            content = etree.HTML(self.getContent(currName))

            # first check if current user has followers
            # if yes, then there will be "div" tags with
            # class attribute whose value is "pagedList_item"
            # if there is no such div tags, pass current user
            pagedList_item = self.parseContent(content, '//div[@class="pagedList_item"]')
            if len(pagedList_item) == 0:
                pass

            # get userList of current user
            userList = self.parseContent(content, '//a[@class="user"]/@href')

            # push all users fetched from current user into stack
            for name in userList:

                # first check if this user has been processed before
                # if not, process this user
                if not hasProcessed(name):
                    # push name into stack
                    self.stack.append(name)


    # param is the parameter that's used to compose the url
    def parseUrl(self, param):
        return "http://www.quora.com" + param + "/followers"

    # parse content with given xpath
    def parseContent(self, content, xpath):
        return content.xpath(xpath)

    def getContent(self, param):

        # this url points to the followers page of given user
        url = self.parseUrl(param)

        # encode url with utf-8 since some usernames contain
        # characters that are not in ascii table
        url = url.encode('utf-8')

        # get webpage of given url
        page = urllib.urlopen(url)

        # return the content of given page
        return page.read()
