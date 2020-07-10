import pandas as pd

"""
The assumption for this code is that the data used to make these predictions were
all up to the same date. 
"""

def read_predictions(filepath):
    """
    Reads a csv file of predictions where stocks are column names
    and the number of rows is the number of days predicted ahead.
    :return: A Pandas DataFrame and the date found in the filepath name as a date object
    """
    pass

def valid_passed_days(date,days=10):
    """
    Takes a date of when the predictions where made and determine if
    days # of  records since have been created.It will first check the
    csv file and afterwards if not found, update the data. Use the index
    of the date in the data to count the # of columns
    :return: boolean
    """

def score_predictions(df:pd.DataFrame,days=10):
    """
    Takes a dataframe of predictions for multiple stocks and returns
    a dictionary of the stock and the average accuracy for the stock
    for the specified period of time. It checks if enough days have passed
    before scoring that number of days.
    :param days:
    :return: A dictionary of stocks and accuracies(regressional).
    """
    pass # Use dict_to_csv to save results.

