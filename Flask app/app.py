from flask import Flask, jsonify
import json
import requests as rq



app=Flask(__name__)

# @app.route('/')
# def index():
#     return "hola"

# peliculas = [{'nombre':'el senior de los anillos', 'director':'tomas', 'anio':1999, 'id':1} , {'nombre':'batman', 'director':'tomas', 'anio':'2013','id':2}]
# # esto crea los jsons
# with open('peliculas.json', 'w') as datosPeliculas:
#     json.dump( peliculas, datosPeliculas)
#     print(datosPeliculas)


# esto carga los jsons
# @app.route("/pelis")
# def pelis():
#     with open('peliculas.json', 'r') as basePeliculas:
#         peli = json.load(basePeliculas)
#         print('funciono')
#         return peli   

# with open('peliculas.json', 'r') as datosPeliculas:
#     peliculas = json.load(datosPeliculas)

# with open('generos.json', 'r') as datosGeneros:
#     generos = json.load(datosGeneros)


@app.route("/generos")
def getGeneros():
    with open('generos.json', 'r') as datosGeneros:
        generos = json.load(datosGeneros)
    return jsonify(generos)
        
 
@app.route("/pelis") 
def getPelis():
    with open('peliculas.json', 'r') as datosPeliculas:
        peliculas = json.load(datosPeliculas)
    return jsonify(peliculas)

@app.route("/directores")
def getDirec():
    with open('directores.json', 'r') as datosDirectores:
        directores = json.load(datosDirectores)
    return jsonify(directores)


        
if __name__ == '__main__':
    app.run(debug=True)
    

    
