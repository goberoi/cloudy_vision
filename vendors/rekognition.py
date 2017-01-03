#sudo pip install boto3
import boto3
import json

def call_vision_api(image_filename, api_keys):
    api_key = api_keys['rekognition']
    if not api_key['client_id'] or not api_key['client_secret']:
        raise Exception('Missing AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY')

    client = boto3.client(
        'rekognition',
        region_name=api_key['region'],
        endpoint_url=api_key['endpoint_url'],
        verify=True,
        aws_access_key_id=api_key['client_id'],
        aws_secret_access_key=api_key['client_secret']
        )

    with open(image_filename, 'rb') as image:
        response = client.detect_labels(
            Image={'Bytes': image.read()}
        )
        result = json.dumps(response)
        return result


def get_standardized_result(api_result):
    output = {
        'tags' : [],
    }
    labels = api_result['Labels']
    for tag in labels:
        output['tags'].append((tag['Name'], tag['Confidence']/100))

    return output