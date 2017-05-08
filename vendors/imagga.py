# -*- coding: utf-8 -*-
import os
import json
import requests


def call_vision_api(image_filename, api_keys):
	api_key = api_keys['imagga']['api_key']
	api_secret = api_keys['imagga']['api_secret']
	
	# image_filename = os.path.abspath(image_filename)
	
	response = requests.post('https://api.imagga.com/v1/content',
			auth=(api_key, api_secret),
			files={'image': open(image_filename, 'rb')})

	upload_result = response.json()
	content_id = upload_result['uploaded'][0]['id']
	
	# print ("content id: %s" % content_id)
	
	response = requests.get('https://api.imagga.com/v1/tagging?content=%s' % content_id, auth=(api_key, api_secret))
	
	# print response.text
	
	return json.loads(response.text)


def get_standardized_result(api_result):
    output = {
        'tags' : [],
    }

    if 'unsuccessful' in api_result:
        output['tags'].append(("error: " + api_result['unsuccessful'][0]['message'], None))
    elif 'results' in api_result:
        api_result = api_result["results"][0]
        for tag_data in api_result['tags']:
            output['tags'].append((tag_data['tag'], tag_data['confidence'] / 100))
    else:
        output['tags'].append(('unknown error', None))

    return output

	