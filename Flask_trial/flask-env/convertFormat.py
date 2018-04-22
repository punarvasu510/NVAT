import imageio
import os, sys
import string

class TargetFormat(object):
	MP4 = ".mp4"
	AVI = ".avi"
	@staticmethod
	def convertFile(inputpath, targetFormat):
    
		outputpath = os.path.splitext(inputpath)[0] + targetFormat
		print("converting\r\n\t{0}\r\nto\r\n\t{1}".format(inputpath, outputpath))

		reader = imageio.get_reader(inputpath)
		fps = reader.get_meta_data()['fps']

		writer = imageio.get_writer(outputpath, fps=fps)
		for i,im in enumerate(reader):
			sys.stdout.write("\rframe {0}".format(i))
			sys.stdout.flush()
			writer.append_data(im)
		print("\r\nFinalizing...")
		writer.close()
		print("Done.")

if __name__ == '__main__':
	folder = 'static/video_clips/'
	for the_file in os.listdir(folder):
		path = string.replace(the_file,"avi","mp4")
		if not os.path.exists(path):
				TargetFormat.convertFile("static/video_clips/"+the_file,TargetFormat.MP4)
		

