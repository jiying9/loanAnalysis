import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from Helper import *
from Loan import *
from LoanImpacts import *
from LoanPortfolio import *

loans = LoanPortfolio()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H6("Input your loan information here:"),
    html.Div(["principal: ",
              dcc.Input(id='principal', value='', type='text')]),
    html.Div(["payment: ",
              dcc.Input(id='payment', value='', type='text')]),
    html.Div(["rate: ",
              dcc.Input(id='rate', value='', type='text')]),
    html.Div(["extra_payment: ",
              dcc.Input(id='extra_payment', value=' ', type='text')]),
    html.Div(["contributor1: ",
              dcc.Input(id='contribute1', value=' ', type='text')]),
    html.Div(["contributor2: ",
              dcc.Input(id='contribute2', value=' ', type='text')]),
    html.Div(["contributor3: ",
              dcc.Input(id='contribute3', value=' ', type='text')]),
    html.Br(),
    html.Button('add a loan', id='btn-nclicks-1', n_clicks=0),
    html.Button('clear all', id='btn-nclicks-2', n_clicks=0),
    html.Button('LoanImpacts', id='btn-nclicks-3', n_clicks=0),
    html.Div(id='loansTable')
])


@app.callback(
    Output(component_id='loansTable', component_property='children'),
    Input(component_id='principal', component_property='value'),
    Input(component_id='payment', component_property='value'),
    Input(component_id='rate', component_property='value'),
    Input(component_id='extra_payment', component_property='value'),
    Input(component_id='contribute1', component_property='value'),
    Input(component_id='contribute2', component_property='value'),
    Input(component_id='contribute3', component_property='value'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks')
)
def update_output_div(principal, payment, rate, extra_payment, c1, c2, c3, btn1, btn2, bt3):
    global loans
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        loan = None
        try:
            loan = Loan(principal=float(principal), rate=float(rate), payment=float(payment),
                        extra_payment=float(extra_payment))
            loan.check_loan_parameters()
            loan.compute_schedule()
        except ValueError as ex:
            print(ex)

        loans.add_loan(loan)
        msg = 'add loan success'
        loans.aggregate()
#        msg = re.sub('\r\n', '<br>', str(Helper.print(loans)))
        return html.Div([
            html.H5('Current loan: '),
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in ['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment',
                                                      'Applied Principal', 'Applied Interest', 'End Principal']])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(Helper.display(float(pay[i]))) for i in range(7)
                    ]) for pay in loan.schedule.values()])
            ]),
            dcc.Graph(figure=Helper.getimg(loan)),
            html.H5('ALL loans: '),
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in ['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment',
                                                      'Applied Principal', 'Applied Interest', 'End Principal']])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(Helper.display(float(pay[i]))) for i in range(7)
                    ]) for pay in loans.schedule.values()])
            ]),
            dcc.Graph(figure=Helper.getimg(loans))
        ])
    elif 'btn-nclicks-2' in changed_id:
        loans = LoanPortfolio()
        msg = 'clear success'
    elif 'btn-nclicks-3' in changed_id:
        loan_impacts = LoanImpacts(principal=float(principal), rate=float(rate), payment=float(payment),
                            extra_payment=float(extra_payment), contributions=[float(c1), float(c2), float(c3)])
        impdata = loan_impacts.compute_impacts()
        return html.Div([
            html.H5('Loan impact: '),
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in ['Index', 'InterestPaid', 'Duration', 'MIInterest', 'MIDuration']])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(pay[i]) for i in range(5)
                    ]) for pay in impdata])
            ])
            ])
    else:
        msg = 'None of the buttons have been clicked yet'

    return 'Output: {}'.format(msg)




if __name__ == '__main__':
    app.run_server(debug=True)