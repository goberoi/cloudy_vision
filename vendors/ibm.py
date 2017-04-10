from watson_developer_cloud import VisualRecognitionV3

def call_vision_api(image_filename, api_keys):
    api_key = api_keys['ibm']

    # Via example found here:
    # https://github.com/watson-developer-cloud/python-sdk/blob/master/examples/visual_recognition_v3.py
    visual_recognition = VisualRecognitionV3('2016-05-20', api_key=api_key)

    with open(image_filename, 'rb') as image_file:
        result = visual_recognition.classify(images_file=image_file)

    return result


def get_standardized_result(api_result):
    output = {
        'tags' : [],
    }

    api_result = api_result["images"][0]

    if "error" in api_result:
        # Check for error
        output['tags'].append(("error-file-bigger-than-2mb", None))
    else:
        api_result = api_result["classifiers"][0]
        for tag_data in api_result['classes']:
            output['tags'].append((tag_data['class'], tag_data['score']))

    return output
