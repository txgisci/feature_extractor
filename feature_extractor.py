# investigate all possible mission names
# add error check if file not present

import requests
import csv
import os

# test values entered in via CLI
input_file = "Basin.csv"
img_size = "small"

url = "https://eol.jsc.nasa.gov/DatabaseImages/ESC"


# creates output folder in current working directory
cwd = os.getcwd()
new_folder = input_file[:-4]
output_path = cwd + '\\' + new_folder + '\\'
os.makedirs(new_folder, mode=0o777, exist_ok=False)

# reads in csv file
with open(input_file, 'r') as f:
    # loops through image ids
    reader = csv.reader(f)
    for row in reader:
        # populates the current image information for url
        img_id = row[0]

        #### If statement for if mission name starts with NAS, only 5 letters in mission name
        mission = img_id[:6]
        img_url = "{}/{}/{}/{}.JPG".format(url, img_size, mission, img_id)
        response = requests.get(img_url)
        # executes if http request successful
        if response.status_code == 200:
            # write image to new folder
            output_file = "{}{}.jpg".format(output_path, img_id)
            with open(output_file, 'wb') as f:
                f.write(response.content)
