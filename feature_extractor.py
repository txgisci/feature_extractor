import argparse # CLI library
import requests
import csv
import os
import re
import sys
from pathlib import Path

# CLI accepting user input
parser = argparse.ArgumentParser(prog='feature_extractor', description='Process image ids.')
parser.add_argument('feature_file', action='store', type=str, help='File to be read in')
parser.add_argument('size', action='store', type=str, help='size')
args = parser.parse_args()

input_file = os.path.join(".","inputs", args.feature_file)
img_size = args.size

file = Path(input_file)
try:
    file.resolve()
except FileNotFoundError:
    print("*** ERROR: File: " + args.feature_file + " does not exist. ***")
    print("\nTerminating script.")
    sys.exit()
else:
    new_folder = args.feature_file[:-4]


# main url
url = "https://eol.jsc.nasa.gov/DatabaseImages"

# creating directory with full permission in octal
mode = 0o777

outputs_dir = os.path.join(".","outputs")

# Create an outputs folder if one doesn't exist
if not os.path.isdir(outputs_dir):
    os.makedirs(outputs_dir, mode=mode)

output_path = os.path.join(outputs_dir, new_folder, "")

try:
    os.makedirs(output_path, mode=mode)
except:
    print("\n*** ERROR: Cannot create folder with name " + new_folder +\
          " because the folder alread exists. ***")
    print("\nTerminating script.")
    sys.exit()

# Finds the number of ids in csv file
with open(input_file, 'r') as p:
        total_count = sum(1 for counter1 in p)


print("\nTotal images to be downloaded: " + str(total_count) + "\n")

# counter for progress of image downloads
count1 = 0

# reads in csv, closes file
with open(input_file, 'r') as f:

    # reader object containes all csv values
    reader = csv.reader(f)

    # row = a python list of values in each line of csv file
    for row in reader:

        # populates the current image information for url
        img_id = row[0]
        # regular expression isolates the mission name
        mission = re.findall(r'\w+',img_id)[0]

        # Accounting for varying mission names
        if 'E' in img_id:
            abbrev = 'ESC'
            if img_size == 'lowres':
                img_size = 'small'
            elif img_size == 'highres':
                img_size = 'large'
        else:
            abbrev = 'ISD'
            if img_size == 'small':
                img_size = 'lowres'
            elif img_size == 'large':
                img_size = 'highres'

        # url of specified image
        img_url = "{}/{}/{}/{}/{}.JPG".format(url, abbrev, img_size, mission,\
                                              img_id)

        # GET request to site
        response = requests.get(img_url)

        # 404 code = image not found
        if response.status_code == 404:
            print("ERROR 404: File not found for image id: " + img_id)
            print(img_url)
        # 200 code = image found and returned
        elif response.status_code == 200:
            count1 += 1

            print("Downloaded " + str(count1) + " / " + str(total_count))
            # creates image path and name
            output_file = "{}{}.jpg".format(output_path, img_id)

            # writes image to output file
            with open(output_file, 'wb') as i:
                i.write(response.content)
