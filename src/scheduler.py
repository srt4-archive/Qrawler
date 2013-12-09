from spider import Spider
import time
import sqlite3


class Scheduler:

	# userList acts as a seed to spider
	userList = ()

	# processedDict contains all users that
	# have been processed
	userDict = {}

	#tempList is the list that contain most recent names that
	# are crawled by spider
	tempList = []

	# tempListCount represent the number of users
	# that have been crawled
	tempListCount = 0

	def __init__(self, inputfile):

		# open given file and read from it
		self.userList = [line.strip() for line in open(inputfile)]
		self.preTime = time.time()
		self.storeUnit = 10000

	# return true if given username has been processed, otherwise
	# add it to the userDict and return false
	def hasProcessed(self, username):
		if username in self.userDict:
			return True

		self.userDict[username] = '1'
		self.tempList.append(username)
		self.tempListCount += 1
		if self.tempListCount > self.storeUnit:
			self.storeData()
		return False

	def startCrawl(self):
		spider = Spider(self.userList)
		spider.crawl(self.hasProcessed)

	def storeData(self):

		#timeDiff is time(measured in minutes) that used to crawl 10000
		timeDiff = (time.time() - self.preTime) / 60
		self.preTime = time.time()

		# filename will be in format like "Thu,28,2013-06:50:07=2.56"
		# where 2.56 is the first 4 digits of timeDiff
		filename = time.strftime("%a, %d, %b, %Y-%H:%M:%S", time.gtime(), + "=" + str(timeDiff)[:4])

		# write data into test file, one username per line
		f = open(filename + '.txt' + 'w')
		f.write('\n'.join(self.tempList))
		f.close()

		# reset tempList to empty and set count to 0
		self.tempList = []
		self.tempListCount = 0

