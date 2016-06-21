import base64
import json
import requests
from clarifai.client import ClarifaiApi

def call_vision_api(image_filename, api_keys):
    clarifai_api = ClarifaiApi(app_id = api_keys['clarifai']['client_id'],
                               app_secret = api_keys['clarifai']['client_secret'])
    result = clarifai_api.tag_images(open(image_filename, 'rb'))
    text_result = json.dumps(result)
    return text_result

def get_standardized_result(api_result):
    output = {
        'tags' : []
    }

    api_result = api_result['results'][0]

    tag_names = api_result['result']['tag']['classes']
    tag_scores = api_result['result']['tag']['probs']
    output['tags'] = zip(tag_names, tag_scores)

    return output
