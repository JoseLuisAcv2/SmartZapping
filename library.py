import os
import uuid
import random
import numpy as np
from random import shuffle
import matplotlib.pyplot as plt
from scipy import misc
from personGroupLib import detectFaceInImage, createPerson, addFace
import httplib, urllib, base64

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def cutImage(imgFile, coords):
	
	pos_x = int(coords[0])
	pos_y = int(coords[1])
	len_x = int(coords[2])
	len_y = int(coords[3])

	logo = imgFile[pos_y:pos_y+len_y, pos_x:pos_x+len_x]
	
	return logo

def readImage(fileName):
	return misc.imread(fileName)

def extraMetadata(metadataFile):
	data = []
	with open(metadataFile) as f:
		for line in f:
			data.append(line[:-1].split(","))
	return data

def extraLogoData():
	cnt = 1
	logoData = []
	rootdir = 'train'
	saveDir = 'Logos'
	subdirs = [x[0] for x in os.walk(rootdir)]
	for subdir in subdirs:
		metadataFile = os.path.join(subdir, 'metadata.txt')
		if os.path.isfile(metadataFile):
			metadata = extraMetadata(metadataFile)
			for meta in metadata:
				for file in os.listdir(subdir):
					if file.endswith('.jpg'):
						if meta[0] != 'kabel1':
							continue
						imgFile = readImage(os.path.join(subdir, file))
						logo = cutImage(imgFile, meta[1:])
						print('Extracting {}: {}'.format(cnt,os.path.join(subdir, file)))
						cnt += 1
						logoData.append((logo,meta[0]))
	return logoData

def saveLogoData():
	cnt = 0
	saveDir = 'Logos'
	logoData = extraLogoData()
	shuffle(logoData)
	N = len(logoData)
	for data in logoData:
		if not os.path.isdir(os.path.join(saveDir,data[1])):
			os.makedirs(os.path.join(saveDir,data[1]))
		logoGray = rgb2gray(data[0])
		plt.imshow(logoGray, cmap = plt.get_cmap('gray'))
		plt.savefig(os.path.join(saveDir,data[1],str(uuid.uuid4())))
		print('Saving logo {}/{}'.format(cnt,N))
		cnt += 1
		if cnt == 40:
			break;

def getMeta():
	cnt = 1
	rootdir = 'train'
	results = set()
	subdirs = [x[0] for x in os.walk(rootdir)]
	for subdir in subdirs:
		metadataFile = os.path.join(subdir, 'metadata.txt')
		if os.path.isfile(metadataFile):
			metadata = extraMetadata(metadataFile)
			for meta in metadata:
				results.add((meta[0],meta[1],meta[2],meta[3],meta[4]))
	
	for result in results:
		print(result)


def createFaceData():
	cnt = 1
	rootdir = 'train'
	subdirs = [x[0] for x in os.walk(rootdir)]
	for subdir in subdirs:
		metadataFile = os.path.join(subdir, 'metadata.txt')
		if os.path.isfile(metadataFile):
			metadata = extraMetadata(metadataFile)
			for meta in metadata:
				cnt = 0
				for file in os.listdir(subdir):
					if file.endswith('.jpg'):

						facesData = detectFaceInImage(os.path.join(subdir, file))
						imgFile = 	readImage(os.path.join(subdir, file))
						for faceData in facesData:
							coords = [faceData['faceRectangle']['left'],faceData['faceRectangle']['top'],faceData['faceRectangle']['width'],faceData['faceRectangle']['height']]
							faceImg = cutImage(imgFile, coords)
							plt.imshow(faceImg)
							#plt.savefig(os.path.join(saveDir,meta[0],str(uuid.uuid4())))
							
							personId = createPerson(meta[0])
							addFace(personId, meta[0], os.path.join(subdir, file), coords)

							print('Extracting {}: {}'.format(cnt,os.path.join(subdir, str(uuid.uuid4()))))
						
						if len(facesData) > 0:
							cnt += 1
							if cnt == 50:
								# More than n images from same directory
								break
