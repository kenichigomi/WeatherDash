"""
API for an interactive weather dashboard
- Kenichi Gomi
"""
from dash import Dash, dcc, html, Input, Output
from API_key import api_key
from weatherAPI import WeatherAPI
import plotly.graph_objects as go
import datetime


def main():
    # init api and get data
    api = WeatherAPI()

    # create layout
    app = Dash(__name__)

    app.layout = html.Div([
            html.H1('Temperature Dashboard'),
            dcc.Graph(id='graph'),

            html.P('Please pick a Location:'),
            dcc.RadioItems(id='city',
                           options=list(api.get_cities().keys()),
                           value='Boston'),

            html.P('Pick a day!'),
            dcc.DatePickerSingle(id='day',
                                 date=datetime.date.today(),
                                 min_date_allowed=datetime.date.today(),
                                 max_date_allowed=(datetime.date.today()+datetime.timedelta(days=5))
            ),


            html.P('Prettify the bars!'),
            dcc.Slider(id='red',
                       min=0,
                       max=255,
                       step=1,
                       value=0,
                       marks=None),
            dcc.Slider(id='green',
                       min=0,
                       max=255,
                       step=1,
                       value=128,
                       marks=None),
            dcc.Slider(id='blue',
                       min=0,
                       max=255,
                       step=1,
                       value=255,
                       marks=None),
    ])

    # define callback
    @app.callback(
        Output('graph', 'figure'),
        Input('city', 'value'),
        Input('day', 'date'),
        Input('red', 'value'),
        Input('green', 'value'),
        Input('blue', 'value')
    )
    def make_graph(city, day, red, green, blue):
        # get info
        lat_long = api.get_cities()[city]
        df = api.get_forecast(lat_long[0], lat_long[1], api_key)

        hours = api.get_hours(df, 'dt_txt', day)

        fig = go.Figure(data=[
            go.Bar(name='Minimum Temperature',
                   y=df['temp_min'],
                   x=hours,
                   marker_color=(f'rgb({red},{green},{blue})')),
            go.Bar(name='Current Temperature',
                   y=df['temp'],
                   x=hours,
                   marker_color=(f'rgb({green},{red},{blue})')),
            go.Bar(name='Maximum Temperature',
                   y=df['temp_max'],
                   x=hours,
                   marker_color=(f'rgb({blue},{green},{red})'))
        ])
        fig.update_layout(barmode='group',
                          title='Current, Minimum, and Maximum Temperature',
                          xaxis_title='Hours (24 hr)',
                          yaxis_title='Temperature (F)')
        return fig

    # run it!
    app.run_server(debug=True)


if __name__ == "__main__":
    main()