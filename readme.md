
# Cloudy Vision: compare computer vision APIs

Run a corpus of images through multiple computer vision API vendors. View image labeing results side by side so that you can get a general feel for how well each vendor works for your use case. Supported vendors: Microsoft, IBM, Google, Cloudsight, Amazon (Rekognition) and Clarifai.

[View example output.](https://goberoi.github.io/cloudy_vision/output/output.html)

[Read this blog post for details.](#)

## How it works

1. For a given directory of images, and list of vendors:
1. Call each vendor API for that image (or skip it if cached), e.g. call Google for dog_at_the_park.jpg.
1. Store results in a JSON file with the name: filename.vendor.json, e.g. dog_at_the_park.jpg.google.json.
1. Optionally match the tags returned with your desired tags to test accuracy.
1. Calculate stats around response times, number of tags returned, etc.
1. Create a scaled copy of the original image with height 200px.
1. Generate output.html to show all the images and labeling results in an easy to consume manner.

## Usage

1. Get keys for each vendor, and put them in a file called api_keys.json (copy example_api_keys.json to get started).
1. Install dependencies (see below).
1. Place all your images in `./input_images`.
1. Run the script: `python cloudy_vision.py`
1. View `./output/output.html` to see results.
1. If you add more images, simply re-run the script. Prior results are cached.

### Note for Amazon Rekognition

The keys should not be placed in the api_keys.json file but in ~/.aws/credentials and ~/.aws/config. See http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-config-files

### Note for Clarifai

The keys should not be placed in the api_keys.json file but in ~/.clarifai/config. See https://github.com/Clarifai/clarifai-python#setup

## Desired Tags

You can specify tags that you hope to get, and see whether results from each vendor match. We'll compute these additional stats:
* matching_tags_count (average and standard deviation): number of api tags matching the image tags
* matching confidence (average and standard deviation): confidence of the matching tags

To work with tagged images, set the `tagged_images` setting to True and fill a tags.json file (copy example_tags.json to get started; this file contains a map `image_filename => tags`).

## Installation

Install these dependencies:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Note that installing Pillow can be dropped if you set settings['resize']=False.

## Contributing

If you make modifications that may help others, please fork and send me a pull request. Some ideas for contributions: (a) add new image recognition vendors, (b) expose more attributes per vendor, e.g. face detection, (c) bugs, requests, feedback.

## Credits

Authored by @goberoi.

Thanks to @lucasdchamps for several features: response time stats; matching with desired tags; Amazon Rekognition; and several other improvements.

## License

MIT License - Copyright (c) 2016 Gaurav Oberoi.
