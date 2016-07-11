
# Cloudy Vision: a tool for comparing computer vision APIs

Run a corpus of images through multiple computer vision API vendors. View image labeing results side by side. Supported vendors: Microsoft, IBM, Google, Cloudsight, and Clarifai.

[View example output.](https://github.com/goberoi/cloudy_vision)

[Read this blog post for details.](#)

## How it works

1. Cloudy Vision is a Python script, that given a directory of images, and a list of API vendors, will do the following for each image:
1. Call each vendor API for that image (or skip it if the result is already cached), e.g. call Google Cloud Vision for dog_at_the_park.jpg.
1. Store the results in a JSON file with the name in the following format: filename.vendor.json, e.g. dog_at_the_park.jpg.google.json.
1. Create a scaled copy of the original image with height 200px.
1. Generate an HTML page, output.html, that shows all the images and labeling results in an easy to consume manner.

## Usage

1. Get keys for each vendor, and put them in a file called api_keys.json (copy example_api_keys.json to get started).
1. Install dependencies (see below).
1. Place all your images in `./input_images`.
1. Run the script: `python cloudy_vision.py`
1. View `./output/output.html` to see results. 
1. If you add more images later, simply re-run the script. Prior results are cached and so those API calls will not be made again.

## Installation

Install these dependencies:
```
pip install cloudsight
pip install git+git://github.com/Clarifai/clarifai-python.git
pip install --upgrade watson-developer-cloud
pip install Jinja2
```

And OpenCV... which can be a pain. OpenCV is only used to resize the images for display. If you don't care about this, you can remove the dependencie, and remove the call to resize and copy images (or email me for help).

## Contributing

If you make modifications that may help others, please fork and send me a pull request. Some ideas for contributions:
1. Add new image recognition vendors.
1. Expose more attributes per vendor, e.g. face detection.
1. Bugs, requests, feedback.

## Credits

Authored by @goberoi.

## License

MIT License - Copyright (c) 2016 Gaurav Oberoi.


