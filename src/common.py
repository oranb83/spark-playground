import os
import re
import logging

import pyspark
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import hour, to_date

from src.events import Events
from src.visualization import Visualization
from src.outputs import Outputs, CSV, CSV_PARTITION_COLUMNS

logger = logging.getLogger(__name__)


def get_session():
    """
    This method return a default spark session.

    @return: spark session.
    """
    return SparkSession.builder.config(conf=SparkConf()).getOrCreate()


def is_valid_directory(directory, filename_suffix="\.json\.*.*$"):
    """
    The directory is either missing or empty.

    @type directory: str
    @param directory: os directory
    @type filename_suffix: str
    @param filename_suffix: csv / json or any other string
    @rtype: bool
    @return: True if directory exist with json files
    """
    if not os.path.isdir(directory):
        return False

    r1 = re.compile(filename_suffix)
    for f in os.listdir(directory):
        if r1.search(f):
            return True

    return False


class Runnable(object):
    """
    This class gets the user input and creates a valid output.
    """
    def __init__(self, args):
        self.input = args.input
        self.debug = args.debug
        self.output = args.output
        self.column = args.column
        self.values = args.values
        self.graph = args.graph

    def run(self):
        """
        Main method.
        """
        if not is_valid_directory(self.input):
            raise RuntimeError("The input directory is missing")

        spark = get_session()
        # TODO: to support other output types a stategy pattern should be implemented
        #       based on the directory files and the correct type should be choosen via code.
        df = spark.read.json(self.input)

        df = Events(df).filter_column(self.column, self.values)
        count = df.count()
        if count == 0:
            logger.info("No Data!")

        # Partitioning column - this means that each day will have it's own graph.
        # TOOD: Consider differerent partitioning per graph - for example scatter graph
        df = df.withColumn(CSV_PARTITION_COLUMNS, to_date(df.created_at, "yyyy-MM-dd"))

        # Datetime
        df = df.withColumn("hour", hour(df.created_at))

        df.createOrReplaceTempView("events")
        # Note: we don't need the events_percentage since any relevant chart (like pie) does the math on it's on.
        #       however, it is possible that this will be required for other future calculations that are better
        #       kept in the output file instead of calculating them upon request later on.
        df_results = spark.sql(
            """
            SELECT date, hour, count(hour) as events, count(hour)*100/{} AS `events_percentage`
            FROM events GROUP BY date, hour order by date, hour
            """.format(count)
        )

        # Show the results for debugging
        if self.debug:
            df_results.show(df_results.count(), truncate=False)

        # TODO: if this operation becomes slow we can run it in a different process
        #       with the multiprocess lib
        Outputs(df_results, self.output).output_type(CSV)

        self.display_graph(df_results)

    def display_graph(self, df):
        """
        Display a supported graph.

        @param df: Spark dataframe
        @raises: UnsupportedChartError
        """
        if not self.graph:
            return

        graph = Visualization(df.toPandas()).choose_graph(self.graph)
