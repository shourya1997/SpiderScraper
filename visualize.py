import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import pandas as pd
import crux
import dash_table


# def urlsparsed():
#     sql_parsedUrl = "SELECT * FROM parsedUrls WHERE parsed=True"
#     df = pd.read_sql(sql_parsedUrl, sql_conn)
#     return df
# def urlnotparsed():
#     sql_parsedUrl = "SELECT * FROM parsedUrls WHERE parsed=False"
#     df = pd.read_sql(sql_parsedUrl, sql_conn)
#     return df
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

name_title = 'Stats from mySQL Server'
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Parsed'),
    dcc.Graph(id='example-graph'),
    dcc.Interval(id='graph-update',interval=1*1000,n_intervals=0)])

@app.callback(Output('example-graph', 'figure'),
            [Input('graph-update', 'n_intervals')])
def update_graph_bar(n):

    cursor, sql_conn = crux.getDbConnection()     
    # This works
    df_parsed = pd.read_sql('select parsed,count(parsed) from parsedUrls where parsed=1 group by parsed', sql_conn)
    df_not_parsed = pd.read_sql('select parsed,count(parsed) from parsedUrls where parsed=0 group by parsed', sql_conn)

    trace1 = go.Bar(
        x = list(df_parsed['parsed']),
        y = list(df_parsed['count(parsed)']),
        name='Parsed'
    )
    trace2 = go.Bar(
        x = list(df_not_parsed['parsed']),
        y = list(df_not_parsed['count(parsed)']),
        name='Not Parsed'
    )
    data = [trace1,trace2]
    layout = go.Layout(barmode='group')


    '''
    trace2 = go.Scatter(
                    x = df.world_rank,
                    y = df.teaching,
                    mode = "lines+markers",
                    name = "teaching",
                    marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
                    text= df.university_name)
    '''
    return {'data':data, 'layout':layout}


    # dataSQL = [] #set an empty list
    # dataSQLL = []
    # X = deque(maxlen=10) 
    # Y = deque(maxlen=1000)
    # X_ = deque(maxlen=10)
    # Y_ = deque(maxlen=100)
    # # data = ['parsed','notparsed']

    
    # cursor.execute("select parsed,count(parsed) from parsedUrls where parsed=1 group by parsed")
    # rows = cursor.fetchall()
    # for row in rows:
    #     dataSQL.append(list(row))
    #     labels = ['parsed','count(parsed)']
    #     df = pd.DataFrame.from_records(dataSQL, columns=labels)
    #     X = df['parsed']
    #     Y = df['count(parsed)']

    # cursor.execute("select parsed,count(parsed) from parsedUrls where parsed=0 group by parsed")
    # rowss = cursor.fetchall()
    # for col in rowss:
    #     dataSQLL.append(list(col))
    #     labels = ['parsed','count(parsed)']
    #     dff = pd.DataFrame.from_records(dataSQLL, columns=labels)
    #     X_ = dff['parsed']
    #     Y_ = dff['count(parsed)']
    
    # # trace1 = {
    # #         'x': list(X),
    # #         'y': list(Y),
    # #         'name': 'Parsed',
    # #         'type': 'bar',
    # #         'textposition':'auto'
    # #         }
    # # trace2 = {
    # #         'x': list(X_),
    # #         'y': list(Y_),
    # #         'name': 'Not Parsed',
    # #         'type': 'bar',
    # #         'textposition':'auto'
    # #         }

    # trace1 = go.Bar(
    #         x= list(X),
    #         y= list(Y),
    #         name= 'Parsed',
    #         textposition='auto'
    #         )
    # trace2 = go.Bar(
    #         x= list(X_),
    #         y= list(Y_),
    #         name= 'Not Parsed',
    #         textposition='auto'
    #         )

    # data = [trace1, trace2]
    # layout = dict(
    #         xaxis=dict(title= 'Not Parsed and Parsed'),
    #         yaxis=dict(title= 'Number of URLs'),
    #         barmode='group'
    #         )

    # # data_y = [X,Y]
    # # print(X[0])
    # # print(Y[0])

    # # data = go.Bar(
    # #          x=list(X),
    # #          y=list(Y),
    # #          name='Parsed Amount',
    # #          marker = dict(color = 'rgba(255, 174, 255, 0.5)',
    # #                          line=dict(color='rgb(0,0,0)',width=1.5)))
    # # fig = go.Figure(data=data, layout=layout)

    # # return 
    # return {'data':data, 'layout':go.Layout(layout)}

if __name__ == '__main__':
    app.run_server(debug=True)