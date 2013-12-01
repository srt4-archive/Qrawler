from scheduler import Scheduler

class Engine:

	def __init__(self, inputFile):
		self.scheduler = Scheduler(inputFile)

	def start(self):
		self.scheduler.startCrawl()
