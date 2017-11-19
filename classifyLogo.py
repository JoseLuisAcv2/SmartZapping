#!/usr/bin/python
import os
import io
import sys
import json
import operator
from PIL import Image
from library import cutImage, readImage
from predictLib import predict, extractLogosfromFaces

def analize(predictions, bestImage):
	score = dict()
	print('----------------')
	print('FINAL PREDICTION')
	for logo in predictions:
		if predictions[logo] > 0.2:
			print('{}: {}'.format(logo,predictions[logo]))

	bestLogo = max(predictions.iteritems(), key=operator.itemgetter(1))[0]
	print('')
	print('FINAL LOGO CLASIFICATION: {}'.format(bestLogo))
	print('FINAL SCORE: {}'.format(predictions[bestLogo]))
	print('----------------')
	bestImage.save(bestLogo+'.jpg')
		

def updatePrediction(newPrediction, totalPrediction, curImage, bestImage, bestTotalPrediction, prominentLogos):
	for prediction in newPrediction['Predictions']:
		logo = prediction['Tag']
		probability = prediction['Probability']
	
		if logo.lower() in prominentLogos:
			prediction['Probability'] = min(prediction['Probability'] + 0.5001, 0.9999)
			probability = prediction['Probability']

		elif len(prominentLogos) > 0 and logo.lower() not in prominentLogos:
			prediction['Probability'] = max(prediction['Probability'] - 0.5001, 0.0001)
			probability = prediction['Probability']

		if logo not in totalPrediction:
			totalPrediction[logo] = probability
		else:
			totalPrediction[logo] = max(totalPrediction[logo],probability)

		if totalPrediction[logo] > bestTotalPrediction:
			bestTotalPrediction = totalPrediction[logo]
			bestImage = curImage

	for logo in totalPrediction:
		if totalPrediction[logo] > 0.2:
			print('{}: {}'.format(logo, totalPrediction[logo]))
	print('')
	return bestImage, bestTotalPrediction

def main():

	if len(sys.argv) <= 1:
		usage()
		sys.exit()

	imgPath  = sys.argv[1]
	imgFile  = open(imgPath, 'rb').read()
	imgFile2 = readImage(imgPath)

	prominentLogos = extractLogosfromFaces(imgPath)
	for x in prominentLogos:
		prominentLogos.remove(x)
		prominentLogos.add(x.lower())

	print('--------------')
	print("POSSIBLE LOGOS:")
	if len(prominentLogos) == 0:
		print("filtering not possible.")
	for logo in prominentLogos:
		print(logo)
	print('--------------')
	print('')

	coords = []
	checkingCoords = []
	with open('logoMetadata.txt') as f:
		for line in f:
			datalogo = (line.split(",")[0]).lower()
			crd = line.strip().split(",")[1:]
			coords.append(crd)
			if datalogo in prominentLogos:
				checkingCoords.append(crd)
			

	if len(checkingCoords) == 0:
		checkingCoords = coords

	bestImage = None
	bestTotalPrediction = 0
	totalPrediction = dict()
	for coord in checkingCoords:
		print('Try coordinates: {}'.format(coord))
		imgCutLogo = cutImage(imgFile2,coord)
		
		imgCutLogo = Image.fromarray(imgCutLogo, 'RGB')
		
		imgByteArr = io.BytesIO()
		imgCutLogo.save(imgByteArr, format='PNG')
		imgByteArr = imgByteArr.getvalue()
		newPrediction = predict(imgByteArr)

		bestImage, bestTotalPrediction = updatePrediction(newPrediction, totalPrediction, imgCutLogo, bestImage, bestTotalPrediction, prominentLogos)

		if bestTotalPrediction > 0.95:
			break;

	analize(totalPrediction, bestImage)


def usage():
	print("Usage: ./classifyLogo image_file")

if __name__ == "__main__":
	main()