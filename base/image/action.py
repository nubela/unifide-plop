import urllib
from decimal import Decimal
from PIL import ExifTags
import os
from base import S3
from base.S3 import S3Object
from base.image.model import Image
from base.util import __gen_uuid, coerce_bson_id
from cfg import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME, UPLOAD_FOLDER, CLOUDFRONT_URL, DOMAIN, UPLOAD_RELATIVE_ENDPOINT
import Image as PILImage

def save(img_obj):
    col = Image.collection()
    id = col.insert(img_obj.serialize())
    return id


def __store_locally(filename, img_stream):
    #save it to disk
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    f = open(file_path, 'wb+')
    f.write(img_stream.read())
    f.close()

    #fix img mode
    img = PILImage.open(file_path)
    if img.mode != 'RGB': # Fix IOError: cannot write mode P as PPM
        img = img.convert('RGB')
        img.save(file_path, "JPEG")


def __store_s3(filename, img_stream):
    conn = S3.AWSAuthConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    obj = S3Object(img_stream.read())
    conn.put(S3_BUCKET_NAME, filename, obj)


def __new_img_obj(filename, height, storage, width):
    img_obj = Image()
    img_obj.file_name = filename
    img_obj.storage = storage
    img_obj.width = width
    img_obj.height = height
    save(img_obj)
    return img_obj


def save_image(image_stream, storage=None):
    #store binary
    filename = __gen_uuid()
    file_path = __store_locally(filename, image_stream)
    if storage == ImageStorage.S3:
        __store_s3(filename, image_stream)

    #get pil img obj
    pil_img = PILImage.open(file_path)
    width, height = pil_img.size

    #save document record
    img_obj = __new_img_obj(file_path, filename, height, storage, width)

    #cleanup
    if storage != ImageStorage.LOCAL:
        os.remove(file_path)

    return img_obj


def __resize_img(img, new_width, new_height):
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


def __rotate_upright(img):
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
    filename = __gen_uuid()
    temp_file_path = os.path.join(UPLOAD_FOLDER, filename)
    urllib.urlretrieve(url_for(img_obj), temp_file_path)
    img = PILImage.open(temp_file_path)
    img = __resize_img(__rotate_upright(img), new_width, new_height)
    img.save(temp_file_path, "JPEG")

    #upload
    f = open(temp_file_path, 'r')
    if img_obj.storage == ImageStorage.S3:
        __store_s3(filename, f)
    f.close()

    #create obj
    resized_obj = __new_img_obj(filename, new_height, img_obj.storage, new_width)

    #cleanup
    if img_obj.storage != ImageStorage.LOCAL:
        os.remove(temp_file_path)

    return resized_obj


def resize(img_obj, new_width, new_height):
    resized_obj = find(img_obj.file_name, new_width, new_height)

    if resized_obj is None:
        resized_obj = __resize(img_obj, new_height, new_width, resized_obj)

    return resized_obj


def get(id):
    coll = Image.collection()
    dic = coll.find_one({"_id": coerce_bson_id(id)})
    return Image.unserialize(dic) if dic is not None else None


def find(filename, width=None, height=None):
    coll = Image.collection()
    find_params_lis = [
        {"file_name": filename},
    ]
    if width is not None and height is not None:
        find_params_lis += [
            {"width": width},
            {"height": height},
        ]
    dic = coll.find_one({"$and": find_params_lis})
    return Image.unserialize(dic) if dic is not None else None


def url_for(image_obj):
    if image_obj.storage == ImageStorage.S3:
        return "%s%s" % (CLOUDFRONT_URL, image_obj.file_name)
    return "%s%s%s" % (DOMAIN, UPLOAD_RELATIVE_ENDPOINT, image_obj.file_name)


class ImageStorage:
    S3 = "s3"
    LOCAL = "local"