import json
import httplib, urllib, base64
from personGroupLib import detectFaceInImage, faceIdentify, getPerson

def predict(imgFile):

	headers = {
	    # Request headers
	    'Content-Type': 'application/octet-stream',
	    'Prediction-key': '18dd754c6da94f538ec11c416029b5e1',
	}

	params = urllib.urlencode({
	    # Request parameters	
	})

	projectID = "96b92da9-f8b9-41e1-ab8f-26d691a649ee"
	body = imgFile

	try:
	    conn = httplib.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
	    conn.request("POST", "/customvision/v1.0/Prediction/"+projectID+"/image?%s" % params, body, headers)
	    response = conn.getresponse()
	    prediction = response.read()
	    conn.close()
	except Exception as e:
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	prediction = json.loads(prediction)
	return prediction

def extractLogosfromFaces(imgName): # FALTA
	logos = set()
	faces = detectFaceInImage(imgName)
	for face in faces:
		matchFaces = faceIdentify(face['faceId'])
		for matchFace in matchFaces:
			for candidate in matchFace['candidates']:
				matchPerson = getPerson(candidate['personId'])
				logo = matchPerson['userData']
				logos.add(logo)

	return logos