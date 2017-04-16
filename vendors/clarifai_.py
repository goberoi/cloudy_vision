from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage


def call_vision_api(image_filename, api_keys):
    app = ClarifaiApp()
    model = app.models.get('general-v1.3')
    image = ClImage(file_obj=open(image_filename, 'rb'))
    result = model.predict([image])
    return result


def get_standardized_result(api_result):
    output = {
        'tags': []
    }

    concepts = api_result['outputs'][0]['data']['concepts']
    tag_names = []
    tag_scores = []

    for concept in concepts:
        tag_names.append(concept['name'])
        tag_scores.append(concept['value'])

    output['tags'] = zip(tag_names, tag_scores)

    return output
