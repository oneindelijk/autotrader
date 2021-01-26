
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from .models import Operation, Balance
from plotly.validators.scatter.marker import SymbolValidator
raw_symbols = SymbolValidator().values

def operations_graph_per_balance(balance_id):
    selection = Operation.objects.filter(balance = balance_id)
    balance_currency = Balance.objects.get(id = balance_id).currency.name
    totalcol = 0
    data = [[selection[0].timestamp, 0, 0]]
    for i, o in enumerate(selection):
        datecol = o.timestamp
        amountcol = o.amount * (1 if o.operation_sign else -1)
        totalcol += amountcol
        data.append([datecol, amountcol, totalcol])
    DF = pd.DataFrame(data, columns=['Timestamp','Amount','Sum'])
    DF['Color'] = np.where(DF['Amount']<0, 'red', 'green')
    return create_div_graph(DF, f'Operations for balance {balance_currency}')



def create_div_graph(data, title):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x = data['Timestamp'],
                       y = data['Sum'], 
                       name = 'Total',
                       mode = 'lines+markers',
                       marker_color = 'rgba(55,0,250,.7)',
                       line_color = 'rgba(151, 161, 255, 1)',
                       marker = dict(
                           size = 12,
                           symbol = 219,
                       ),
                       yaxis = 'y1'),
                    secondary_y=True)

    fig.add_trace(go.Bar(x = data['Timestamp'],
                           y = data['Amount'], 
                           name = 'Deposit/Withdrawal',
                           yaxis = 'y2',
                           marker_color = data['Color']),
                secondary_y=False)
    fig.update_layout(title = dict(text = title, 
            font_color = 'white',),
            plot_bgcolor= 'rgba(50, 61, 82, 0)',
            paper_bgcolor = 'rgba(50, 61, 82, 0)',
            legend = dict(font_color = 'white'),
            yaxis = dict(color = 'rgba(50, 200, 5, 1)',
                    gridcolor = 'rgba(50, 200, 5, .3)',
                    zerolinecolor = 'rgba(100, 250, 55, 1)',
                    ),
            yaxis2 = dict(color = 'rgba(151, 161, 255, 1)',
                    gridcolor = 'rgba(101, 111, 252, .6)',
                    zerolinecolor = 'rgba(151, 161, 255, 1)',
                    ),
            xaxis = dict(color = 'rgba(250, 200, 5, 1)',
                    tickformat = '%Y-%b',
                    type = 'category',
                    gridcolor = 'rgba(250, 200, 5, .1)',
                    ),
            showlegend=False,  #TODO  toggle this depending on layout of html page
            )
    
    # plot_div = go.Figure(data = data, layout = layout )
    return plot(fig, output_type='div')