import argparse
import requests
import csv
import os
import re
import sys
from pathlib import Path
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import urllib3

# CLI accepting user input
parser = argparse.ArgumentParser(prog='feature_extractor',
                                 description='Scrape a list of image ids from"\
                                 " GAPE by pulling images based on URL.')
parser.add_argument('feature_file', action='store', type=str,
                    help='CSV file of image ids')
parser.add_argument('--small', action='store_true', help="Download images with"\
                    " low resolution (default: high resolution)")
parser.add_argument('--with_crosshairs', action='store_true', help="Download"\
                    " images with crosshairs (default: no crosshairs)")
args = parser.parse_args()

# User enters the small option cia CLI
if args.small:
    img_size = 'small'
else:
    img_size = 'large'

# Max number of retries
total_retries = 5

# Checking if input file is present
input_file = os.path.join('.','inputs', args.feature_file)
file = Path(input_file)
try:
    file.resolve()
except FileNotFoundError:
    print("*** ERROR: File: " + args.feature_file + " does not exist. ***")
    print("\nTerminating script.")
    sys.exit()
else:
    new_folder = args.feature_file[:-4]

if args.with_crosshairs:
    # Core urls for images with crosshairs
    url_1 = "https://eol.jsc.nasa.gov/CatalogersAccess/GetRotatedImage"\
            ".pl?image="
    url_2 = "&rotation=1&MarkCenter=1"
else:
    # Core url for general images
    url = "https://eol.jsc.nasa.gov/DatabaseImages"

# Noted ids with _2 extenstion in name
anomalous_ids = ['ISS002-E-5448', 'ISS002-E-5632', 'ISS002-E-5633',
                 'ISS002-E-5634']

# Creating all new directories with full permission in octal
mode = 0o777

# Create an outputs folder if one doesn't exist
outputs_dir = os.path.join('.','outputs')
if not os.path.isdir(outputs_dir):
    os.makedirs(outputs_dir, mode=mode)

# Alerts for folder duplicate
output_path = os.path.join(outputs_dir, new_folder, "")
try:
    os.makedirs(output_path, mode=mode)
except FileExistsError:
    print("\n*** ERROR: Cannot create folder with name " + new_folder +
          " because the folder alread exists. ***")
    print("\nTerminating script.")
    sys.exit()

# Finds the number of ids in csv file
with open(input_file, 'r') as p:
        total_count = sum(1 for counter1 in p)

# Intitial output message
print("\nTotal number of image ids in file: " + str(total_count) + "\n")

# Counter for progress of image downloads
count_total = 0

count_success = 0


# Begin reading input feature file
with open(input_file, 'r') as f:

    # Reader object containes all csv values
    reader = csv.reader(f)
    # row = a python list of all values in single row
    for row in reader:
        # Populates the current image information for url
        img_id = row[0]
        # Regular expression isolates the mission name
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

        # Account for the few images with extended name
        if img_id in anomalous_ids:
            img_id = img_id + '_2'

        if args.with_crosshairs:
            img_url = '{}{}{}'.format(url_1, img_id, url_2)
        else:
            img_url = '{}/{}/{}/{}/{}.JPG'.format(url, abbrev, img_size,
                                                  mission, img_id)

        s = requests.Session()
        retries = Retry(total=total_retries,
                        backoff_factor=0.1,
                        status_forcelist=[ 500, 502, 503, 504 ])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        # Prints to screen the success or failure of download
        try:
            response = s.get(img_url)

        except requests.exceptions.RetryError:
            print("*** ERROR: Reached the max amount of retries ( " +
            str(total_retries) + " ) for image id: " + str(img_id) + " ***\n")
            count_total += 1

        else:
            if response.status_code == 404: # Image not found
                print("ERROR 404: File not found for image id: " + img_id)
            elif response.status_code == 200: # Image found and returned
                # Print progress to screen
                count_total += 1
                count_success += 1
                print("Processed image " + str(count_total) + " / " +
                      str(total_count))

                # Creates image path and name
                output_file = '{}{}.jpg'.format(output_path, img_id)

                # Writes image to output file
                with open(output_file, 'wb') as i:
                    i.write(response.content)

print("\n*** " + str(count_success) + " Images successfully downloaded ***")
