from flask import Flask, jsonify
import json
import requests as rq



app=Flask(__name__)

@app.route('/')
def index():
    return "hola"

peliculas = [{'nombre':'el senior de los anillos', 'director':'tomas', 'anio':1999, 'id':1} , {'nombre':'batman', 'director':'tomas', 'anio':'2013','id':2}]
# esto crea los jsons
with open('peliculas.json', 'w') as datosPeliculas:
    json.dump( peliculas, datosPeliculas)
    print(datosPeliculas)


# esto carga los jsons
@app.route("/pelis")
def pelis():
    with open('peliculas.json', 'r') as basePeliculas:
        peli = json.load(basePeliculas)
        print('funciono')
        return peli   
    

    
if __name__ == '__main__':
    app.run(debug=True)
    

    
