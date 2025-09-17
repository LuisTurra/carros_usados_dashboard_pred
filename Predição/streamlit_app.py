import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Predição de Preço de Carros Usados", layout="wide")


model = joblib.load('./car_price_model.pkl') 
df = pd.read_csv('Carros Usados.csv')
model_columns = list(model.feature_names_in_)



encoders = {
    'make': joblib.load('make_encoder.pkl'),
    'model': joblib.load('model_encoder.pkl'),
    'trim': joblib.load('trim_encoder.pkl'),
    'body_type': joblib.load('body_type_encoder.pkl'),
    'fuel_type': joblib.load('fuel_type_encoder.pkl'),
    'transmission': joblib.load('transmission_encoder.pkl'),
    'condition': joblib.load('condition_encoder.pkl'),
    'seller_type': joblib.load('seller_type_encoder.pkl'),
    'city': joblib.load('city_encoder.pkl'),
    'state': joblib.load('state_encoder.pkl'),
    'country': joblib.load('country_encoder.pkl')
}

st.title('Predição de Preço de Carros Usados')


if 'inputs' not in st.session_state or st.session_state['inputs'] is None:
    st.session_state['inputs'] = {}
if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None

inputs = st.session_state['inputs']


col1, col2, col3, col_button = st.columns([3,3,3,1])


if col_button.button("Reset"):
    st.session_state['inputs'] = {}
    st.session_state['prediction'] = None

filtered_df = df.copy()


dependent_columns = [
    'make', 'model', 'trim', 'body_type', 'fuel_type',
    'transmission', 'condition', 'seller_type'
]

col_map = {0: col1, 1: col2, 2: col3}

for i, col_name in enumerate(dependent_columns):
    options = sorted(filtered_df[col_name].dropna().unique())
    if col_name in encoders:
        options = [o for o in options if o in encoders[col_name].classes_]
    selected = col_map[i % 3].selectbox(col_name.replace('_', ' ').title(),
                                        options, key=col_name)
    inputs[col_name] = selected
    filtered_df = filtered_df[filtered_df[col_name] == selected]


min_year = int(df['year'].min())
max_year = int(df['year'].max())
inputs['year'] = col1.slider('Year', min_value=min_year, max_value=max_year,
                             value=max_year, step=1)


country_options = sorted(filtered_df['country'].dropna().unique())
inputs['country'] = col1.selectbox('Country', country_options, key='country')

state_options = sorted(df[df['country'] == inputs['country']]['state'].dropna().unique())
inputs['state'] = col2.selectbox('State', state_options, key='state')

city_options = sorted(df[df['state'] == inputs['state']]['city'].dropna().unique())
inputs['city'] = col3.selectbox('City', city_options, key='city')


inputs['mileage'] = st.slider('Mileage', min_value=0, max_value=500000,
                             value=50000, step=1000)


st.header('Additional Features')
checkbox_cols = st.columns(4)
features_list = [
    'Adaptive Cruise Control', 'Alloy Wheels', 'Android Auto', 'Apple CarPlay',
    'Backup Camera', 'Blind Spot Monitor', 'Bluetooth', 'Fog Lights',
    'Heated Seats', 'Keyless Entry', 'LED Headlights', 'Lane Keep Assist',
    'Leather Seats', 'Navigation', 'Panoramic Roof', 'Parking Sensors',
    'Push Button Start', 'Sunroof', 'Ventilated Seats', 'Wireless Charging'
]

for i, feature in enumerate(features_list):
    col = checkbox_cols[i % 4]
    inputs[feature] = 1 if col.checkbox(feature, key=feature) else 0


if st.button('Preço Predição'):
    
    encoded_data = {key: encoders[key].transform([inputs[key]])[0] for key in encoders}

    
    input_data = pd.DataFrame([{**encoded_data,
                                'mileage': inputs['mileage'],
                                **{f: inputs[f] for f in features_list},
                                'year': inputs['year']
                               }])

    
    input_data = input_data[model_columns]

   
    st.session_state['prediction'] = model.predict(input_data)[0]


prediction = st.session_state.get('prediction', None)
if prediction is not None:
    st.markdown(
        f"<h1 style='text-align: center; color: green;'>Predição Preço: ${prediction:,.2f}</h1>",
        unsafe_allow_html=True
    )