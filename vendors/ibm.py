from watson_developer_cloud import VisualRecognitionV3

def call_vision_api(image_filename, api_keys):
    api_key = api_keys['ibm']['api_key']
    iam_url = api_keys['ibm']['url']
    language = api_keys['ibm']['language']

    # Via example found in the code snippets from the Implementation doc
    # in the IBM Watson dashboard/console
    visual_recognition = VisualRecognitionV3('2018-03-19',
        iam_api_key=api_key,
        url=iam_url)

    with open(image_filename, 'rb') as image_file:
        result = visual_recognition.classify(images_file=image_file, headers={'Accept-Language': language})

    return result


def get_standardized_result(api_result):
    color_indicators = ['color', 'couleur']
        # add color word in other languages if you use a different
        # language, as per the configs in api_keys
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

        # some tags contain the word "color", so we use that indicator
        # to extract color information. This is not as reliable as other
        # vendors providing structured information about colors, but it
        # is better than nothing
        color_tags = [tag for tag in api_result['classes'] for color_indicator in color_indicators if color_indicator in tag['class']]
        if len(color_tags) > 0:
            output['colors'] = []
            for color_tag in color_tags:
                color = color_tag['class']
                for color_indicator in color_indicators:
                    color = color.replace(color_indicator, '')
                color = color.strip()
                output['colors'].append((color, color_tag['score']))

    return output
