#Dependacies
import picamera
from PIL import Image
import uuid
from random import randint
import facebook
from time import sleep
import datetime
import os
from fractions import Fraction
from colour import Color
#initialize
#lalala
#variables
current_image = ''
oauth_access_token = "EAAaX99auJb8BAExUxtAYpzHmne4qWGZCyyv4oRZAodIkvxf8V9bgASKKV7XU54291gKpjVuSyCa2MlmZAaNVDAo8ffXSmcXPisOTTOfwX1EGmF9Ys3TEsrvLA1xHdTA9DqDGpVodpp5Vfaz58sydt2bZBr3iSnPyZCZCwfwxXCOTh1fdrxtn6ZCa2i5YAhQtHYZD"
t_photo = True
#config

cam = picamera.PiCamera()
cam.resolution = (800,1200)
cam.framerate = 32
cam.awb_mode='off'
cam.awb_gains=Fraction(8,5)
cam.exposure_mode='backlight'
cam.shutter_speed=31098
cam.brightness = 50
cam.ISO = 400
cam.meter_mode = 'spot'
cam.contrast= 0
cam.drc_strength= 'off'
cam.annotate_text_size = 160
#cam.annotate_foreground = Color('black')


#text = input("prompt")
cam.start_preview()
sleep(5)
try:
	if t_photo:
		#Take Photo
		cam.start_preview()

		# show overlay on preview
		# Load the arbitrarily sized image
		skin = "booth-{}.png".format(randint(1, 3))
		img = Image.open(skin)
		pad = Image.new('RGBA', (
	    	((img.size[0] + 31) // 32) * 32,
	    	((img.size[1] + 15) // 16) * 16,
	    ))
		pad.paste(img, (0, 0))
		o = cam.add_overlay(pad.tobytes(), size=img.size)
		o.alpha = 255
		o.layer = 3

		#count Down
		cam.annotate_text = 'Get Ready!'
		sleep(1)
		#cam.annotate_background = Color('red')
		cam.annotate_text = 'ONE'
		sleep(1)
		#cam.annotate_background = Color('yellow')
		cam.annotate_text = 'TWO'
		sleep(1)
		#cam.annotate_background = Color('green')
		cam.annotate_text = 'THREE'
		sleep(1)
		cam.annotate_text = ''

		#Name and capture photo
		current_image = 'booth_cap_{}.jpg'.format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
		cam.capture(current_image)

		#turn of camera
		cam.stop_preview()
		sleep(2)
		#Overlay Photo
		background = Image.open(current_image)
		overlay = Image.open(skin)

		background = background.convert("RGBA")
		overlay = overlay.convert("RGBA")
		background.paste(overlay, (0, 0), overlay)
		#background.show()
		#new_img = Image.blend(background, overlay, 0.5)
		#Save Photo
		final_photo = "booth-{}.png".format(str(uuid.uuid4()))
		#new_img.save(final_photo ,"PNG")
		background.save(final_photo ,"PNG")



		#Upload Photo
		graph = facebook.GraphAPI(oauth_access_token)
		#photo = open(final_photo, "rb")
		# Upload an image with a caption.
		graph.put_photo(image=open(final_photo, 'rb'), message="From Brandon's Photo booth")
		#graph.put_object("me", "photos", message="From Brandon's Photo booth", source=photo.read())
		#photo.close()

		#delete photos
		directory = "/home/pi/Documents/PhotoBooth/FAB_photoBooth/"
		os.remove((directory + final_photo))
		os.remove((directory + current_image))

		# Reset
		t_photo = False
except KeyboardInterrupt:
	print('Booth Stopped!')