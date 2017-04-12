
# Cloudy Vision: compare computer vision APIs

Run a corpus of images through multiple computer vision API vendors. View image labeing results side by side so that you can get a general feel for how well each vendor works for your use case. Supported vendors: Microsoft, IBM, Google, Cloudsight, Amazon and Clarifai.

[View example output.](https://goberoi.github.io/cloudy_vision/output/output.html)

[Read this blog post for details.](#)

## Example results

A benchmark was run on 13/01/2017 with images from [Caltech 101](https://www.vision.caltech.edu/Image_Datasets/Caltech101/). We got the following results:

| API | avrg response time | std response time | avrg tags count | std tags count |
| ------- | -------- | -------- | ---- | --- |
| IBM | 1.18 | 0.33 | 7.45 | 2.79 |
| Google | 1.13 | 0.1 | 6.73 | 2.63 |
| Amazon | 1.34 | 0.57 | 5.91 | 4.99 |
| Clarifai | 1.88 | 0.29 | 20 | 0 |
| Microsoft | 1.99 | 0.71 | 3.2 | 2.77 |
| Cloudsight | 14.67 | 8.41 | 0 | 0 |

## How it works

1. For a given directory of images, and list of vendors:
1. Call each vendor API for that image (or skip it if cached), e.g. call Google for dog_at_the_park.jpg.
1. Store results in a JSON file with the name: filename.vendor.json, e.g. dog_at_the_park.jpg.google.json.
1. Create a scaled copy of the original image with height 200px.
1. Generate output.html to show all the images and labeling results in an easy to consume manner.

## Usage

1. Get keys for each vendor, and put them in a file called api_keys.json (copy example_api_keys.json to get started).
1. Install dependencies (see below).
1. Place all your images in `./input_images`.
1. Run the script: `python cloudy_vision.py`
1. View `./output/output.html` to see results.
1. If you add more images, simply re-run the script. Prior results are cached.

### Note for rekognition

The keys should not be placed in the api_keys.json file but in ~/.aws/credentials and ~/.aws/config. See http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-config-files

## Tagged images

You can work with tagged images. Cloudy will inspect the tags returned by the different APIs and look
for tags that match the image tags. From these matching tags, cloudy computes the following metrics:

* matching_tags_count (average and standard deviation): number of api tags matching the image tags
* matching confidence (average and standard deviation): confidence of the matching tags

To work with tagged images, set the `tagged_images` setting to True and fill a tags.json file (copy example_tags.json to get started).
This file contains a map `image_filename => tags`.

## Installation

Install these dependencies:
```
pip install numpy
pip install cloudsight
pip install git+git://github.com/Clarifai/clarifai-python.git
pip install --upgrade watson-developer-cloud
pip install Jinja2
pip install boto3
```

And OpenCV... which can be a pain. OpenCV is only used to resize the images for display. If you don't care about this, you can remove the dependencie, and remove the call to resize and copy images (or email me for help).

## Contributing

If you make modifications that may help others, please fork and send me a pull request. Some ideas for contributions: (a) add new image recognition vendors, (b) expose more attributes per vendor, e.g. face detection, (c) bugs, requests, feedback.

## Credits

Authored by @goberoi

## License

MIT License - Copyright (c) 2016 Gaurav Oberoi.
