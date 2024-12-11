import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# Load Data and Model
@st.cache_data
def load_data():
    return pd.read_csv("df_limpio.csv")  # Replace with your dataset

# Load Model
@st.cache_resource
def load_model():
    with open("Decision_Tree_Classifier.pkl", "rb") as file:
        return pickle.load(file)
# Load Scaler
with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)
df = load_data()
model = load_model()




# Sidebar filters for visualization
st.sidebar.header("Filtros para visualización")

hospitalizado_mapping = {0: "No Hospitalizado", 1: "Hospitalizado"}
tipo_diabetes_mapping = {
    0: "Diabetes mellitus tipo 1",
    1: "Diabetes mellitus tipo 2"
}

departamentos = sorted(df['DEPARTAMENTO'].unique())
hospitalizado_options = ["No Hospitalizado", "Hospitalizado"]
tipo_diabetes_options = list(tipo_diabetes_mapping.values())

ciudades = st.sidebar.multiselect('Seleccionar por departamento', departamentos)
selected_hospitalizado = st.sidebar.multiselect(
    "Seleccionar por hospitalización", 
    hospitalizado_options, 
    #default=hospitalizado_options
)
selected_tipo_diabetes = st.sidebar.multiselect(
    "Seleccionar por tipo de diabetes", 
    tipo_diabetes_options, 
    #default=tipo_diabetes_options
)

# Apply filters directly on df
filtered_df = df.copy()

if ciudades:
    filtered_df = filtered_df[filtered_df['DEPARTAMENTO'].isin(ciudades)]

if selected_hospitalizado:
    filtered_df = filtered_df[filtered_df['HOSPITALIZADO'].isin(
        [0 if h == "No Hospitalizado" else 1 for h in selected_hospitalizado])]

if selected_tipo_diabetes:
    filtered_df = filtered_df[filtered_df['TIPO_DIABETES'].isin(
        [key for key, value in tipo_diabetes_mapping.items() if value in selected_tipo_diabetes])]

# Sidebar for user input
st.sidebar.header("Información del Paciente")

edad = st.sidebar.number_input("Edad", min_value=0, max_value=120, value=30, step=1)
sexo = st.sidebar.selectbox("Genero", options=["Masculino", "Femenino"])
tipo_diabetes = st.sidebar.selectbox("Tipo de Diabetes", options=["Diabetes mellitus tipo 1", "Diabetes mellitus tipo 2"])
antiguedad_dx = st.sidebar.number_input("Días desde primer diagnóstico", min_value=0, max_value=2555, value=5, step=1)
dx_obesidad = st.sidebar.selectbox("Diagnóstico Obesidad ", options=["Si", "No"])
dx_hipertension = st.sidebar.selectbox("Diagnóstico Hipertension ", options=["Si", "No"])
dx_salud_mental = st.sidebar.selectbox("Diagnóstico Salud Mental", options=["Si", "No"])

# Prepare input data
input_data = pd.DataFrame({
    "EDAD": [edad],
    "SEXO": [1 if sexo == "Femenino" else 0],
    "TIPO_DIABETES": [0 if tipo_diabetes == "Diabetes mellitus tipo 1" else 1], #if tipo_diabetes == "Diabetes mellitus tipo 2"],
    "ANTIGUEDAD_DX": [antiguedad_dx],
    "CON_DX_OBESIDAD": [1 if dx_obesidad == "Si" else 0],
    "CON_DX_HIPERTENSION": [1 if dx_hipertension == "Si" else 0],
    "CON_DX_SALUDMENTAL": [1 if dx_salud_mental == "Si" else 0],
})

# Apply scaler to relevant columns
input_data[['EDAD', 'ANTIGUEDAD_DX']] = scaler.transform(input_data[['EDAD', 'ANTIGUEDAD_DX']])


# Main content
# Visualization Section with Filters

import altair as alt

# Dashboard content
st.title("Dashboard de Visualizaciones")
# Display filtered data (optional)
#st.write("Filtered Data", filtered_df)
# Visualization 1: VALOR_NETO by Ciudad
st.write("VALOR_NETO por Ciudad")
valor_neto_ciudades = (
    filtered_df.groupby('DEPARTAMENTO')['VALOR_NETO'].sum().reset_index().sort_values('VALOR_NETO', ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(data=valor_neto_ciudades, x='VALOR_NETO', y='DEPARTAMENTO', palette='viridis', ax=ax1)
ax1.set_title('VALOR_NETO por Departamento')
ax1.set_xlabel('VALOR_NETO')
ax1.set_ylabel('Departamento')
st.pyplot(fig1)

# Visualization 2: VALOR_NETO by Hospitalización
st.write("VALOR_NETO por Estado de Hospitalización")
valor_neto_hospitalizado = (
    filtered_df.groupby('HOSPITALIZADO')['VALOR_NETO'].sum().reset_index()
)
valor_neto_hospitalizado['Estado'] = valor_neto_hospitalizado['HOSPITALIZADO'].map(hospitalizado_mapping)

fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.barplot(data=valor_neto_hospitalizado, x='VALOR_NETO', y='Estado', palette='coolwarm', ax=ax2)
ax2.set_title('VALOR_NETO por Estado de Hospitalización')
ax2.set_xlabel('VALOR_NETO')
ax2.set_ylabel('Estado de Hospitalización')
st.pyplot(fig2)

# Visualization 3: Hospitalización por Departamento
st.write("Estado de Hospitalización por Departamento")
hospitalizacion_departamento = (
    filtered_df.groupby(['DEPARTAMENTO', 'HOSPITALIZADO']).size().reset_index(name='count')
)
hospitalizacion_departamento['Estado'] = hospitalizacion_departamento['HOSPITALIZADO'].map(hospitalizado_mapping)

chart_hosp_departamento = alt.Chart(hospitalizacion_departamento).mark_bar().encode(
    x=alt.X('count:Q', title='Cantidad'),
    y=alt.Y('DEPARTAMENTO:N', sort='-x'),
    color=alt.Color('Estado:N', scale=alt.Scale(scheme='set1')),
    tooltip=['DEPARTAMENTO', 'Estado', 'count']
).properties(
    width=700,
    height=400,
    title="Estado de Hospitalización por Departamento"
)
st.altair_chart(chart_hosp_departamento)

# Visualization 4: TIPO_DIABETES por Departamento
st.subheader("TIPO_DIABETES por Departamento")
diabetes_departamento = (
    filtered_df.groupby(['DEPARTAMENTO', 'TIPO_DIABETES']).size().reset_index(name='count')
)
diabetes_departamento['Tipo'] = diabetes_departamento['TIPO_DIABETES'].map(tipo_diabetes_mapping)

chart_diabetes_departamento = alt.Chart(diabetes_departamento).mark_bar().encode(
    x=alt.X('count:Q', title='Cantidad'),
    y=alt.Y('DEPARTAMENTO:N', sort='-x'),
    color=alt.Color('Tipo:N', scale=alt.Scale(scheme='set2')),
    tooltip=['DEPARTAMENTO', 'Tipo', 'count']
).properties(
    width=700,
    height=400,
    title="TIPO_DIABETES por Departamento"
)
st.altair_chart(chart_diabetes_departamento)

st.title("Prevención de hospitalización para pacientes de diabetes")
st.write("Proporcione detalles del paciente en la barra lateral para predecir si es probable que sea hospitalizado")

if st.button("Predecir"):
    prediction = model.predict(input_data)[0]
    result = "Hospitalizado" if prediction == 1 else "No sera hospitalizado"
    st.subheader(f"Predicción: {result}")

    # Additional information
    st.write("### Input Data:")
    st.write(input_data)