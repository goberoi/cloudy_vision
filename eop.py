import json
import os
import time
from SimpleCV import Image, Color, DrawingLayer
import vendors.google
import vendors.microsoft


input_images_dir = "input_images"
output_dir = "output"
vendor_list = [ vendors.google, vendors.microsoft ]
vendor_colors = {
    'google' : Color.GREEN,
    'microsoft' : Color.BLUE
}
with open('api_keys.json') as data_file: api_keys = json.load(data_file)

settings = {

    # Tag rendering parameters
    'tag_x_pos' : 5,
    'tag_bar_height' : 20,
    'font_size' : 20,
    'font_name' : "ubuntu"
}


def log_status(filepath, vendor, msg):
    filename = os.path.basename(filepath)
    print("%s -> %s" % ((filename + ", " + vendor_name(vendor)).ljust(40), msg))


def vendor_name(vendor_package_name):
    return vendor_package_name.__name__.split(".")[1]

def render_results_on_image(image, index, vendor, api_result):

    ## RENDER TAGS

    # Extract the tags
    tags = [tag['name'] for tag in vendor.get_tags_from_api_result(api_result)]
    tags.insert(0, vendor_name(vendor) + ":")

    # Set rendering
    layer = DrawingLayer(image.size())
    layer.setFontBold(False)
    layer.selectFont(settings['font_name'])
    layer.setFontSize(settings['font_size'])

    # Render the tags in the newly created bottom area
    y_pos = (layer.height - settings['tag_bar_height'] * (index + 1)) + 4
    layer.text(
        ", ".join(tags), 
        (settings['tag_x_pos'], y_pos), 
        color=Color.WHITE)

    image.addDrawingLayer(layer)

    ## RENDER FACE BOXES

    # TODO

    return image

def process_all_images():

    # Loop through all input images.
    for filename in os.listdir(input_images_dir):

        # Only process files that have these image extensions.
        if not filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            continue

        # Create a full path so we can read these files.
        filepath = os.path.join(input_images_dir, filename)

        # Create a copy of the image so we can render results on it.
        output_image = Image(filepath)

        # Expand the image at the bottom
        output_image = output_image.embiggen(
            (output_image.width, output_image.height + settings['tag_bar_height'] * len(vendor_list)), 
            Color.BLACK, 
            (0, 0))

        # Walk through all vendor APIs to call.
        for index, vendor in enumerate(vendor_list):
            output_json_path = os.path.join(output_dir, filename + "." + vendor_name(vendor) + ".json")

            # Check if the call is already cached.
            if os.path.isfile(output_json_path):

                # If so, read the result from the .json file stored in the output dir.
                log_status(filepath, vendor, "skipping API call, already cached")
                with open(output_json_path, 'r') as infile:
                    raw_api_result = infile.read()

            else:

                # If not, make the API call for this particular vendor.
                log_status(filepath, vendor, "calling API")
                raw_api_result = vendor.call_vision_api(filepath, api_keys)

                # And cache the result in a .json file
                log_status(filepath, vendor, "success, storing result in %s" % output_json_path)
                with open(output_json_path, 'w') as outfile:
                    outfile.write(raw_api_result)

                # Sleep so we avoid hitting throttling limits
                time.sleep(1)

            # Parse the JSON result we fetched (via API call or from cache)
            api_result = json.loads(raw_api_result)
            log_status(filepath, vendor, "extracted tags %s" % vendor.get_tags_from_api_result(api_result) )

            # Render this particular vendor's analysis on the copy of the original image.
            output_image = render_results_on_image(output_image, index, vendor, api_result)

            #if vendor_name(vendor) == 'google':
            #    break

        print("before save, width: %i, height: %i" % (output_image.width, output_image.height))

        # All vendors should have been rendered on this copy of the image. Write it to disk.
        output_image.save(os.path.join(output_dir, os.path.basename(filepath)))


if __name__ == "__main__":
    process_all_images()
