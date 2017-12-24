import random
import threading
import time

class EngineSim(object):

	def __init__(self):
		self.ot = 0.0
		self.cht = 0.0
		self.op = 0.0
		self.running = False
		self.sleepTime = 0.5 # Update values every 1/2 second
		return

	def updateEngineState(self,runTime,sleepTime):
		""" Thread that simulates a few engine stats"""
		updates = 0
		maxUpdates = int(runTime / sleepTime)
		self.running = True
		while updates < maxUpdates and self.running == True:
			self.simOilTemp()	
			self.simOilPressure()
			self.simCht()
			time.sleep(sleepTime)
			updates += 1
			#print("%d %f %f %f " %(updates,self.ot,self.op,self.cht))
		#print("Engine stopped")

	def rand(self,minr,maxr):
		""" Generate a random number between minr,maxr"""
		diff = maxr - minr
		r = random.random() * diff
		return minr + r

	def newVal(self,lastVal,r,bias):
		""" Generate a new random number centered around lastVal
		of range 'r' and bias 'bias'"""
		mn = (lastVal - r ) + bias
		mx = (lastVal + r ) + bias
		return self.rand(mn,mx)

	def simOilTemp(self):
		# Begin with 60 F
		if self.ot == 0.0:
			ot = 60
		else:
			# We have reached a max temp, hover there
			if self.ot > 240:
				ot = self.newVal(self.ot,5,0)
			else:
				if self.ot < 180:
					# Engine is still warming up
					ot = self.ot + 5
				else:
					# Operating temp
					ot = self.newVal(self.ot,3,0.25)

		self.ot = ot
		return ot
	
	def simCht(self):
		if self.cht == 0.0:
			cht = 100
		else:
			if self.cht < 250.0:
				cht = self.newVal(self.cht,5,10)
			else:
				if self.cht > 350.0:
					cht = self.newVal(self.cht,1,-0.5)
				else:
					cht = self.newVal(self.cht,5,0.25)

		self.cht = cht
		return cht
	def simOilPressure(self):
		if self.op == 0.0:
			op = 60.0
		else:
			if self.op < 5.0:
			    	op = self.newVal(self.op,0.5,0.0)
			else:
				if self.op < 10.0:
				    op = self.newVal(self.op,1,0.01)
				else:
				    op = self.newVal(self.op,2,-1)
			    
		self.op = op
		
	def stop(self):
		self.running = False
	def start(self):
		self.runTime = self.rand(5*60,90*60)
		self.runThread = threading.Thread(None,self.updateEngineState, "engineState",(self.runTime,self.sleepTime))
		self.runThread.start()
		self.running = True
		#print('ready')


es = EngineSim()
es.start()

while True:
	try:
		time.sleep(1)
	except:
		es.stop()
		break


exit(0)
