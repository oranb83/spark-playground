import plotly
import plotly.graph_objs as go

from src.errors import UnsupportedChartError


class Visualization(object):
    """
    This class gets pandas dataframe and creates an HTML based on the data.

    TODO: consider working with https://matplotlib.org/
          it was not choosen due to issues with mac os that will require debugging,
          but it's a better lib then the choosen one: https://plot.ly/ that is
          currently running offline mode which is nice for local debugging.
    """
    def __init__(self, pd):
        self.pd = pd

    @classmethod
    def graphs(cls):
        """
        Show All the supported graphs.
        """
        # Reflection: this will produce all the Visualization class method names that are not private
        return [m for m in dir(cls) if m.endswith("_chart")]

    def choose_graph(self, _type):
        """
        Strategy pattern to choose the graph.

        @type _type: str
        @param _type: type of graph
        """
        if _type == "scatter":
            self.scatter_chart()
        elif _type == "pie":
            self.pie_chart()
        else:
            raise UnsupportedChartError(
                "The choosen graph type is not supported! Please choose one of the supported graphs: `{}`".format(self.graphs())
            )

    def scatter_chart(self):
        """
        Scatter chart displaying the amount of events per hour.
        """
        plotly.offline.plot(
            [go.Scatter(x=self.pd.hour, y=self.pd.events)],
            auto_open=True,
            filename="hourly_line_chart"
        )

    def pie_chart(self):
        """
        Pie chart desplaying the amount of events per hour with percentage.
        """
        plotly.offline.plot(
            {
                "data": [go.Pie(values=self.pd.events)],
                "layout": go.Layout(title="Hourly pie chart")
            },
            auto_open=True,
            filename="hourly_pie_chart"
        )
