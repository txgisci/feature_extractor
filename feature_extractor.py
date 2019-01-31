# investigate all possible mission names
# add error check if file not present

import requests
import csv
import os
import re

# test values entered in via CLI
input_file = "Island.csv"
new_folder = input_file[:-4]
input_file = 'inputs//' + input_file


#################################### read in input file from folder here

# main url
url = "https://eol.jsc.nasa.gov/DatabaseImages"

# creates output folder in current working directory
cwd = os.getcwd()
# deletes '.csv' at the end of file name entered


# creating directory with full permission in octal
mode = 0o777
# raises an OSError if target directory already exists
exist_ok = False

################### IF not present then call makedirs()
################### on outputs folder first
if not os.path.isdir('./outputs'):
    outputs_dir = cwd + '\\outputs\\'
    os.makedirs(outputs_dir, mode=mode, exist_ok=exist_ok)

output_path = cwd + '\\outputs\\' + new_folder + '\\'
# generates output folder
os.makedirs(output_path, mode=mode, exist_ok=exist_ok)

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

        if mission[:3] == 'ISS':
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
        img_url = "{}/{}/{}/{}/{}.JPG".format(url, abbrev, img_size, mission, img_id)

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
