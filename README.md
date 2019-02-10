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

Use a Python version of 3.4 or greater. 

If you don't already have requests installed as a package, open your anacondona prompt and type:
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

## To get the script running:

NOTE: All csv files are already present in the 'inputs' file. 

The script takes 2 arguments: The name of the feature file you want to read in and the size/resolution of the image (small or large)
### An example command would be something like:

```
python feature_extractor.py basin.csv small 
```
The script will display progress messages, alerting the user everytime an image is successfully downloaded.

All images will populate in a folder named the same name of the csv file the user typed in. 

This new folder will appear in the 'outputs' folder.




