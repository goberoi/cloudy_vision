from jinja2 import FileSystemLoader, Environment
from shutil import copyfile
import json
import numpy as np
import os
import pprint
import shutil
import time
import re
import vendors.google
import vendors.microsoft
import vendors.clarifai_
import vendors.ibm
import vendors.cloudsight_
import vendors.rekognition


SETTINGS = None
def settings(name):
    """Fetch a settings parameter."""

    # Initialize settings if necessary.
    global SETTINGS
    if SETTINGS is None:

        # Change this dict to suit your taste.
        SETTINGS = {
            'api_keys_filepath' : './api_keys.json',
            'input_images_dir' : 'input_images',
            'output_dir' : 'output',
            'static_dir' : 'static',
            'output_image_height' : 200,
            'vendors' : {
                'google' : vendors.google,
                'msft' : vendors.microsoft,
                'clarifai' : vendors.clarifai_,
                'ibm' : vendors.ibm,
                'cloudsight' : vendors.cloudsight_,
                'rekognition' : vendors.rekognition,
            },
            'resize': False,
            'statistics': [
                'response_time',
                'tags_count',
                'matching_tags_count',
                'matching_confidence',
            ],
            'tagged_images': False,
            'tags_filepath': './tags.json',
        }

        # Load API keys
        with open(SETTINGS['api_keys_filepath']) as data_file:
            SETTINGS['api_keys'] = json.load(data_file)

    return SETTINGS[name]


if settings('resize'):
    import cv2


def log_status(filepath, vendor_name, msg):
    filename = os.path.basename(filepath)
    print("%s -> %s" % ((filename + ", " + vendor_name).ljust(40), msg))


def resize_and_save(input_image_filepath, output_image_filepath):
    image = cv2.imread(input_image_filepath)
    height = image.shape[0]
    width = image.shape[1]
    aspect_ratio = float(width) / float(height)

    new_height = settings('output_image_height')
    new_width = int(aspect_ratio * new_height)

    output_image = cv2.resize(image, (new_width, new_height))
    cv2.imwrite(output_image_filepath, output_image)


def render_from_template(directory, template_name, **kwargs):
    loader = FileSystemLoader(directory)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    return template.render(**kwargs)


def vendor_statistics(image_results):
    vendor_stats = {}
    for vendor in settings('vendors'):
        vendor_results = []
        for image_result in image_results:
            for res in image_result['vendors']:
                if res['vendor_name'] == vendor:
                    vendor_results.append(res)

        vendor_stats[vendor] = []
        for stat_key in settings('statistics'):
            values = np.array([vr[stat_key] for vr in vendor_results])
            vendor_stats[vendor].append({
                'name': 'average ' + stat_key,
                'value': np.average(values)
            })
            vendor_stats[vendor].append({
                'name': 'standard deviation ' + stat_key,
                'value': np.std(values)
            })

    return vendor_stats


def find_matching_tags(tags, standardized_result):
    matching_tags = set()
    for tag in tags:
        p = re.compile(tag, re.IGNORECASE)
        for res_tag in standardized_result['tags']:
            if p.match(res_tag[0]):
                matching_tags.add(res_tag)

    return list(matching_tags)


def process_all_images():

    image_results = []

    # Create the output directory
    if not os.path.exists(settings('output_dir')):
        os.makedirs(settings('output_dir'))

    # Read image labels
    if settings('tagged_images'):
        with(open(settings('tags_filepath'), 'r')) as tags_file:
            tags = json.loads(tags_file.read())

    # Loop through all input images.
    for filename in os.listdir(settings('input_images_dir')):

        # Only process files that have these image extensions.
        if not filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            continue

        # Create a full path so we can read these files.
        filepath = os.path.join(settings('input_images_dir'), filename)

        image_tags = []
        if settings('tagged_images'):
            image_tags = tags[filename]

        # Create an output object for the image
        image_result = {
            'input_image_filepath' : filepath,
            'output_image_filepath' : filename,
            'vendors' : [],
            'image_tags' : image_tags,
        }
        image_results.append(image_result)

        # Walk through all vendor APIs to call.
        for vendor_name, vendor_module in sorted(settings('vendors').iteritems(), reverse=True):

            # Figure out filename to store and retrive cached JSON results.
            output_json_filename = filename + "." + vendor_name + ".json"
            output_json_path = os.path.join(settings('output_dir'), output_json_filename)

            # And where to store the output image
            output_image_filepath = os.path.join(settings('output_dir'), filename)

            # Check if the call is already cached.
            if os.path.isfile(output_json_path):

                # If so, read the result from the .json file stored in the output dir.
                log_status(filepath, vendor_name, "skipping API call, already cached")
                with open(output_json_path, 'r') as infile:
                    api_result = json.loads(infile.read())

            else:

                # If not, make the API call for this particular vendor.
                log_status(filepath, vendor_name, "calling API")
                api_call_start = time.time()
                api_result = vendor_module.call_vision_api(filepath, settings('api_keys'))
                api_result['response_time'] = time.time() - api_call_start

                # And cache the result in a .json file
                log_status(filepath, vendor_name, "success, storing result in %s" % output_json_path)
                with open(output_json_path, 'w') as outfile:
                    outfile.write(json.dumps(api_result))

                # Resize the original image and write to an output filename
                log_status(filepath, vendor_name, "writing output image in %s" % output_image_filepath)
                if settings('resize'):
                    resize_and_save(filepath, output_image_filepath)
                else:
                    copyfile(filepath, output_image_filepath)


                # Sleep so we avoid hitting throttling limits
                time.sleep(1)

            # Parse the JSON result we fetched (via API call or from cache)
            standardized_result = vendor_module.get_standardized_result(api_result)

            tags_count = 0
            matching_tags = []
            matching_confidence = 0
            if 'tags' in standardized_result:
                tags_count = len(standardized_result['tags'])

                if settings('tagged_images'):
                    matching_tags = find_matching_tags(image_tags, standardized_result)

                    if len(matching_tags) > 0:
                        matching_confidence = sum([t[1] for t in matching_tags]) / len(matching_tags)

            image_result['vendors'].append({
                'api_result' : api_result,
                'vendor_name' : vendor_name,
                'standardized_result' : standardized_result,
                'output_json_filename' : output_json_filename,
                'response_time' : api_result['response_time'],
                'tags_count' : tags_count,
                'matching_tags' : matching_tags,
                'matching_tags_count' : len(matching_tags),
                'matching_confidence' : matching_confidence,
            })

    # Compute global statistics for each vendor
    vendor_stats = vendor_statistics(image_results)

    # Render HTML file with all results.
    output_html = render_from_template(
        '.',
        os.path.join(settings('static_dir'), 'template.html'),
        image_results=image_results,
        vendor_stats=vendor_stats
    )

    # Write HTML output.
    output_html_filepath = os.path.join(settings('output_dir'), 'output.html')
    with open(output_html_filepath, 'w') as output_html_file:
        output_html_file.write(output_html.encode('utf-8'))


if __name__ == "__main__":
    process_all_images()
