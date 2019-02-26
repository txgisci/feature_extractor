# Personal Image Query Download

## 1. Navigate to the “Gateway to Astronaut Photography of Earth” and Perform Query
  •	URL: https://eol.jsc.nasa.gov/
  
  •> Search Photos
  
  •	Search for images by geographical features, specific region, or NASA Photo ID
  
  •	Submit query

## 2. TSV Download
  •	Navigate to the bottom of the page containing your query results and click “Download a TSV (tab-separated value) text file for these photos”

  •	Open downloaded TSV file in Microsoft Excel

## 3. Data Manipulation
  •	Delete all of the data except for the first three columns (mission, roll, and frame)
  
  •	Use the following algorithm in the second cell of the fourth column to combine the first three columns:        
  ```
  =CONCATENATE(TRIM(A2), "-", TRIM(B2), "-", TRIM(C2))
  ```
  Note: The first three columns need to be grouped into a single column in order to make the feature_extractor python script run properly.    “Concatenate” groups the first three cells in a row while “trim” gets rid of any extra spaces. Finally, the photo ID must have dashes     (-) between each value.
  
  •	Once a new cell is generated click the small square at the bottom right of the cell which copies the algorithm to each cell in the        column
  
  •	Paste the new column as “Paste as Values” (Excel command to unlink new column from first three)
  
  •	Delete the first three columns and rename your remaining column “Photo ID”
  
  •	Name the second column “Feature” and fill in the first cell of that column with your feature name (i.e. Crater, San Antonio, or Lake)     followed by clicking the bottom right square of the cell to copy that feature name to the rest of the column

## 4. Final Steps
  •	Save your new Excel file as a CSV into your inputs folder used in the feature_extractor python script
  
  •	Run feature_extractor python script with the following command in command prompt: 
  ```
  python feature_extractor.py basin.csv
  ```
  Note: Substitute your queried feature name for “basin.” 
  
  •	Navigate to your outputs folder to view downloaded images from your personal image query!

