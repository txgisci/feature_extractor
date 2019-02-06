# Feature Extractor Script

The purpose of the tool is to automate the process of downloading specified images from https://eol.jsc.nasa.gov/SearchPhotos/ 


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

### Alternative to Conda
Install Python programming language with version 3.4 or greater.

```
https://www.python.org/downloads/
```


## Downlading the repository to your local machine

Step 1. Make sure you are in the master branch in the correct repository
```
https://github.com/txgisci/feature_extractor
```

Step 2. Click the gree drop down option titled 'Clone or download'.

Step 3. Download the zip file, open your command prompt and navigate to the 'feature extractor' repository

## To get the script running:

NOTE: All files are already present in the 'inputs' file. 

The CLI (Command Line Interface) script takes 2 arguments: The name of the feature file you want to read in and the size of the image (small or large)

An example command would be something like:

```
python feature_extractor.py basin.csv small 
```





