import numpy as np
import cv2
import os

# this two lines are for loading the videos.
# in this case the video are named as: example_1.mp4, example_2.mp4, ...,

# videofiles = [n for n in os.listdir('.') if n[0]=='e' and n[-4:]=='.mp4' and (n[-5]=='2' or n[-5]=='1' )]
# videofiles = sorted(videofiles, key=lambda item: int( item.partition('.')[0][3:]))

videofiles = [n for n in os.listdir('.') if n[0]=='e' and n[-4:]=='.mp4']
videofiles = sorted(videofiles)

video_index = 0
cap = cv2.VideoCapture(videofiles[0])

# video resolution: 1624x1234 px
# fourcc = cv2.cv.CV_FOURCC('F','M','P', '4')
fourcc = cv2.cv.CV_FOURCC(*'MP4V')

out = cv2.VideoWriter("video.mp4", fourcc, 15, (1624, 1234), 1)

while(cap.isOpened()):
    ret, frame = cap.read()
    if frame is None:
        print ("end of video " + str(video_index) + " .. next one now")
        video_index += 1
        if video_index >= len(videofiles):
            break
        cap = cv2.VideoCapture(videofiles[ video_index ])
        ret, frame = cap.read()
    cv2.imshow('frame',frame)
    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print ("end")
