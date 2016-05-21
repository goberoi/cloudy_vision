
# For each file in 'input-images' directory:
#   For each api_vendor in api_vendors dictionary:
#     Check if cached_api_results directory contains a cached result for that vendor, e.g. for my_image.png and Google, check for my_image.google.json.
#     If it exists, skip to the next vendor.
#     If it does not, api_result = Vendor.fetch_vision_api_results(image_filename)
#     