import numpy as np
import cv2
import sys
import time

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#fourcc = cv2.VideoWriter_fourcc(*'MPEG')
#fourcc = cv2.VideoWriter_fourcc(*'X264')
fourcc = cv2.VideoWriter_fourcc(*'MP4V')

name = 'example_'+ sys.argv[1] +'.mp4'
out = cv2.VideoWriter(name,fourcc, 20.0, (640,480))

# To capture video for fixed duration
capture_duration = 30
start_time = time.time()

while(cap.isOpened() and int(time.time() - start_time) < capture_duration ):

    ret, frame = cap.read()
    if ret==True:
        #frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)

# To capture video until letter 'Q' is pressed
#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
