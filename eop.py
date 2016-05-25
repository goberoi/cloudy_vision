
# Fetch and process images
#
# For each file in 'input-images' directory:
#   For each api_vendor in api_vendors dictionary:
#     api_results = check if cached_api_results directory contains a cached result for that vendor, e.g. for my_image.png and Google, check for my_image.google.json.
#     If api_results is empty:
#       api_result = Vendor.fetch_vision_api_results(image_filename)
#       write cached file, e.g. my_image.google.json
#     Vendor.draw_face_detection_markers(image_filename) --> my_image.google.face.png
#     html_snippets.append(Vendor.html_output(filename, api_result))
#

import json
import os
import time
import vendors.google
import vendors.microsoft


input_images_dir = "input_images"
output_dir = "output"
vendor_list = [ vendors.google, vendors.microsoft ]
with open('api_keys.json') as data_file: api_keys = json.load(data_file)

def log_status(filepath, vendor, msg):
    filename = os.path.basename(filepath)
    print("%s -> %s" % ((filename + ", " + get_vendor_name(vendor)).ljust(40), msg))

def get_vendor_name(vendor_package_name):
    return vendor_package_name.__name__.split(".")[1]

def call_vendors_for_all_images():
    for filename in os.listdir(input_images_dir):
        filepath = os.path.join(input_images_dir, filename)
        if filepath.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            for vendor in vendor_list:
                output_json_path = os.path.join(output_dir, os.path.splitext(filename)[0] + "." + get_vendor_name(vendor) + ".json")

                if os.path.isfile(output_json_path):
                    log_status(filepath, vendor, "skipping, already cached")
                else:
                    log_status(filepath, vendor, "calling API")
                    api_result = vendor.call_vision_api(filepath, api_keys)

                    log_status(filepath, vendor, "success, storing result in %s" % output_json_path)
                    with open(output_json_path, 'w') as outfile:
                        json.dump(api_result, outfile)

                    time.sleep(1)

if __name__ == "__main__":
    call_vendors_for_all_images()

#    result = vendors.google.call_vision_api("input_images/front_door_package.jpg", api_keys)
#    print(result)
