'''
# Sidebar Filters
st.sidebar.title("Datos para predicción del modelo")
#hospitalizado_filter = st.sidebar.selectbox("Hospitalizado", ["All"] + list(data["HOSPITALIZADO"].unique()))
#departamento_filter = st.sidebar.selectbox("Departamento", ["All"] + list(data["DEPARTAMENTO"].unique()))
tipo_diabetes_filter = st.sidebar.selectbox("Tipo de Diabetes", ["All"] + list(data["TIPO_DIABETES"].unique()))
edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
sexo = st.sidebar.selectbox("Sexo",  list["MASCULINO", "FEMENINO"])
antiguedad_dx = st.number_input("Antigüedad DX", min_value=0, max_value=100, step=1)
dx_obesidad = st.selectbox("Diagnóstico de Obesidad", [0, 1])
dx_hipertension = st.selectbox("Diagnóstico de Hipertensión", [0, 1])
dx_salud_mental = st.selectbox("Diagnóstico de Salud Mental", [0, 1])
#st.sidebar.title("Datos para predicción del modelo")

# Filter Data
filtered_data = data.copy()
if hospitalizado_filter != "All":
    filtered_data = filtered_data[filtered_data["HOSPITALIZADO"] == hospitalizado_filter]
if departamento_filter != "All":
    filtered_data = filtered_data[filtered_data["DEPARTAMENTO"] == departamento_filter]
if tipo_diabetes_filter != "All":
    filtered_data = filtered_data[filtered_data["TIPO_DIABETES"] == tipo_diabetes_filter]

# Main Section: Visualizations
st.title("Visualizations")
st.write("Filtered Data", filtered_data)

st.subheader("Distribution of VALOR_NETO")
sns.barplot(filtered_data["VALOR_NETO"], kde=True)
st.pyplot(plt)'''
st.sidebar.header("Filtros para visualización")
departamentos = sorted(list(df['DEPARTAMENTO'].unique()))
hospitalizado = sorted(list(df['HOSPITALIZADO'].unique()))
ciudades = st.sidebar.multiselect('Seleccionar por departamento', departamentos)
selected_hospitalizado = st.sidebar.multiselect(
    "Seleccionar por hospitalización",hospitalizado, 
    options=[0, 1], 
    format_func=lambda x: "No Hospitalizado" if x == 0 else "Hospitalizado",
    index=0
)
selected_tipo_diabetes = st.sidebar.multiselect(
    "Seleccionar por tipo de diabetes", 
    options=df['TIPO_DIABETES'].unique(), 
    default=df['TIPO_DIABETES'].unique()
)

# Apply filters
filtered_df = df[
    (df['DEPARTAMENTO'].isin(departamentos)) &
    (df['HOSPITALIZADO'] == selected_hospitalizado) &
    (df['TIPO_DIABETES'].isin(selected_tipo_diabetes))
]


# Sidebar filters for visualization
# Mapping dictionaries for display
hospitalizado_mapping = {0: "No Hospitalizado", 1: "Hospitalizado"}
tipo_diabetes_mapping = {
    0: "Diabetes mellitus tipo 1",
    1: "Diabetes mellitus tipo 2"
}
# Get unique values for filtering
departamentos = sorted(list(df['DEPARTAMENTO'].unique()))
hospitalizado_keys = list(hospitalizado_mapping.keys())
hospitalizado_labels = [hospitalizado_mapping[key] for key in hospitalizado_keys]
tipo_diabetes_keys = list(tipo_diabetes_mapping.keys())
tipo_diabetes_labels = [tipo_diabetes_mapping[key] for key in tipo_diabetes_keys]

# Sidebar filters
ciudades = st.sidebar.multiselect('Seleccionar por departamento', departamentos)

selected_hospitalizado_labels = st.sidebar.multiselect(
    "Seleccionar por hospitalización",
    options=hospitalizado_labels
    #default=hospitalizado_labels
)
selected_tipo_diabetes_labels = st.sidebar.multiselect(
    "Seleccionar por tipo de diabetes",
    options=tipo_diabetes_labels
    #default=tipo_diabetes_labels
)

# Convert labels back to values for filtering
selected_hospitalizado = [key for key, label in hospitalizado_mapping.items() if label in selected_hospitalizado_labels]
selected_tipo_diabetes = [key for key, label in tipo_diabetes_mapping.items() if label in selected_tipo_diabetes_labels]

# Apply filters
filtered_df = df[
    (df['DEPARTAMENTO'].isin(ciudades)) &
    (df['HOSPITALIZADO'].isin(selected_hospitalizado)) &
    (df['TIPO_DIABETES'].isin(selected_tipo_diabetes))
]
