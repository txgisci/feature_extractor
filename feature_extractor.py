
import argparse # CLI library
import requests
import csv
import os
import re
import sys

# CLI accepting user input
parser = argparse.ArgumentParser(prog='feature_extractor', description='Process image ids.')
parser.add_argument('feature_file', action='store', type=str, help='File to be read in')
parser.add_argument('size', action='store', type=str, help='size')
args = parser.parse_args()

#input_file = '.\\inputs\\' + args.feature_file
input_file = os.path.join(".","inputs", args.feature_file)

try:
    f = open(input_file)
    f.close()
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

# Create an outputs folder if one doesn't already exist
if not os.path.isdir(os.path.join(".","outputs")):
    outputs_dir = os.path.join(".","outputs")
    os.makedirs(outputs_dir, mode=mode)

output_path = os.path.join(".","outputs", new_folder, "")
# generates output folder for feature
try:
    os.makedirs(output_path, mode=mode)
except:
    print("\n*** ERROR: Cannot create folder with name " + new_folder +\
          " because the folder alread exists. ***")
    print("\nTerminating script.")
    sys.exit()

# reads in csv file
with open(input_file, 'r') as f:

    # resets to small every time. Need to re-code
    img_size = "small"

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
            print(response.status_code)
            # creates image path and name
            output_file = "{}{}.jpg".format(output_path, img_id)

            # writes image to output file
            with open(output_file, 'wb') as i:
                i.write(response.content)
