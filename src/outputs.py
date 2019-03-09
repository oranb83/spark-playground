CSV = "csv"
CSV_PARTITION_COLUMNS = "date"


class Outputs(object):

    def __init__(self, df, output_folder):
        self.df = df
        self.output = output_folder

    def output_type(self, _type):
        """
        Strategy pattern in case we will have additional output types.

        @type _type: str
        @param _type: type of graph
        """
        if _type == CSV:
            return self.write_data_to_csv()

        raise ValueError("CSV output is the only supported type for the moment")

    def write_data_to_csv(self):
        """
        Output as CSV.
        """
        # Write data as csv
        self.df.coalesce(1).write.partitionBy(CSV_PARTITION_COLUMNS).mode(
            "overwrite").csv(self.output, header=True)
