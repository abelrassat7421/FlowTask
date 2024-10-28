# Added by MP to sync with EEG amplifiers (november 2023)

from psychopy import core, parallel

class LptPort:

	def __init__(self, lptPortAddress):
		self.address = lptPortAddress
		self.port = parallel.ParallelPort(address=lptPortAddress)
		self.port.setData(0)
		self.sleepTimeBeforeReset = 0.004

	def sendEvent(self, eventNumber):
		self.port.setData(eventNumber)
		core.wait(self.sleepTimeBeforeReset)
		self.port.setData(0)
