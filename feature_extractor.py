# investigate all possible mission names
# add error check if file not present

import requests
import csv
import os
import re

# test values entered in via CLI
input_file = "Basin.csv"
img_size = "small"

# main url
url = "https://eol.jsc.nasa.gov/DatabaseImages/ESC"

# creates output folder in current working directory
cwd = os.getcwd()
# deletes '.csv' at the end of file name entered
new_folder = input_file[:-4]
# creates name of output folder
output_path = cwd + '\\' + new_folder + '\\'
# cre
os.makedirs(new_folder, mode=0o777, exist_ok=False)

# reads in csv file
with open(input_file, 'r') as f:
    # reader object containes all csv values
    reader = csv.reader(f)
    # row = a python list of values in each line of csv file
    for row in reader:
        # populates the current image information for url
        img_id = row[0]
        # regular expression isolates the mission name
        mission = re.findall(r'\w+',img_id)[0]
        # url of specified image
        img_url = "{}/{}/{}/{}.JPG".format(url, img_size, mission, img_id)
        # GET request to site
        response = requests.get(img_url)
        # 404 code = image not found
        if response.status_code == 404:
            print("ERROR 404: File not found for image id: " + img_id)
        # 200 code = image found and returned
        elif response.status_code == 200:
            # creates image path and name
            output_file = "{}{}.jpg".format(output_path, img_id)
            # writes image to output file
            with open(output_file, 'wb') as f:
                f.write(response.content)
