import logging
import os
import re
import uuid
import yaml

from google import google, images
from imgurpython import ImgurClient
from PIL import Image

crontable = []
outputs = []

emoji_regex = r':(.+):'
atemojibot_regex = r'<@U0F7XKZ61>'
MAX_RESULTS = 4
SUPPORTED_FORMATS = ['.gif', '.png', '.jpg', '.jpeg']

logger = logging.getLogger(__name__)


def process_message(data):
    try:
        find_emoji(data)
    except Exception:
        logger.exception('unknown error')


def find_emoji(data):
    body = data.get('text')
    if body and (data['channel'].startswith('D') or re.search(atemojibot_regex, body)):
        result = re.search(emoji_regex, body)
        if result:
            emoji = result.group(1)
            options = images.ImageOptions()
            options.image_type = images.ImageType.CLIPART
            options.size_category = images.SizeCategory.ICON
            results = google.search_images(emoji, options, num_images=MAX_RESULTS * 2)
            supported_results = [
                result for result in results
                if result.link and result.link[-4:].lower() in SUPPORTED_FORMATS
            ][:MAX_RESULTS]
            new_files = download_results(supported_results, emoji)
            imgur_links = upload_imgur(new_files)

            for imgur_link in imgur_links:
                outputs.append([data['channel'], imgur_link])


def download_results(results, name):
    path = 'download/%s_%s' % (name, uuid.uuid4())
    os.mkdir(path)
    images.fast_download(results, path=path, threads=4)
    image_files = os.listdir(path)
    new_files = []
    for filename in image_files:
        try:
            full_path = '%s/%s' % (path, filename)
            image = Image.open(full_path)
            image.thumbnail((128, 128))
            new_path = '%s/resized_%s' % (path, filename)
            image.save(new_path, image.format)
            new_files.append(new_path)
        except IOError:
            print "IOError on %s" % filename
            logger.exception('IOError on %s', filename)
        except Exception:
            logger.exception('unknown image error')

    return new_files


def upload_imgur(new_files):
    config = yaml.load(file('rtmbot.conf', 'r'))
    client = ImgurClient(config['IMGUR_CLIENT_ID'], config['IMGUR_SECRET'])
    imgur_links = []
    for filepath in new_files:
        try:
            imgur_result = client.upload_from_path(filepath)
            if imgur_result:
                imgur_link = imgur_result.get('link')
                if imgur_link:
                    imgur_links.append(imgur_link)
        except Exception:
            logger.exception('IMGUR fail')
    return imgur_links
