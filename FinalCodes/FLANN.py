import numpy as np
import cv2
from matplotlib import pyplot as plt
from db2 import Db

class Flann:

	
	def __init__(self,action1,action2):
		self.intruderId1 = action1.intruder_id
		self.intruderId2 = action2.intruder_id
		
		self.id1 = action1.id
		self.id2 = action2.id
		
		self.croppedImage = "intruder_profiles/cropFrame_{}.jpg".format(self.intruderId1)
		self.fullImage = "intruder_profiles/fullFrame_{}.jpg".format(self.intruderId2)
		
	def match(self):
		
		#vidcap = cv2.VideoCapture(video)
		img1 = cv2.imread(self.croppedImage,0)          # queryImage
		img2 = cv2.imread(self.fullImage,0) # trainImage

		#success = True
		#while success:
			#success,img2 = vidcap.read()


			# Initiate SIFT detector
		sift = cv2.xfeatures2d.SURF_create()

			# find the keypoints and descriptors with SIFT
		kp1, des1 = sift.detectAndCompute(img1,None)
		kp2, des2 = sift.detectAndCompute(img2,None)

			# FLANN parameters
		FLANN_INDEX_KDTREE = 1
		index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
		search_params = dict(checks=50)   # or pass empty dictionary
		flann = cv2.FlannBasedMatcher(index_params,search_params)
		matches = flann.knnMatch(des1,des2,k=2)

		# Need to draw only good matches, so create a mask
		matchesMask = [[0,0] for i in xrange(len(matches))]

		# ratio test as per Lowe's paper
		for i,(m,n) in enumerate(matches):
			if m.distance < 0.4*n.distance:
				matchesMask[i]=[1,0]
				flag = True
				print "Matched! id {} with id {}".format(self.intruderId1,self.intruderId2)
				try:
					
					conn = Db.get_connection()
					cursor = conn.cursor()
 
					print "Linking actions: {}, {}".format(self.id1, self.id2)
					cursor.callproc('project.LINK_INTRUDER_ACTIONS',(self.id1,self.id2))
					
					conn.commit()
 
					print "Results {}".format(cursor.fetchone())
				except Exception as e:
					print(e)
				break
			else:
				flag = False
				#print "Not a match id {} with {}".format(self.intruderId1,self.intruderId2) 
		'''
			draw_params = dict(matchColor = (0,255,0),
						singlePointColor = (255,0,0),
						matchesMask = matchesMask,
						flags = 0)
					   
		#img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
		#plt.imshow(img3,),plt.show()
		'''			

if __name__ == '__main__':
	f = Flann()
	#get images from db
	f.match()