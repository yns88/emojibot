import logging
import os
import re
import uuid

from google import google, images
from PIL import Image

crontable = []
outputs = []

emoji_regex = r':(.+):'
MAX_RESULTS = 4
SUPPORTED_FORMATS = ['.gif', '.png', '.jpg', '.jpeg']

logger = logging.getLogger(__name__)


def process_message(data):
    if data['channel'].startswith('D'):
        result = re.search(emoji_regex, data['text'])
        if result:
            emoji = result.group(1)
            options = images.ImageOptions()
            options.image_type = images.ImageType.CLIPART
            options.size_category = images.SizeCategory.ICON
            results = google.search_images(emoji, options, num_images=MAX_RESULTS * 2)
            # download_results(results, emoji)

            for result in results:
                if result.link[-4:].lower() in SUPPORTED_FORMATS:
                    outputs.append([data['channel'], result.link])
                if len(outputs) >= 4:
                    break


def download_results(results, name):
    path = 'download/%s_%s' % (name, uuid.uuid4())
    os.mkdir(path)
    images.download(results, path=path)
    image_files = os.listdir(path)
    for filename in image_files:
        try:
            full_path = '%s/%s' % (path, filename)
            image = Image.open(full_path)
            image.thumbnail((128, 128))
            if image.format == 'ICO':
                image.save('%s/resized_%s' % (path, filename), 'PNG')
            else:
                image.save('%s/resized_%s' % (path, filename), image.format)
        except IOError:
            print "IOError on %s" % filename
            logger.exception('IOError on %s', filename)
        except Exception:
            logger.exception('uknown error')

    return path
