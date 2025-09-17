import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Dashboard Carros Usados", layout="wide")
df=pd.read_csv(r"Carros Usados.csv")
df.head()

st.title("🚗 Dashboard Carros Usados")
st.markdown(
    """<hr style="border:2px solid #900ACA; border-radius:5px;">""",
    unsafe_allow_html=True
)
if st.button("Predição de Preço por Carro"):
    js = "window.open('https://luisturra-carros-usados-dashboard-pr-prediostreamlit-app-69dct0.streamlit.app/', '_blank')"  
    components.html(f"<script>{js}</script>", height=0)
st.markdown(
    """<hr style="border:2px solid #900ACA; border-radius:5px;">""",
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Carros", len(df))
with col2:
    st.metric("Média de Preço", f"${df['price'].mean():,.0f}")
with col3:
    st.metric("Média de Quilometragem ", f"{df['mileage'].mean():,.0f} km")

st.markdown(
    """<hr style="border:2px solid #900ACA; border-radius:5px;">""",
    unsafe_allow_html=True
)

montadora_media_preco = df.groupby("make", as_index=False)["price"].mean()
montadora_media_preco=montadora_media_preco.sort_values("price", ascending=False)
ano_media_preco = df.groupby("year", as_index=False)["price"].mean()
fuel_price = df.groupby("fuel_type")["price"].sum()
seller_price = df.groupby("seller_type")["price"].sum()
country_avg = df.groupby('country').agg({'price': 'mean'}).reset_index()

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(
    montadora_media_preco,
    x="make",
    y="price",
    color_discrete_sequence=["#900ACA"] 
)


    max_price = montadora_media_preco['price'].max()
    min_price = montadora_media_preco['price'].min()

    step = (max_price - min_price) / 3  
    tick_vals = np.arange(0, max_price + step, step).round(2)
    if len(tick_vals) < 5:  
        step = (max_price - min_price) / 5
        tick_vals = np.arange(0, max_price + step, step).round(2)


    fig.update_layout(
        title={
            'text': "Preço Médio por Marca",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'family': 'Arial', 'color': 'white'}
        },
        xaxis_title=None,
        yaxis_title=None,
        xaxis_title_font={'size': 14, 'color': '#FFFFFF'},
        yaxis_title_font={'size': 14, 'color': '#FFFFFF'},
        xaxis_tickfont={'size': 12, 'color': '#E0E0E0'},
        yaxis_tickfont={'size': 12, 'color': '#E0E0E0'},
        xaxis_tickangle=45, 
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)', 
        margin=dict(l=50, r=50, t=80, b=100), 
        yaxis_showgrid=False 
    )


    fig.update_yaxes(
        tickprefix="$",
        tickformat=",d", 
        tickfont=dict(color='#E0E0E0'),
        tickvals=tick_vals, 
        range=[0, max_price * 1.1] 
    )

    
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Preço Médio: $%{y:,.0f}<extra></extra>",
        marker_line_color='#FFFFFF',
        marker_line_width=0.8,  
        opacity=0.9,
        width=0.8   
    )



    #fig.show()


    st.plotly_chart(fig,use_container_width=True)
with col2:
    fig = px.bar(
    ano_media_preco,
    x="year",
    y="price",
      
    color_discrete_sequence=['#900ACA'],  
)


    max_price = ano_media_preco['price'].max()
    min_price = ano_media_preco['price'].min()
    step = (max_price - min_price) / 4  
    tick_vals = np.arange(0, max_price + step, step).round(2)
    if len(tick_vals) < 5:  
        step = (max_price - min_price) / 5
        tick_vals = np.arange(0, max_price + step, step).round(2)


    fig.update_layout(
        title={
            'text': "Preço Médio por Ano",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'family': 'Arial', 'color': 'white'}  
        },
        xaxis_title=None,
        yaxis_title=None,
        xaxis_title_font={'size': 14, 'color': '#FFFFFF'}, 
        yaxis_title_font={'size': 14, 'color': '#FFFFFF'}, 
        xaxis_tickfont={'size': 12, 'color': '#E0E0E0'}, 
        yaxis_tickfont={'size': 12, 'color': '#E0E0E0'},  
        xaxis_tickangle=45,  
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_showgrid=False, 
        margin=dict(l=50, r=50, t=80, b=100)
        
    )


    fig.update_yaxes(
        tickprefix="$",
        tickformat=",d",
        tickfont=dict(color='#E0E0E0'),
        tickvals=tick_vals, 
        range=[0, max_price * 1.1] 
    )



    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Preço Médio: $%{y:,.0f}<extra></extra>",
        marker_line_color='#FFFFFF', 
        marker_line_width=0.8, 
        opacity=0.9 
    )




    #fig.show()


    st.plotly_chart(fig,use_container_width=True)
st.markdown(
    """<hr style="border:2px solid #900ACA; border-radius:5px;">""",
    unsafe_allow_html=True
)
col3, col4,col5 = st.columns(3)    
with col3:
    fig = go.Figure(data=[
    go.Pie(
        labels=fuel_price.index,
        values=fuel_price.values,
        textinfo='percent+label', 
        textfont=dict(size=12, color='#FFFFFF'), 
        marker=dict(
            colors=px.colors.sequential.Plasma, 
            line=dict(color='#FFFFFF', width=0.8) 
        ),
        hovertemplate="<b>%{label}</b><br>Preço Total: $%{value:,.0f}<br>Proporção: %{percent}<extra></extra>",
        opacity=0.9 
    )
])


    fig.update_layout(
        title={
            'text': "Porcentagem Tipo de Combustível",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'family': 'Arial', 'color': 'white'}  
        },
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        margin=dict(l=50, r=50, t=80, b=50)  
    )


    #fig.show()


    st.plotly_chart(fig, use_container_width=True)
with col4:
    fig = go.Figure(data=[
    go.Pie(
        labels=seller_price.index,
        values=seller_price.values,
        textinfo='percent+label',
        textfont=dict(size=12, color='#FFFFFF'), 
        marker=dict(
            colors=px.colors.sequential.Plasma, 
            line=dict(color='#FFFFFF', width=0.8) 
        ),
        hovertemplate="<b>%{label}</b><br>Preço Total: $%{value:,.0f}<br>Proporção: %{percent}<extra></extra>",
        opacity=0.9 
    )
])


    fig.update_layout(
        title={
            'text': "Porcentagem por Tipo de Venda",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'family': 'Arial', 'color': 'white'} 
        },
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        margin=dict(l=50, r=50, t=80, b=50) 
    )


    #fig.show()


    st.plotly_chart(fig, use_container_width=True)
with col5:
    feature_cols = df.columns[15:]  
    df[feature_cols] = df[feature_cols].astype(bool)

   
    feature_counts = df[feature_cols].sum().sort_values(ascending=False)
    avg_price_features = {
    col: df.loc[df[col], "price"].mean() 
    for col in feature_cols
}
    avg_price_features = pd.Series(avg_price_features).sort_values(ascending=True)


    fig = go.Figure(data=[
        go.Bar(
            x=avg_price_features.values,
            y=avg_price_features.index,
            orientation='h',  
            marker=dict(
                color='#800080',  
                line=dict(color='#FFFFFF', width=0.8)  
            ),
            text=[f'${int(x):,}' for x in avg_price_features.values],  
            textposition='auto',  
            textfont=dict(size=12, color='#FFFFFF'),  
            opacity=0.9,  
            hovertemplate="<b>%{y}</b><br>Média de Preço: $%{x:,.0f}<extra></extra>"
        )
    ])


    max_price = avg_price_features.max()
    min_price = avg_price_features.min()
    step = (max_price - min_price) / 4  
    tick_vals = np.arange(0, max_price + step, step).round(2)
    if len(tick_vals) < 5:
        step = (max_price - min_price) / 5
        tick_vals = np.arange(0, max_price + step, step).round(2)

    fig.update_xaxes(
        title=None,
        showticklabels=False
    )
    fig.update_layout(
        title={
            'text': "Média de Preço por Características",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'family': 'Arial', 'color': 'white'} 
        },
        xaxis_title=None,
        yaxis_title=None,
        xaxis_title_font={'size': 14, 'color': '#FFFFFF'}, 
        yaxis_title_font={'size': 14, 'color': '#FFFFFF'}, 
        xaxis_tickfont={'size': 12, 'color': '#E0E0E0'}, 
        yaxis_tickfont={'size': 12, 'color': '#E0E0E0'},  
        xaxis=dict(
            tickprefix="$",
            tickformat=",d",
            tickvals=tick_vals,
            range=[0, max_price * 1.1], 
            showgrid=False 
        ),
        yaxis=dict(
            showgrid=False 
        ),
        showlegend=False, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=100, r=50, t=80, b=50) 
    )


    #fig.show()


    st.plotly_chart(fig, use_container_width=True)
    
st.markdown(
    """<hr style="border:2px solid #900ACA; border-radius:5px;">""",
    unsafe_allow_html=True
)    
fig = px.choropleth(
    country_avg,
    locations='country',
    locationmode='country names',
    color='price',
    color_continuous_scale='Plasma',  
    title='Média de Preço dos Carros por País',
    labels={'price': 'Média de Preço (USD)'},
    hover_data={'price': ':,.0f'},  
)


fig.update_layout(
    title={
        'text': "Média de Preço dos Carros por País",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20, 'family': 'Arial', 'color': 'white'}  
    },
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor='white',  
        projection_type='equirectangular',
        bgcolor='rgba(0,0,0,0)', 
        showland=True,
        landcolor='rgba(50,50,50,0.2)', 
    ),
    coloraxis_colorbar=dict(
        title='Média de Preço (USD)',
        titlefont={'size': 14, 'color': '#FFFFFF'},  
        tickfont={'size': 12, 'color': '#E0E0E0'}, 
        tickprefix='$', 
        tickformat=',.0f', 
        bgcolor='rgba(0,0,0,0)', 
        titlefont_color='#FFFFFF',
        tickcolor='#FFFFFF',
       tickvals=[country_avg['price'].min(), country_avg['price'].max()] 
    ),
    paper_bgcolor='rgba(0,0,0,0)',  
    plot_bgcolor='rgba(0,0,0,0)', 
    font=dict(color='#FFFFFF', family='Arial', size=12), 
    margin=dict(l=20, r=10, t=50, b=50),  
    showlegend=False,  
)


fig.update_traces(
    hovertemplate="<b>%{location}</b><br>Média de Preço: $%{z:,.0f}<extra></extra>"
)


#fig.show()


st.plotly_chart(fig, use_container_width=True)