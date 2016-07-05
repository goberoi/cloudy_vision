import cv2
from jinja2 import FileSystemLoader, Environment
import json
import numpy
import os
import pprint
import shutil
import time
import vendors.google
import vendors.microsoft
import vendors.clarifai_
import vendors.ibm
import vendors.cloudsight_


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
                'cloudsight' : vendors.cloudsight_
            }
        }

        # Load API keys
        with open(SETTINGS['api_keys_filepath']) as data_file: 
            SETTINGS['api_keys'] = json.load(data_file)

    return SETTINGS[name]
        

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


def process_all_images():

    image_results = []

    # Create the output directory
    if not os.path.exists(settings('output_dir')):
        os.makedirs(settings('output_dir'))

    # Loop through all input images.
    for filename in os.listdir(settings('input_images_dir')):

        # Only process files that have these image extensions.
        if not filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            continue

        # Create a full path so we can read these files.
        filepath = os.path.join(settings('input_images_dir'), filename)

        # Create an output object for the image
        image_result = {
            'input_image_filepath' : filepath,
            'output_image_filepath' : filename,
            'vendors' : []
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
                    raw_api_result = infile.read()

            else:

                # If not, make the API call for this particular vendor.
                log_status(filepath, vendor_name, "calling API")
                raw_api_result = vendor_module.call_vision_api(filepath, settings('api_keys'))

                # And cache the result in a .json file
                log_status(filepath, vendor_name, "success, storing result in %s" % output_json_path)
                with open(output_json_path, 'w') as outfile:
                    outfile.write(raw_api_result)

                # Resize the original image and write to an output filename
                log_status(filepath, vendor_name, "writing output image in %s" % output_image_filepath)
                resize_and_save(filepath, output_image_filepath)

                # Sleep so we avoid hitting throttling limits
                time.sleep(1)

            # Parse the JSON result we fetched (via API call or from cache)
            api_result = json.loads(raw_api_result)

            standardized_result = vendor_module.get_standardized_result(api_result)
            image_result['vendors'].append({
                'api_result' : api_result,
                'vendor_name' : vendor_name,
                'standardized_result' : standardized_result,
                'output_json_filename' : output_json_filename
            })


    # Render HTML file with all results.
    output_html = render_from_template('.', os.path.join(settings('static_dir'), 'template.html'), image_results=image_results)
    
    # Write HTML output.
    output_html_filepath = os.path.join(settings('output_dir'), 'output.html')
    with open(output_html_filepath, 'w') as output_html_file:
        output_html_file.write(output_html)

       
if __name__ == "__main__":
    process_all_images()
#    print vendors.clarifai_.get_acces_token(settings('api_keys'))

