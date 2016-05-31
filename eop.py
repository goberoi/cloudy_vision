import jinja2
import json
import os
import time
import vendors.google
import vendors.microsoft


# Global settings.
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
            'vendors' : {
                'google' : vendors.google,
                'microsoft' : vendors.microsoft
            }
        }

        # Load API keys
        with open(SETTINGS['api_keys_filepath']) as data_file: 
            SETTINGS['api_keys'] = json.load(data_file)

    return SETTINGS[name]
        

def log_status(filepath, vendor_name, msg):
    filename = os.path.basename(filepath)
    print("%s -> %s" % ((filename + ", " + vendor_name).ljust(40), msg))


def process_all_images():

    api_results = []

    # Loop through all input images.
    for filename in os.listdir(settings('input_images_dir')):

        # Only process files that have these image extensions.
        if not filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            continue

        # Create a full path so we can read these files.
        filepath = os.path.join(settings('input_images_dir'), filename)

        # Walk through all vendor APIs to call.
        for vendor_name, vendor_module in settings('vendors').iteritems():

            # Figure out filename to store and retrive cached JSON results.
            output_json_path = os.path.join(settings('output_dir'), filename + "." + vendor_name + ".json")

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

                # Sleep so we avoid hitting throttling limits
                time.sleep(1)

            # Parse the JSON result we fetched (via API call or from cache)
            api_result = json.loads(raw_api_result)
            log_status(filepath, vendor_name, "extracted tags %s" % vendor_module.get_tags_from_api_result(api_result))
            
            api_results.append(api_result)

if __name__ == "__main__":
    process_all_images()
