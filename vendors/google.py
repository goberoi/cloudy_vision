
import base64
import simplejson as json
import requests

def _convert_image_to_base64(image_filename):
    with open(image_filename, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def call_vision_api(image_filename, api_keys):
    base64_image = _convert_image_to_base64(image_filename)
    google_api_key = api_keys['google']
    post_url = "https://vision.googleapis.com/v1/images:annotate?key=" + google_api_key

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

