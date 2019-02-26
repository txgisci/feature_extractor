# Feature Extractor Script

The purpose of the CLI script is to automate the process of downloading specified images from https://eol.jsc.nasa.gov/SearchPhotos/ 


## Installing
Step 1. Install Conda:

A powerful package manager and environment manager that you use with command line commands at the Anaconda Prompt for Windows, or in a Terminal window for macOS or Linux.
```
https://docs.anaconda.com/anaconda/install/
```


Step 2. Get Conda Running: 

Follow the sections 'Before you start', 'Contents' and 'Starting conda' on Conda's offical user guide site. 
```
https://conda.io/docs/user-guide/getting-started.html
```

Step 3. Set Up the Environment:

Create a new environment with a Python version of 3.4 or greater. 

Requests should be the only non-built-in Python library imported into the script. If you don't already have requests installed as a package, open your anacondona prompt and type:
```
pip3 install requests 
```



## Downlading the repository to your local machine

Step 1. Follow the link below and confirm you are in the 'master' branch.
```
https://github.com/txgisci/feature_extractor
```

Step 2. Click the green drop down option titled 'Clone or download'.

Step 3. Download the zip file, open your command prompt and navigate to the newly downloaded 'feature extractor' repository

## To get the script running

NOTE: All available feature files are already present in the 'inputs' folder. 
You can also create a custom list of image ids you want to download and place the csv file in the inputs folder. 

The script takes 1 argument: The name of the file you want to read in 
##### An example command would be something like

```
python feature_extractor.py basin.csv
```

### Optional arguments 

1. By default, the script downloads the high resolution version of the image. To download the low resolution version include the flag '--small' 
```
python feature_extractor.py basin.csv --small
```

2. By default, the script downloads images without crosshairs. To download the images with crosshairs include the flag '--with_crosshairs'
```
python feature_extractor.py basin.csv --with_crosshairs
```
The crosshairs image only comes in the high-resolution option. Including the '--small' flag won't affect the default output. 


## Expected output

The script will display progress messages, alerting the user everytime an image is successfully processed.

All images will populate in a folder named the same name of the csv file the user typed in. 

This new folder will appear in the 'outputs' folder.




