import Smartfridge as sf
import serial
import time
from time import gmtime, strftime
#from SimpleCV import Camera

def clearNL(data):
	return data[0:len(data)-1]

#ser = serial.Serial('/dev/ttyACM0', 9600)
ser = serial.Serial('/dev/ttyACM0', 9600)

#cam = Camera()
time.sleep(2)
ser.write("9")
allWeight = float(ser.readline())

print allWeight

while True:

	uid = clearNL(ser.readline())
	weight = float(ser.readline())
	print weight
	productWeight = weight - allWeight
	allWeight = weight

#	try:
#		if uid:
#			sf.getName(uid)
#			sf.newTransaction(NULL, uid)
#	except:
#		sf.addProduct(uid, uid, productWeight)

	if sf.checkProductExists(uid) == 1:
		sf.newTransaction('/home/pi/Desktop/Fridge.jpg', uid)
		sf.updateWeight(uid, productWeight)
	else:
		sf.addProduct(uid, uid, productWeight)