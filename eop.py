
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
# Render web page
# 
# For each file in 'input-images' directory:
#   html += draw a big new div
#   html += the image
#   for each api_vendor in api_vendors dictionary:
#     api_results = pull results for that 

import json
import vendors.google

vendor_list = [ vendors.google ]
with open('api_keys.json') as data_file:
    api_keys = json.load(data_file)

def call_vendors_for_all_images():
    for vendor in vendor_list:
        api_result = vendor.call_vision_api("hello.png", api_keys)
        print(api_result)

if __name__ == "__main__":
#    call_vendors_for_all_images()
    result = vendors.google.call_vision_api("input_images/front_door_package.jpg", api_keys)
    print(result)
