import requests

search_api_url = 'http://0.0.0.0:7860/prediccion'


data = {'edad': 22,
        'sexo': 'mujer',
        'alfabeto': 'Si',
        'sistema_salud': 'Obra social (incluye PAMI)',
        'nivel_educativo': 'Secundaria Completa',
        'ocupacion_jerarquia': 'Cuenta propia'
        }




response = requests.post(search_api_url, json=data)
print(response.json())

#response = requests.get('http://0.0.0.0:7860/prediccion')
#print(response.json())

#response = requests.get('http://0.0.0.0:7860/')
#print(response.json())

#response = await requests.get('http://127.0.0.1:8000/edvai')
#print(response.json())