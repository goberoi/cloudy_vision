
import base64
import json
import requests

def _convert_image_to_base64(image_filename):
    with open(image_filename, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    return encoded_string

def call_vision_api(image_filename, api_keys):
    api_key = api_keys['google']
    post_url = "https://vision.googleapis.com/v1/images:annotate?key=" + api_key

    base64_image = _convert_image_to_base64(image_filename)

    post_payload = {
      "requests": [
        {
          "image": {
            "content" : base64_image
          },
          "features": [
            {
              "type": "LABEL_DETECTION",
              "maxResults": 10
            },
            {
              "type": "FACE_DETECTION",
              "maxResults": 10
            },
            {
              "type": "LANDMARK_DETECTION",
              "maxResults": 10
            },      
            {
              "type": "LOGO_DETECTION",
              "maxResults": 10
            },
            {
              "type": "SAFE_SEARCH_DETECTION",
              "maxResults": 10
            },          
          ]
        }
      ]
    }

    result = requests.post(post_url, json=post_payload)
    result.raise_for_status()

    return result.text

# Return array of dicts, each with keys 'name' and 'score'.
def get_tags_from_api_result(api_result):
    tags = []
    for annotation in api_result['responses'][0]['labelAnnotations']:
      tags.append({ 
        'name' : annotation['description'],
        'score' : annotation['score']
        })
    return tags


def get_standardized_result(api_result):
    output = {
        'tags' : {},
    }

    api_result = api_result['responses'][0]

    for tag in api_result['labelAnnotations']:
        output['tags'][tag['description']] = tag['score']

    if 'logoAnnotations' in api_result:
        output['logo_annotations'] = {}
        for annotation in api_result['logoAnnotations']:
            output['logo_annotations'][annotation['description']] = annotation['score']

    return output
