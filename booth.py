#Dependacies
import picamera
import Image
import uuid
from random import randint

#initialize

#variables
current_image = ''
oauth_access_token = 'lb7KxI5Q7wjXcX9_lLLCm1a9AG4'
t_photo = True
#config

cam = picamera.PiCamera()
cam.resolution = (800,1200)
cam.brightness = 60

text = input("prompt")
if t_photo:
	#Take Photo
	cam.start_preview()

	#count Down
	cam.annotate_text = 'Get Ready!'
	sleep(1)
	cam.annotate_text = 'Uno'
	sleep(1)
	cam.annotate_text = '2'
	sleep(1)
	cam.annotate_text = 'Three'
	sleep(1)

	#Name and capture photo
	current_image = 'booth_cap_{}.jpg'.format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
	cam.capture(current_image)

	#turn of camera
	cam.stop_preview()

	#Overlay Photo
	background = Image.open(current_image)
	overlay = Image.open("skin-{}.jpg".format(randint(0, 2)))

	background = background.convert("RGBA")
	overlay = overlay.convert("RGBA")

	new_img = Image.blend(background, overlay, 0.5)
	#Save Photo
	final_photo = "booth-{}.png".format(str(uuid.uuid4()))
	new_img.save(final_photo ,"PNG")


	#Upload Photo
	graph = facebook.GraphAPI(oauth_access_token)
	photo = open(final_photo, "rb")
	graph.put_object("me", "photos", message="From Brandon's Photo booth", source=photo.read())
	photo.close()

	#delete photos
	os.remove(final_photo)
	os.remove(current_image)

	# Reset
	t_photo = False