import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, dash_table
import os

image_path = os.path.abspath('bg.jpg')

# Carregando dados
arquivo_path = 'C:/Users/Augus/Documents/GitHub/med_vet/a3_inteligencia_artificial/bancodedados.xlsx'
df_original = pd.read_excel(arquivo_path)

# Criando nomes de animais, se não existirem
Animais = []
num = 0
if 'Animais' not in df_original.columns:
    for num in range(1, 34+1):
        animal = 'Animal_' + str(num)
        Animais.append(animal)
    
    df_original['Animais'] = Animais
    df = df_original[['Animais'] + [coluna for coluna in df_original.columns if coluna.lower() != 'animais']]
    df.to_excel('dbVeterinaria.xlsx', index=False)
    
else:
    pass
    
# Inicializando o app Dash
app = Dash(__name__)

# Contagem de diagnósticos
contagem_diagnostico = df['Diagnóstico'].value_counts()

# Dados para o gráfico de contagem de diagnósticos
diagnostico_animal = df

# Opções para o dropdown de diagnósticos por animais
opcoes_diagnostico_animais = list(df['Animais']) 
opcoes_diagnostico_animais.append('Todos os animais')

# Configurando gráfico de contagem de diagnósticos
grafico_contagem_diagnostico = px.bar(
    x=contagem_diagnostico.index,
    y=contagem_diagnostico.values,
    labels={'x': 'Doenças', 'y': 'Contagem por animal'},
)
grafico_contagem_diagnostico.update_traces(
    marker=dict(
        color='blue',
        line=dict(color='white', width=2),
    )
)
grafico_contagem_diagnostico.update_layout(
    paper_bgcolor='white',
    font=dict(size=14),
)
grafico_contagem_diagnostico.update_xaxes(
    title_font=dict(size=20, color='blue'),
    tickfont=dict(color='blue')    
)
grafico_contagem_diagnostico.update_yaxes(
    title_font=dict(size=20, color='blue'),
    tickfont=dict(color='blue')   
)

# Configurando gráfico de dispersão (scatter plot) Hb vs Erit
grafico_scatter_hgb_erit = px.scatter(
    df,
    x='Hemoglobina (g/dL)', 
    y='Eritrócitos (10/µL)',
    labels={'x': 'Hemoglobina', 'y': 'Eritrocitos'}, 
    hover_data={'Diagnóstico': True, 'Animais': True}
)
grafico_scatter_hgb_erit.update_traces(
    marker=dict(
        color='blue',
        line=dict(color='white', width=2),
    )
)
grafico_scatter_hgb_erit.update_layout(
    paper_bgcolor='white',
    font=dict(size=14),
)
grafico_scatter_hgb_erit.update_xaxes(
    title_font=dict(size=20, color='blue'),
    tickfont=dict(color='blue'),
)
grafico_scatter_hgb_erit.update_yaxes(
    title_font=dict(size=20, color='blue'),
    tickfont=dict(color='blue'),
)

# Configurando gráfico de pizza para a composição de diagnósticos
diagnosis_pie_chart = px.pie(df, names='Diagnóstico')
diagnosis_pie_chart.update_traces(
    textinfo='percent+label', 
    insidetextorientation='radial',
    marker=dict(colors=px.colors.qualitative.Plotly)
)
diagnosis_pie_chart.update_layout(
    paper_bgcolor='white',
    font=dict(size=14, color='blue'),
    height=500,  # Ajuste a altura conforme preferência
    width=700, # Ajuste a largura conforme preferência

)

# Configurando gráfico de box plot para a distribuição da Hemoglobina por diagnóstico
box_plot_hemoglobina = px.box(
    df, x='Diagnóstico', y='Hemoglobina (g/dL)',
    labels={'x': 'Diagnóstico', 'y': 'Hemoglobina (g/dL)'},
)
box_plot_hemoglobina.update_traces(
    marker=dict(
        color='blue',
        line=dict(color='white', width=2),
    )
)
box_plot_hemoglobina.update_layout(
    paper_bgcolor='white',
    font=dict(size=14, color='blue'),
)
box_plot_hemoglobina.update_xaxes(
    title_font=dict(size=20, color='blue'),
    tickfont=dict(color='blue'),
)
box_plot_hemoglobina.update_yaxes(
    title_font=dict(size=20, color='blue'),
    tickfont=dict(color='blue'),
)

# Reshape data into long format for stacked bar chart
df_long = df.melt(id_vars=['Animais', 'Diagnóstico'], var_name='Parâmetro', value_name='Valor')

# Configurando gráfico de barras empilhadas para a composição de diagnósticos
stacked_bar_chart = px.bar(
    df_long,
    x='Diagnóstico',
    y='Valor',
    color='Parâmetro',
    labels={'Valor': 'Valor', 'Parâmetro': 'Parâmetro'},
    height=500,  # Ajuste a altura conforme preferência
    width=1340,  # Ajuste a largura conforme preferência
)

stacked_bar_chart.update_traces(
    marker=dict(
        line=dict(color='white', width=1),
    )
)

stacked_bar_chart.update_layout(
    paper_bgcolor='white',
    font=dict(size=14, color='blue'),
    barmode='stack',
    xaxis={'categoryorder': 'total descending'},
)

# Layout do app
# Add your image as the background
# ...

# Layout do app
# Add your image as the background
app.layout = html.Div(style={'backgroundImage': 'url("/assets/bg.jpg")', 'backgroundSize': 'cover', 'backgroundRepeat': 'no-repeat', 'height': '100vh', 'width': '100vw'}, children=[
    html.Link(
        rel='stylesheet',
        href='/assets/style.css'
    ),
    html.H1(children='Dashboard Veterinária', id='titulo_principal'),
    
    # Contagem de diagnósticos
    html.H2(children='Contagem de Diagnósticos', id='h2_count_diagnostic'),
    dcc.Graph(
        id='grafico_contagem_diagnostico',
        figure=grafico_contagem_diagnostico
    ),

    # Gráfico de dispersão
    html.H2("Gráfico de Dispersão: Hemoglobina vs Eritrócitos", id='h2_scatter_hgb_erit'),
    dcc.Graph(
        id='grafico_scatter_hgb_erit',
        figure=grafico_scatter_hgb_erit
    ),

    # Gráfico de pizza de diagnósticos
    html.H2("Composição de Diagnósticos", id='h2_diagnostic_composition'),
    dcc.Graph(
        id='pie-chart-diagnosis-composition',
        figure=diagnosis_pie_chart,
        className='pie-chart-diagnosis-composition'
    ),

    # Grafico de distribuição de hemoglobina por diagnostico
    html.H2("Box Plot: Distribuição da Hemoglobina por Diagnóstico", id='h2_box_plot_hemoglobina'),
    dcc.Graph(
        id='box-plot-hemoglobina',
        figure=box_plot_hemoglobina
    ),

    # Grafico de composição de parametros para diagnostico
    html.H2("Composição de Diagnósticos", id='h2_stacked_bar_chart'),
    dcc.Graph(
        id='stacked-bar-chart-diagnosis-composition',
        figure=stacked_bar_chart,
    ),

    # Diagnóstico por Animal
    html.H2("Diagnóstico por Animal", id='h2_diagnostic_animal'),
    html.Div(id='dropdown', children=[
        dcc.Dropdown(
            options=[{'label': animal, 'value': animal} for animal in opcoes_diagnostico_animais],
            value='Todos os animais', 
            id='drop_diagnostic_animal',
            className='drop-diagnostic_animal',
            clearable=False,
            style={
                'backgroundColor': 'white',
                'color': 'blue',
                'fontSize' : '20px',
                'verticalAlign': 'middle',
                'textAlign': 'center'
            }
        ),
    ]),

    # Tabela de diagnósticos por animal
    html.Div(id='texto_diagnostico_animal'),
    dash_table.DataTable(
        id='table_diagnostic_animal',
        columns=[{'name': col, 'id': col} for col in diagnostico_animal.columns], 
        data=diagnostico_animal.to_dict('records'),
        style_table={
            'height': '300px',
            'overflowY': 'auto',
            
        }, 
        style_cell={
            'minWidth': 110, 'maxWidth': 110, 'width': 110,
            'textAlign': 'center',
            'color': 'blue'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'color': 'blue'
        },
        style_header={
            'whiteSpace': 'normal',
            'color': 'blue'
        }
    )
])

# ...



# Callbacks
@app.callback(
    Output('table_diagnostic_animal', 'data'),
    Input('drop_diagnostic_animal', 'value')
)
def update_outputs(selected_animal):
    if selected_animal == 'Todos os animais':
        filtered_diagnostico_animal = diagnostico_animal
    else:
        filtered_diagnostico_animal = diagnostico_animal[diagnostico_animal['Animais'] == selected_animal]       
    # Atualiza a tabela
    dados_tabela = filtered_diagnostico_animal.to_dict('records')
    return dados_tabela

@app.callback(
    Output('texto_diagnostico_animal', 'children'),
    Input('drop_diagnostic_animal', 'value')
)
def texto_diagnostico_animal(value):
    return f"Você está vendo '{value}'"

# Executa o app
if __name__ == '__main__':
    app.run_server(debug=True)

def texto_diagnostico_animal(value):
    return f"Você está vendo '{value}'"

# Executa o app
if __name__ == '__main__':
    app.run_server(debug=True)
