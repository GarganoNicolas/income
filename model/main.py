from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel


import pickle
import pandas as pd
from fastapi.encoders import jsonable_encoder


app = FastAPI()

with open("model/model1.pkl", "rb") as f:
    model = pickle.load(f)

    
class Answer(BaseModel):
    edad                   : int
    sexo                   : str
    alfabeto               : str
    sistema_salud          : str
    nivel_educativo        : str
    ocupacion_jerarquia    : str
  


@app.get("/")
async def root():
    return {"message": "Proyecto INCOME  - Nicolas Gargano"}


@app.post("/prediccion")
def predict_fraud_customer(answer: Answer):

    answer_dict = jsonable_encoder(answer)
    
    for key, value in answer_dict.items():
        answer_dict[key] = [value]
    
    # Crear dataframe
    single_instance = pd.DataFrame.from_dict(answer_dict)


    data3=single_instance.copy()
    data2=data3
    data2['sexo']=data3['sexo'].replace({'hombre': 0, 'mujer': 1})
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


# Definir en uvicorn el puerto **7860** y host **0.0.0.0**
if __name__ == '__main__':

    # 0.0.0.0 o 127.0.0.1
    uvicorn.run(app, host='0.0.0.0', port=7860)
