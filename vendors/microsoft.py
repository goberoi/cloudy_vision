
import base64
import json
import requests

def call_vision_api(image_filename, api_keys):
    api_key = api_keys['microsoft']
    post_url = "https://api.projectoxford.ai/vision/v1.0/analyze?visualFeatures=Categories,Tags,Description,Faces,ImageType,Color,Adult&subscription-key=" + api_key

    image_data = open(image_filename, 'rb').read()
    result = requests.post(post_url, data=image_data, headers={'Content-Type': 'application/octet-stream'})
    result.raise_for_status()

    return result.text


def get_tags_from_api_result(api_result):
    tags = []
    for tag_data in api_result['tags']:
        tags.append({ 
            'name' : tag_data['name'],
          'score' : tag_data['confidence']
        })
    return tags


def get_standardized_result(api_result):
    output = {
        'tags' : {},
        'categories' : {},
        'adult' : {},
        'captions' : {},
        'image_types' : {}
#        'tags_without_score' : {}
    }

    for tag_data in api_result['tags']:
        output['tags'][tag_data['name']] = tag_data['confidence']

    for category in api_result['categories']:
        output['categories'][category['name']] = category['score']

    output['adult'] = api_result['adult']

    for caption in api_result['description']['captions']:
        output['captions'][caption['text']] = caption['confidence']

#    for tag in api_result['description']['tags']:
#        output['tags_without_score'][tag] = 'n/a'

    output['image_types'] = api_result['imageType']

    return output
