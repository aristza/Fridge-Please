import Smartfridge as sf
import RPi.GPIO as GPIO
import Adafruit_DHT
import time

servoPIN = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
pstemp = sf.getFridgeDesiredTemperature()
p = GPIO.PWM(servoPIN, 50)
p.start(0)

try:

	while True:

		temp = sf.getFridgeActualTemperature()
		stemp = sf.getFridgeDesiredTemperature()
		hum = sf.getFridgeHumidity()
	
		if stemp != pstemp:
		
			pstemp = stemp

			if stemp == 0:
				p.ChangeDutyCycle(2.5)
				time.sleep(0.2)
				p.ChangeDutyCycle(0)
			elif stemp == 1:
				p.ChangeDutyCycle(5)
				time.sleep(0.2)
				p.ChangeDutyCycle(0)
			elif stemp == 2:
				p.ChangeDutyCycle(7.5)
				time.sleep(0.2)
				p.ChangeDutyCycle(0)
			elif stemp == 3:
				p.ChangeDutyCycle(10)
				time.sleep(0.2)
				p.ChangeDutyCycle(0)
			elif stemp == 4:
				p.ChangeDutyCycle(12.5)
				time.sleep(0.2)
				p.ChangeDutyCycle(0)
		
		huma, tempa = Adafruit_DHT.read_retry(11, 4)

		if temp != tempa:
			sf.setFridgeActualTemperature(float(tempa))
	
		if hum != huma:
			sf.setFridgeHumidity(float(huma))

		time.sleep(1)

except KeyboardInterrupt:

	p.stop()
	GPIO.cleanup()