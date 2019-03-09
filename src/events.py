from pyspark.sql.functions import col

from src.errors import ColumnNameError


class Events(object):
    """
    This class encapsulates basic dataframe operations specific to this task.
    """
    def __init__(self, df):
        self.df = df

    def filter_column(self, column=None, values=[]):
        """
        Filter events from dataframe by column name and it's values.

        @param df: spark dataframe
        @param column: column name in the dataframe
        @type column: str or None
        @return: filtered spark dataframe
        @raises: ColumnNameError
        """
        if column is None:
            return self.df

        columns = self.df.columns
        if column not in columns:
            raise ColumnNameError("Column does not exist in the dataframe!")

        return self.df.filter(col(column).isin(values))
