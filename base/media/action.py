import imghdr
import multiprocessing
import urllib
from decimal import Decimal
import os

from PIL import ExifTags
import Image as PILImage
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from base.media.model import Media
from base.util import _gen_uuid, coerce_bson_id
from cfg import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME, UPLOAD_FOLDER, DOMAIN, UPLOAD_RELATIVE_ENDPOINT


def is_image(media_stream):
    ext = imghdr.what(None, media_stream.read())
    return ext in ["jpg", "gif", "png"]


def save(media_obj):
    col = Media.collection()
    id = col.save(media_obj.serialize())
    return id


def _store_locally(filename, file_stream, is_img=False):
    #save it to disk
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    f = open(file_path, 'wb+')
    f.write(file_stream.read())
    f.close()

    #fix img mode
    if is_img:
        img = PILImage.open(file_path)
        if img.mode != 'RGB': # Fix IOError: cannot write mode P as PPM
            img = img.convert('RGB')
            img.save(file_path, "JPEG")

    return file_path


def _store_s3(filename, file_path):
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(S3_BUCKET_NAME)
    k = Key(bucket)
    k.key = filename
    k.set_contents_from_filename(file_path)
    k.set_acl('public-read')
    return k.generate_url(expires_in=0, query_auth=False)


def _new_img_obj(filename, height, storage, width):
    img_obj = Media()
    img_obj.file_name = filename
    img_obj.storage = storage
    img_obj.width = width
    img_obj.height = height
    img_obj.file_type = MediaType.IMAGE
    img_obj._id = save(img_obj)
    return img_obj


def _defer_store_s3(file_path, filename, media_obj):
    url = _store_s3(filename, file_path)
    media_obj.storage = MediaStorage.S3
    media_obj.url = url
    save(media_obj)
    os.remove(file_path)


def save_media(media_stream, storage=None):
    if storage is None:
        storage = MediaStorage.LOCAL

    #store locally first
    filename = _gen_uuid()
    file_path = _store_locally(filename, media_stream)

    #save document record (as local first)
    media_obj = Media()
    media_obj.file_name = filename
    media_obj.storage = MediaStorage.LOCAL
    media_obj.file_type = MediaType.OTHERS
    media_obj._id = save(media_obj)

    #upload to s3, deferred/threaded
    if storage == MediaStorage.S3:
        t = multiprocessing.Process(target=_defer_store_s3, args=(file_path, filename, media_obj))
        t.daemon = False
        t.start()

    return media_obj


def save_image(image_stream, storage=None):
    if storage is None:
        storage = MediaStorage.LOCAL

    #store locally first
    filename = _gen_uuid()
    file_path = _store_locally(filename, image_stream)


    #get pil img obj
    pil_img = PILImage.open(file_path)
    width, height = pil_img.size

    #save document record
    img_obj = _new_img_obj(filename, height, storage, width)

    if storage == MediaStorage.S3:
        t = multiprocessing.Process(target=_defer_store_s3, args=(file_path, filename, img_obj))
        t.daemon = False
        t.start()

    return img_obj


def _resize_img(img, new_width, new_height):
    """
    resizes a larger image to a smaller one, while performing performing center crop.
    """
    # we don't wanna resize an image into a resolution thats larger than it already is
    w, h = img.size

    #both dimensions are smaller than what's needed
    if w <= new_width and h <= new_height:
        return img

    #get the larger side for center cropping for ratio shrinking
    width_offset = w - new_width
    height_offset = h - new_height
    if width_offset < height_offset:
        ratio_to_shrink = Decimal(new_width) / Decimal(w)
        img = img.resize((new_width, h * ratio_to_shrink))
    else:
        ratio_to_shrink = Decimal(new_height) / Decimal(h)
        img = img.resize((w * ratio_to_shrink, new_height))

    #center crop
    w, h = img.size
    width_offset = w - new_width
    height_offset = h - new_height
    if width_offset < height_offset:
        #centre height
        offset = height_offset / 2
        img = img.crop((0, offset, w, offset + new_height))
    else:
        #center width
        offset = width_offset / 2
        img = img.crop((offset, 0, offset + new_width, h))

    return img


def _rotate_upright(img):
    #rotate of exif info exists
    if hasattr(img, "_getexif"):
        if not img._getexif() is None:
            found_exif = False
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    found_exif = True
                    break
            exif = dict(img._getexif().items())

            if orientation in exif and found_exif:
                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)
    return img


def __resize(img_obj, new_height, new_width, resized_obj):
    #download + resize
    filename = _gen_uuid()
    temp_file_path = os.path.join(UPLOAD_FOLDER, filename)
    urllib.urlretrieve(url_for(img_obj), temp_file_path)
    img = PILImage.open(temp_file_path)
    img = _resize_img(_rotate_upright(img), new_width, new_height)
    img.save(temp_file_path, "JPEG")

    #upload
    f = open(temp_file_path, 'r')
    if img_obj.storage == MediaStorage.S3:
        _store_s3(filename, f)
    f.close()

    #create obj
    resized_obj = _new_img_obj(filename, new_height, img_obj.storage, new_width)

    #cleanup
    if img_obj.storage != MediaStorage.LOCAL:
        os.remove(temp_file_path)

    return resized_obj


def resize(img_obj, new_width, new_height):
    resized_obj = find(img_obj.file_name, new_width, new_height)

    if resized_obj is None:
        resized_obj = __resize(img_obj, new_height, new_width, resized_obj)

    return resized_obj


def get(id):
    coll = Media.collection()
    dic = coll.find_one({"_id": coerce_bson_id(id)})
    return Media.unserialize(dic) if dic is not None else None


def find(filename, width=None, height=None):
    coll = Media.collection()
    find_params_lis = [
        {"file_name": filename},
    ]
    if width is not None and height is not None:
        find_params_lis += [
            {"width": width},
            {"height": height},
        ]
    dic = coll.find_one({"$and": find_params_lis})
    return Media.unserialize(dic) if dic is not None else None


def url_for(media_obj):
    if media_obj.storage == MediaStorage.S3:
        return media_obj.url
    return "%s/%s/%s" % (DOMAIN, UPLOAD_RELATIVE_ENDPOINT, media_obj.file_name)


class MediaStorage:
    S3 = "s3"
    LOCAL = "local"


class MediaType:
    IMAGE = "img"
    OTHERS = "others"
