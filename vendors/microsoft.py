import json
import requests

def call_vision_api(image_filename, api_keys):
    api_key = api_keys['microsoft']['api_key']
    location = api_keys['microsoft']['location']
    post_url = "https://" + location + ".api.cognitive.microsoft.com/vision/v1.0/analyze?visualFeatures=Categories,Tags,Description,Faces,ImageType,Color,Adult&subscription-key=" + api_key

    image_data = open(image_filename, 'rb').read()
    result = requests.post(post_url, data=image_data, headers={'Content-Type': 'application/octet-stream'})
    result.raise_for_status()

    return json.loads(result.text)

# Return a dictionary of features to their scored values (represented as lists of tuples).
# Scored values must be sorted in descending order.
#
# {
#    'feature_1' : [(element, score), ...],
#    'feature_2' : ...
# }
#
# E.g.,
#
# {
#    'tags' : [('throne', 0.95), ('swords', 0.84)],
#    'description' : [('A throne made of pointy objects', 0.73)]
# }
#
def get_standardized_result(api_result):
    output = {
        'tags' : [],
        'captions' : [],
        'categories' : []
#        'adult' : [],
#        'image_types' : []
#        'tags_without_score' : {}
    }

    if 'description' in api_result:
        if 'tags' in api_result['description']:
            for tag_data in api_result['description']['tags']:
                output['tags'].append((tag_data, None))
                    # tags do not have confidence or scores

        if 'captions' in api_result['description']:
            for caption in api_result['description']['captions']:
                output['captions'].append((caption['text'], caption['confidence']))

    if 'categories' in api_result:
        for category in api_result['categories']:
            output['categories'].append((category['name'], category['score']))

    if 'color' in api_result:
        output['colors'] = []
        for color_type in ['accentColor', 'dominantColorBackground', 'dominantColorForeground']:
            if color_type in api_result['color']:
                output['colors'].append((api_result['color'][color_type], None, color_type))
                    # colors do not have confidence or scores
        if 'dominantColors' in api_result['color']:
            for color in api_result['color']['dominantColors']:
                output['colors'].append((color, None, 'dominant'))

#    output['adult'] = api_result['adult']

#    output['image_types'] = api_result['imageType']

    return output
