import exifread
import os
import argparse
from geopy.geocoders import Nominatim, OpenMapQuest
from geopy.point import Point
import re
import time
import shutil

lat_long_tags = [
    'GPS GPSLatitude',
    'GPS GPSLongitude',
    'GPS GPSLatitudeRef',
    'GPS GPSLongitudeRef'
]
date_tag = 'EXIF DateTimeOriginal'


def get_tags(folder):
    tag_dict = {}
    for p_file in os.listdir(folder):
        ext = os.path.splitext(itemname)[1] 
        if not ext in ['.jpg', '.png', '.jpeg', '.tiff']:
            continue
        f = open(os.path.join(folder, p_file), 'rb')
        tags = exifread.process_file(f)
        f.close()
        tag_dict[os.path.join(folder, p_file)] = tags 
    return tag_dict

def convert_location(lat, longt, lat_d, long_d):
    lat = [value if not isinstance(value, exifread.classes.Ratio) else value.num / value.den for value in lat.values]
    longt = [value if not isinstance(value, exifread.classes.Ratio) else value.num / value.den for value in longt.values]
    point_str = '{} {}m {:.3f}s {} {} {}m {}s {}'.format(*lat, lat_d, *longt, long_d)
    point = Point(point_str)
    geolocator = Nominatim(user_agent="Photo_Wiz")
    location = geolocator.reverse(point)
    return location.raw['address']

def copy_image(src, dst):
    src_root = os.path.splitdrive(os.path.abspath(src))
    dst_root = os.path.splitdrive(os.path.abspath(dst))
    if src_root == dst_root:
        os.link(src, dst)
    else:
        shutil.copyfile(src, dst)

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('-s', '--source_folder', required=True, help='Folder to search for pictures.')
    argp.add_argument('-d', '--dest_folder', required=True, help='Base folder for storage.')
    args = argp.parse_args()
    tags_dict = get_tags(args.source_folder)
    for itemname, tags in tags_dict.items():
        date_struct = time.strptime(tags.get(date_tag).printable, "%Y:%m:%d %H:%M:%S")
        e_time = int(time.mktime(date_struct) * 100)
        addr = convert_location(*[tags.get(l) for l in lat_long_tags])
        folders = [os.path.join(args.dest_folder, 'location_sort', addr['state'], addr['county']),
                   os.path.join(args.dest_folder, 'time_sort', str(date_struct.tm_year), str(date_struct.tm_mon))]
        ext = os.path.splitext(itemname)[1]
        print('Backed up {} to:'.format(itemname))
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
            copy_image(itemname, os.path.join(folder, '{}{}'.format(e_time, ext)))
            print('\t{}'.format(os.path.join(folder, '{}{}'.format(e_time, ext))))



