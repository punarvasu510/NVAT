import numpy as np
import cv2

cap = cv2.VideoCapture('example_1.mp4')
#ret, frame = cap.read()	

while(cap.isOpened()):
#while(ret):
	ret, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	cv2.imshow('frame',gray)
	if cv2.waitKey(5) & 0xFF == ord('q'):
	    break

	#ret, frame = cap.read()

cap.release()
cv2.destroyAllWindows()
