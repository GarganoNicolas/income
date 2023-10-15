import gradio as gr
import pandas as pd
import pickle
import os

# Define params names
PARAMS_NAME = [
            "edad",
            "sexo",
            "alfabeto",
            "sistema_salud",
            "nivel_educativo",
            "ocupacion_jerarquia"
]

           
# Load model
with open("model/model1.pkl", "rb") as f:
    model = pickle.load(f)




def predict(*args):
    answer_dict = {}

    for i in range(len(PARAMS_NAME)):
        answer_dict[PARAMS_NAME[i]] = [args[i]]

    # Crear dataframe
    single_instance = pd.DataFrame.from_dict(answer_dict)


    data3=single_instance.copy()
    data2=data3
    data2['sexo']=data3['sexo'].replace({'Hombre': 0, 'Mujer': 1})
    data2['alfabeto']=data3['alfabeto'].replace({'Si': 0, 'No': 1})
    replacements = {
        'No paga ni le descuentan': 1,
        'Obra social (incluye PAMI)': 5,
        'Obra social y mutual/prepaga/servicio de emergencia.': 6,
        'Mutual / Prepaga / Servicio de emergencia': 3,
        'Planes y seguros públicos': 2,
        'Ns./Nr.': 0,
        'Mutual/prepaga/servicio de emergencia/ Planes y Seguros Públicos': 4
    }

    # Replace the values in the column
    data2['sistema_salud'] = data3['sistema_salud'].replace(replacements)

    replacements1 = {
        'Superior Universitaria Completa': 6,
        'Primaria Completa': 2,
        'Secundaria Incompleta': 3,
        'Secundaria Completa': 4,
        'Primaria Incompleta(incluye educación especial)': 1,
        'Superior Universitaria Incompleta': 5,
        'Sin instrucción': 0
}

    # Replace the values in the column
    data2['nivel_educativo'] = data3['nivel_educativo'].replace(replacements1)

    replacements2 = {
        'Cuenta propia': 2,
        'Director': 3,
        'otro': 0,
        'Trabajador asalariado': 1
}

    # Replace the values in the column
    data2['ocupacion_jerarquia'] = data3['ocupacion_jerarquia'].replace(replacements2)
    
    
    prediction = model.predict(data2)


    # Cast numpy.int64 to just a int
    result = int(prediction[0])
    dolar2019 = 35
    result = result/dolar2019

    import requests
    url = 'https://dolarapi.com/v1/dolares/blue'

    dolar_response = requests.get(url)
    json_response = dolar_response.json()
    compra_value = json_response['compra']
    result = result*compra_value

    # Adaptación respuesta
    result = int(result)
    result = str(result)
    length = len(result)
    if length > 6:
        first_part = result[:length-6]
        second_part = result[length-6:length-3]
        third_part = result[length-3:]
        result = first_part + '.' + second_part + '.' + third_part

    elif length > 3 < 7:
        first_part = result[:length-3]
        second_part = result[length-3:]
        result = first_part + '.' + second_part

    response = '$\t' + result + '\t\t\t💸'


    return response

css = '''

.gradio-container {
    background-color: #FF000080;
    color: white;
}
.gradio-input {
    background-color: #FF0000;
    color: white;
}
.gradio-output {
    background-color: #FF0000;
    color: white;
}
.gradio-container {
    max-width: 600px;
    margin: auto;
    text-align: center;
}

.gradio-row {
    max-width: 60px;
    margin: auto;
}
.gradio-input-label, .gradio-output-label {
    color: #FFCCCB;
}

img {
    display: block;
    align-items:center;
    margin-left: auto;
    margin-right: auto;
}

'''


with gr.Blocks(css=css) as demo:
    gr.Markdown(
        """
        #   Frente unido de los trabajadores ⚒ 
        """
    )

    with gr.Row():
        with gr.Column():

            gr.Markdown(
                """
                ## Ingrese sus condiciones sociolaborales  🤓
                """
            )
            
            edad = gr.Slider(
                label='Edad',
                minimum=15,
                maximum=86,
                step=1,
                randomize=True
            )

            sexo = gr.Radio(
                label='Genero',
                choices=['Hombre', 'Mujer'],
                value='Hombre',
            )

            alfabeto = gr.Radio(
                label='Alfabeto',
                choices=['Si', 'No'],
                value='Si',
            )

            sistema_salud = gr.Dropdown(
                label='Sistema de Salud',
                choices=['No paga ni le descuentan', 'Obra social (incluye PAMI)', 'Obra social y mutual/prepaga/servicio de emergencia.', 'Mutual / Prepaga / Servicio de emergencia', 'Planes y seguros públicos', 'Ns./Nr.', 'Mutual/prepaga/servicio de emergencia/ Planes y Seguros Públicos'],
                multiselect=False,
                value='No paga ni le descuentan',
            )

            nivel_educativo = gr.Dropdown(
                label='Nivel Educativo',
                choices=['Superior Universitaria Completa', 'Primaria Completa', 'Secundaria Incompleta', 'Secundaria Completa', 'Primaria Incompleta(incluye educación especial)', 'Superior Universitaria Incompleta', 'Sin instrucción'],
                multiselect=False,
                value='Secundaria Completa',
            )

            ocupacion_jerarquia = gr.Dropdown(
                label='Ocupacion Jerarquia',
                choices=['Cuenta propia', 'Director', 'otro', 'Trabajador asalariado'],
                multiselect=False,
                value='Cuenta propia',
            )

        with gr.Column():

            gr.Markdown(
                """
                ## Creemos este es el valor de tu explotacion
                """
            )
            gr.Markdown(
                """
                ## <img src="https://media.giphy.com/media/KESfG6KmWrBss/giphy.gif" alt="GIF">
                """
            )

            label = gr.Label(label="income status")
            predict_btn = gr.Button(value="Hasta la victoria siempre!")
            predict_btn.click(
                predict,
                inputs=[
                    edad,
                    sexo,
                    alfabeto,
                    sistema_salud,
                    nivel_educativo,
                    ocupacion_jerarquia,
                ],
                outputs=[label],
                api_name="prediccion"
            )
            

    gr.Markdown(
        """
        <p style='text-align: center'>
            <a href='https://www.escueladedatosvivos.ai/cursos/bootcamp-de-data-science' 
                target='_blank'>Proyecto demo creado en el bootcamp de EDVAI 🤗
            </a>
        </p>
        """
    )

demo.launch()
