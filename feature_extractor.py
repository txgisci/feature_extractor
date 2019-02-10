import argparse
import requests
import csv
import os
import re
import sys
from pathlib import Path
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# CLI accepting user input
parser = argparse.ArgumentParser(prog='feature_extractor',
                                 description='Process image ids.')
parser.add_argument('feature_file', action='store', type=str,
                    help='File to be read in')
parser.add_argument('size', action='store', type=str, help='size')
args = parser.parse_args()

# Setting up user inputs
input_file = os.path.join(''.'','inputs', args.feature_file)
img_size = args.size

# Checking if input file is present
file = Path(input_file)
try:
    file.resolve()
except FileNotFoundError:
    print("*** ERROR: File: " + args.feature_file + " does not exist. ***")
    print("\nTerminating script.")
    sys.exit()
else:
    new_folder = args.feature_file[:-4]

# Core url
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
except:
    print("\n*** ERROR: Cannot create folder with name " + new_folder +
          " because the folder alread exists. ***")
    print("\nTerminating script.")
    sys.exit()

# Finds the number of ids in csv file
with open(input_file, 'r') as p:
        total_count = sum(1 for counter1 in p)

# Intitial output message
print("\nTotal images to be downloaded: " + str(total_count) + "\n")

# Counter for progress of image downloads
count1 = 0

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

        # Full url of current image
        img_url = '{}/{}/{}/{}/{}.JPG'.format(url, abbrev, img_size, mission,
                                              img_id)

        # Retry to account for connection errors
        s = requests.Session()
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[ 500, 502, 503, 504 ])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        # Prints to screen the success or failure of download
        try:
            response = s.get(img_url)
        except requests.exceptions.ConnectionError:
            print(response.status_code)
        else:
            if response.status_code == 404: # Image not found
                print("ERROR 404: File not found for image id: " + img_id)
                print(img_url)
            elif response.status_code == 200: # Image found and returned
                # Print progress to screen
                count1 += 1
                print("Downloaded image " + str(count1) + " / " +
                      str(total_count))

                # Creates image path and name
                output_file = '{}{}.jpg'.format(output_path, img_id)

                # Writes image to output file
                with open(output_file, 'wb') as i:
                    i.write(response.content)
