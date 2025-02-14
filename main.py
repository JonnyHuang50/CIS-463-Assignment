'''
Hai-Hsin Huang
HR: Souces on Canvas and instructor's demo
'''
from gpiozero import DistanceSensor, LED
import time
import signal

led_blue = LED(0)
led_red = LED(4)
led_green = LED(5)
sensor = DistanceSensor(14, 12)  #(sensor-gpio, trigger-gpio)
sensor.max_distance = 3
sensor.threshold_distance_1 = 0.3 #1st threshold distance
sensor.threshold_distance_2 = 0.6 #2nd threshold distance
sensor.threshold_distance_3 = 0.9 #3rd threshold distance

while True:
    print('Distance to nearest object is ', int(sensor.distance * 100), ' cm')
    if sensor.distance < sensor.threshold_distance_1: #blue LED on if match 1st threshold distance
        led_blue.on()
        led_red.off()
        led_green.off()
    elif sensor.distance < sensor.threshold_distance_2: #red LED on if match 1st threshold distance
        led_blue.off()
        led_red.on()
        led_green.off()
    elif sensor.distance < sensor.threshold_distance_3: #green LED on if match 1st threshold distance
        led_blue.off()
        led_red.off()
        led_green.on()
    else: #all LEDs off when out of all the threshold distance above
        led_blue.off()
        led_red.off()
        led_green.off()
        
    time.sleep(0.5)
