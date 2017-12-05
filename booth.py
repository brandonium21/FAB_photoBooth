#Dependacies
import picamera
from PIL import Image
import uuid
from random import randint
import facebook
from time import sleep
import datetime
import os
#initialize

#variables
current_image = ''
oauth_access_token = "EAAaX99auJb8BAGIs6mkG093zOJkTx57ifZBEX0cezTjc9p48LXsZCKPYb4pTxUTpPZAoolWPbZBoix6xv2CFOQUEXF9hCCZBGGUQQFCA9OId8qWJpqKIln6DFZBgvK6uT8YxNPsv5JBrdr1XkvEVgZCiZBLfnqejiZCMpLJIgbZBeh3iG6bmfoH3swKBuBAEfzFuMZD"
t_photo = True
#config

cam = picamera.PiCamera()
cam.resolution = (800,1200)
cam.brightness = 60

#text = input("prompt")
try:
	if t_photo:
		#Take Photo
		cam.start_preview()

		# show overlay on preview
		# Load the arbitrarily sized image
		skin = "booth-{}.png".format(randint(1, 3))
		img = Image.open(skin)
		pad = Image.new('RGB', (
	    	((img.size[0] + 31) // 32) * 32,
	    	((img.size[1] + 15) // 16) * 16,
	    ))
		pad.paste(img, (0, 0))
		o = cam.add_overlay(pad.tobytes(), size=img.size)
		o.alpha = 128
		o.layer = 3

		#count Down
		cam.annotate_text = 'Get Ready!'
		sleep(1)
		cam.annotate_text = 'ONE'
		sleep(1)
		cam.annotate_text = 'TWO'
		sleep(1)
		cam.annotate_text = 'THREE'
		sleep(1)

		#Name and capture photo
		current_image = 'booth_cap_{}.jpg'.format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
		cam.capture(current_image)

		#turn of camera
		cam.stop_preview()

		#Overlay Photo
		background = Image.open(current_image)
		overlay = Image.open(skin)

		background = background.convert("RGBA")
		overlay = overlay.convert("RGBA")

		new_img = Image.blend(background, overlay, 0.5)
		#Save Photo
		final_photo = "booth-{}.png".format(str(uuid.uuid4()))
		new_img.save(final_photo ,"PNG")


		#Upload Photo
		graph = facebook.GraphAPI(oauth_access_token)
		#photo = open(final_photo, "rb")
		# Upload an image with a caption.
		graph.put_photo(image=open(final_photo, 'rb'), message="From Brandon's Photo booth")
		#graph.put_object("me", "photos", message="From Brandon's Photo booth", source=photo.read())
		photo.close()

		#delete photos
		os.remove(final_photo)
		os.remove(current_image)

		# Reset
		t_photo = False
except KeyboardInterrupt:
	print('Booth Stopped!')