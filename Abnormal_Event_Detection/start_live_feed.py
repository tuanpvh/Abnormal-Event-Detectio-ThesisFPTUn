'''

Running The Spatiotemporal autoencoder on live webcam field


run python3 start_live_feed.py 'path_to_model' to start the feed and processing





Author: Harsh Tiku


'''





import cv2
import numpy as np 



def mean_squared_loss(x1,x2):


	''' Compute Euclidean Distance Loss  between 
	input frame and the reconstructed frame'''




	diff=x1-x2
	a,b,c,d,e=diff.shape
	n_samples=a*b*c*d*e
	sq_diff=diff**2
	Sum=sq_diff.sum()
	dist=np.sqrt(Sum)
	mean_dist=dist/n_samples

	return mean_dist

threshold=0.1
def abnomaly_detect(frames, model):
	imagedump=[]
	for frame in frames:
		frame=cv2.resize(frame,(227,227))
		#Convert the Image to Grayscale
		gray=0.2989*frame[:,:,0]+0.5870*frame[:,:,1]+0.1140*frame[:,:,2]
		gray=(gray-gray.mean())/gray.std()
		gray=np.clip(gray,0,1)
		imagedump.append(gray)


	imagedump=np.array(imagedump)
	imagedump.resize(227,227,10)
	imagedump=np.expand_dims(imagedump,axis=0)
	imagedump=np.expand_dims(imagedump,axis=4)

	# print('Processing data')
	output=model.predict(imagedump)
	loss=mean_squared_loss(imagedump,output)

	# print(loss)
	if loss>threshold:
		return 1
	return 0

		


