import numpy as np
import cv2
import sys, time
import socket
import bluetooth
import uuid

playing = False
current_frame = 0
current_screen = 0

demo_screens = [ # name, num of frames
	('splash',1),
	]
greeting_screens = [
	('hello', 750)
	]

data = []

def bluetooth_ops():

	services = bluetooth.find_service(address="F8:95:C7:6B:97:11")
	if len(services) > 0:
		return greeting_screens


	return None

def play_vid_series(screens, fps=30):
	screens = demo_screens
	global current_frame
	global current_screen
	current_screen = 0
	current_frame = 0
	while True:
		if not playing:
			x = bluetooth_ops()
		if x!=None and not playing:
			global playing
			playing = True
			screens = x
			current_screen = 0
			current_frame = 0
			try:
				cap.release()
			except:
				print("yolo")
		if current_frame == 0:
			print(screens)
			cap = cv2.VideoCapture('ui/'+screens[current_screen][0]+'.avi')
			cv2.namedWindow("window")
		elif current_frame == screens[current_screen][1]-1:
			cap.release()
			current_screen += 1
			current_frame = 0
			if current_screen > len(screens)-1:
				current_screen = 0
				break
			continue
		#, cv2.WND_PROP_FULLSCREEN)
		#cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
		ret, frame = cap.read()
		print(time.time())
		#color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
		cv2.imshow('window', small)
		current_frame += 1
		if cv2.waitKey(int(700/fps)) & 0xFF == ord('q'):
			sys.exit(0)

while True:
	try:
			playing = False
			play_vid_series(demo_screens)
	except KeyboardInterrupt:
		sys.exit(0)
	except Exception:
		current_frame = 0
		current_screen = 0
		screens = demo_screens

cv2.destroyAllWindows()