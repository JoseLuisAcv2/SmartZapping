import PIL, json
import httplib, urllib, base64
import Image
import os, sys, uuid

subscriptionKey = '284ae21d230441229e2b80200e4e44bc'

def createPersonGroup():
    headers = {
        # Request headers.
        'Content-Type': 'application/json',

        'Ocp-Apim-Subscription-Key': subscriptionKey,
    }

    personGroupId = 'tvgroup'

    # The userData field is optional. The size limit for it is 16KB.
    body = "{ 'name':'Group1' }"

    try:
        # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the 
        #   URL below with "westus".
        conn = httplib.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
        conn.request("PUT", "/face/v1.0/persongroups/%s" % personGroupId, body, headers)
        response = conn.getresponse()

        # 'OK' indicates success. 'Conflict' means a group with this ID already exists.
        # If you get 'Conflict', change the value of personGroupId above and try again.
        # If you get 'Access Denied', verify the validity of the subscription key above and try again.
        print(response.reason)

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))



def getPersonGroup(personGroupId):

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': subscriptionKey,
    }

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups/"+personGroupId+"?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def listPersonGroup():

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': subscriptionKey,
    }

    params = urllib.urlencode({
        # Request parameters
    })

    try:
        conn = httplib.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def createPerson(label):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscriptionKey,
    }

    params = urllib.urlencode({
    })

    body = "{'name':'"+str(uuid.uuid4())+"', 'userData':'"+label+"',}"
    
    try:
        conn = httplib.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/tvgroup/persons?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return data['personId']

def addFace(personId, label, imgName, coord):

    uri_base = 'northeurope.api.cognitive.microsoft.com'

    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscriptionKey,
    }

    params = urllib.urlencode({
        # Request parameters
        'userData': label,
        'targetFace': '{},{},{},{}'.format(coord[0],coord[1],coord[2],coord[3])
    })

    body = open(imgName, 'rb').read()

    try:
        conn = httplib.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/tvgroup/persons/"+str(personId)+"/persistedFaces?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def detectFaceInImage(imgName):

    subscription_key = subscriptionKey
    uri_base = 'northeurope.api.cognitive.microsoft.com'

    # Request headers.
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request parameters.
    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
    })

    body = open(imgName, 'rb').read()

    try:
        conn = httplib.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return parsed


def trainPersonGroup():

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': subscriptionKey,
    }

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/persongroups/tvgroup/train?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def getTrainingStatus():
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': subscriptionKey,
    }

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups/tvgroup/training?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def faceIdentify(faceId):

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscriptionKey,
    }

    params = urllib.urlencode({
    })

    body = '{\
        "personGroupId":"tvgroup",\
        "faceIds":["'+str(faceId)+'"],\
        "maxNumOfCandidatesReturned":5,\
        "confidenceThreshold": 0.5\
    }'

    try:
        conn = httplib.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/identify?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        parsed = json.loads(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


    return parsed

def getPerson(personId):
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': subscriptionKey,
    }

    params = urllib.urlencode({
    })

    try:
        conn = httplib.HTTPSConnection('northeurope.api.cognitive.microsoft.com')
        conn.request("GET", "/face/v1.0/persongroups/tvgroup/persons/"+str(personId)+"?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        parsed = json.loads(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return parsed