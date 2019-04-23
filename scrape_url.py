import csv

# hard coded file name that contains single column of image ids
input_file = 'Volcano.csv'

# Core parts of url
url1 = 'https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission='
url2 = '&roll='
url3 = '&frame='

# Begin reading input feature file
with open(input_file, 'r') as f:
    # Reader object containes all csv values
    reader = csv.reader(f)
    # row = a python list of all values in single row
    for row in reader:
        img_id = row[0]
        # Separates the three sections of image id
        img_list = img_id.split('-')
        # Formats the final url for given image id
        url = '{}{}{}{}{}{}'.format(url1, img_list[0], url2, img_list[1], url3,
                                    img_list[2])
        # print(url)


