import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import pickle

#style frontend
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#wczytanie oczyszczonego datasetu
df = pd.read_csv('df_cleaned.csv', index_col=0)

#załadowanie zapisanego uprzednio modelu
with open('model4.pickle', 'rb') as file:
    model4 = pickle.load(file)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Img(src='assets/baner_top.jpg', width='1910px'),
        html.H2('Predykcja Cen Samochodów Używanych'),
        html.H4('Regresyjny model uczenia maszynowego')
    ],style={'textAlign': 'center'}),
    html.Hr(),
    #sekcja z wyborem komponentów
    html.Div([
        #pierwszy slider
        html.Label('Wybierz rok produkcji samochodu:'),
        dcc.Slider(
            id='slider-1',
            min=df.Production_year.min(),
            max=df.Production_year.max(),
            step=1,
            marks={i: str(i) for i in range(df.Production_year.min(),df.Production_year.max() + 1,5)},
            tooltip={'placement': 'bottom'}
        ),
        html.Hr(),
        #drugi slider
        html.Label('Wybierz moc silnika:'),
        dcc.Slider(
            id='slider-2',
            min=30,
            max=1300,
            #min=df.Power_HP.min(),
            #max=df.Power_HP.max(),
            step=1,
            marks={i: str(i) for i in range(30, 1301, 50)},
            #marks={i: str(i) for i in range(int(df.Power_HP.min()),int(df.Power_HP.max()),80)},
            tooltip={'placement': 'bottom'}
        ),
        html.Hr(),
        #trzeci slider
        html.Label('Wybierz pojemność skokową:'),
        dcc.Slider(
            id='slider-3',
            min=0,
            max=8500,
            #min=df.Displacement_cm3.min(),
            #max=df.Displacement_cm3.max(),
            step=1,
            marks={i: str(i) for i in range(0, 8501, 500)},
            tooltip={'placement': 'bottom'}
        ),
        html.Hr(),
        #czwarty slider
        html.Label('Wybierz przebieg:'),
        dcc.Slider(
            id='slider-4',
            min=0,
            max=600_000,
            #min=df.Mileage_km.min(),
            #max=df.Mileage_km.max(),
            step=1,
            marks={i: str(i) for i in range(0, 600_001, 50_000)},
            #marks={i: str(i) for i in range(int(df.Mileage_km.min()), int(df.Mileage_km.max())+1, 50000)},
            tooltip={'placement': 'bottom'}
        ),
        html.Br(),
        #pięć rozwijana lista
        html.Label('Rodzaj paliwa:'),
        html.Div([
            dcc.Dropdown(
                id='dropdown-1',
                options=[{'label': i, 'value': j} for i,j in zip(['Diesel', 'Benzyna', 'CNG','LPG','Hybrid' ],
                                                                 ['Diesel', 'Gasoline', 'Gasoline + CNG','Gasoline + LPG','Hybrid'])]
            )
        ], style={'width': '10%', 'textAlign': 'left'}),

        html.Br(),
        #sześć rozwijana lista
        html.Label('Liczba drzwi:'),
        html.Div([
            dcc.Dropdown(
                id='dropdown-2',
                options=[{'label': i, 'value': i} for i in [2,3,4,5,6]]

            )
        ], style={'width': '10%', 'textAlign': 'left'}),
        html.Br(),
        #siedem rozwijana lista
        html.Label('Skrzynia biegów:'),
        html.Div([
            dcc.RadioItems(
                id='radio-1',
                options=[{'label': i, 'value': j} for i,j in zip (['Manualna', 'Automatyczna'],
                                                                  ['Manual', 'Automatic'])]
            )
        ], style={'width': '10%', 'textAlign': 'left'}),

        #sekcja wynikowa
        html.Div([
            html.Hr(),
            html.H3('Predykcja na podstawie modelu'),
            html.Hr(),
            html.H4('Wybrałeś następujące parametry:'),
            html.Div(id='div-1'),
            html.Div(id='div-2'),
            html.Hr()
        ], style={'margin': '0 auto', 'textAlign': 'center'})


    ], style={'width': '90%', 'textAlign': 'left', 'margin': '0 auto' , 'fontSize': 20,
              'background-color': 'white', 'padding': '30px' }),
html.Img(src='assets/baner_bottom.jpg')
],style={'background-color': '#e9ecef'})#tło

#funkcje interaktywne

#słownik do zmapowania wartości ANG-PL
Fuel_type = {'Diesel': 'Diesel','Gasoline': 'Benzyna', 'Gasoline + CNG': 'CNG','Gasoline + LPG': 'LPG','Hybrid': 'Hybrid'}
Transmission_Manual = {'Manual': 'Manualna', 'Automatic': 'Automatyczna'}
#dekorator
@app.callback(
    Output('div-1', 'children'),
    [Input('slider-1', 'value'),
    Input('slider-2', 'value'),
    Input('slider-3', 'value'),
    Input('slider-4', 'value'),
    Input('dropdown-1', 'value'),
    Input('dropdown-2', 'value'),
    Input('radio-1', 'value')]
)
#pozwoli wyświetlić na stronie wybrane przez użytkownika parametry
def display_parameters(val1,val2,val3,val4,val5,val6,val7):

    #instrukcja warunkowa jeśli nie wszystkie parametry zostaną wybrane
    if val1 and val2 and val3 and val4 and val5 and val6 and val7:
        val5 = Fuel_type[val5] #złapie wybraną wartość i zamieni na PL wg zmapowania
        val7 = Transmission_Manual[val7]
        return html.Div([
            html.H6(f'Rok produkcji: {val1} r.'),
            html.H6(f'Moc silnika: {val2} km'),
            html.H6(f'Pojemność silnika: {val3} cm3'),
            html.H6(f'Przebieg: {val4} kilometrów'),
            html.H6(f'Rodzaj paliwa: {val5}'),
            html.H6(f'Liczba drzwi: {val6}'),
            html.H6(f'Skrzynia biegów: {val7}'),
        ],style={'textAlign': 'left'})
    else:
        return html.Div([
            html.H4('Podaj wszystkie parametry !')
        ])

# drugi callback
#element do przewidywania ceny

@app.callback(
    Output('div-2', 'children'),
    [Input('slider-1', 'value'),
    Input('slider-2', 'value'),
    Input('slider-3', 'value'),
    Input('slider-4', 'value'),
    Input('dropdown-1', 'value'),
    Input('dropdown-2', 'value'),
    Input('radio-1', 'value')]
)
#predykcja
def predict_value(val1,val2,val3,val4,val5,val6,val7):

    #instrukcja warunkowa jeśli nie wszystkie parametry zostaną wybrane
    if val1 and val2 and val3 and val4 and val5 and val6 and val7:

        val5_1, val5_2, val5_3, val5_4 = 0, 0, 0, 0

        if val5 == 'Gasoline':
            val5_1 = 1
        elif val5 == 'Gasoline + CNG':
            val5_2 = 1
        elif val5 == 'Gasoline + LPG':
            val5_3 = 1
        elif val5 == 'Hybrid':
            val5_4 = 1

        if val7 == 'Manual':
            val7 = 1
        else:
            val7 = 0

        df_sample = pd.DataFrame(
            data= [
                [val1,val2,val3,val4,val5_1, val5_2, val5_3, val5_4,val6,val7]
            ],
            columns= ['Production_year', 'Mileage_km', 'Power_HP', 'Displacement_cm3', 'Doors_number', 'Fuel_type_Gasoline',
            'Fuel_type_Gasoline + CNG', 'Fuel_type_Gasoline + LPG', 'Fuel_type_Hybrid', 'Transmission_Manual']
        )

        print(df_sample)

        #predykcja ceny
        price = model4.predict(df_sample)[0]
        price = round(price/10,2)

        return html.Div([
            html.H4(f'Sugerowana cena pojazdu: {price} PLN')
        ],style={'background-color': '#EA526F', 'width':'30%', 'margin': '0 auto'})


if __name__ == '__main__':
    app.run_server(debug=True , port=8051)
