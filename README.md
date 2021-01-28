# Jupyter Notebooks

* prototype ML solutions
* feature engineering
* share data analysis results
* tutorials, explanations
* plus whatever you come up with

## Get Started
* create a virtualenv
* activate the virtualenv
* install the requirements.text using "pip install -r requirements.text"
  * alternatively install Anaconda from http://www.continuum.io/
* clone this repo
* change to the root of your repo clone
* start the IPython notebook server with "./start_ipython.sh"
* find some amazing patterns in data :)

## Best Practices
* SQL or S3 csv files?
  * SQL for adhoc, re-run the notebook frequently to "monitor" the data
  * S3, csv for reproducable results, re-run the notebook but have a history of data being used, shared results
* for common tasks use the same layout, flow
  * start with imports
  * read the data
  * clean it
  * feature analysis
    * distribution function
    * outliers
  * validation
    * feature reduction, selection
    * model selection
    * estimator performance, over-fitting

## Data
* how to read data with SQL is explained in the example_redshift notebook
* for local or S3 files .. you got the idea

## github
* easy to share
* if the output is left in the ipynb file the notebook can be executed later and then the results can be compared to previous runs
* github.com already renders the notebooks. it has an nbviewer build in.
* github enterprise should soon render them too
