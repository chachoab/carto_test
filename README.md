This is my submission to the Data Science position. Here is a brief description of the project structure:

## Notebooks

Notebooks used in exploration. See Report.

## Report

The report can be found at /report. It's basically a merge of the used notebooks.

## ETL

/src/data

 - read_acs_data.py: this script takes care of the demographic ACS data, taking the following steps:
   - Joins with geolocation data.
   - Set median_year_structure_built to null where lower than 1900.
   - Replace null values in all fields with the average of the adjacent blocks.
   - Replace remaining null values with the column average.
 
 - read_ny_data_by_block.py: this script reads the split NYC Taxi dataset one file at a time.
   - First lines where total_amount is negative and trip_distance is zero are discarded.
   - Then the data is joined with the block geolocation.
   - Lines are summarized by number of daily pickups by block
   - Finally the results are merged and the average daily pickups by block are calculated

- prepare_final_dataset.py: this scripts takes the two datasets produced by the previous scripts and joins them. Lines without average pickups data are discarded. This is the final dataset that will be fed to the model

## Model

/src/model

To train and test a model I used the train_test_model script. This script implements the preprocessing, training and testing so I can compare how different algorithms behave. Results and fitted models are stored in the folders of the same name.

### Preprocessing

First standard centering and scaling is performed on the variables to improve the interpretability of the coefficients.

### Train and test sets

Data is split 80/20.

### Searching for hyperparameters

Randomized grid search is used to find the hyperparameters that give the best performance.

### Performance

Some performance metrics are calculated to asses the fit of the tested algorithm:

 - Root Mean Square Error
 - Mean Absolute Error
 - R^2