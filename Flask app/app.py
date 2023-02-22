from flask import Flask, jsonify, Response, request
import json
import requests as rq

app=Flask(__name__)



@app.route("/comentarios")
def getComentarios():
    with open('comentarios.json', 'r') as datosComentarios:
        comentarios = json.load(datosComentarios)
    return jsonify(comentarios)


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

@app.route("/peliculas/director/<id>")
def getPeliculasDirector(id):
    with open('peliculas.json', 'r') as datosPeliculas:
        peliculas= json.load(datosPeliculas)

    peliculasDirector = []

    for pelicula in peliculas:
        if pelicula["directorID"] == id:
            peliculasDirector.append(pelicula)
    if len(peliculasDirector)==0:
        return "director no encontrado"
    else:
        return jsonify(peliculasDirector)
    
@app.route("/peliculas/portada")
def getPeliculasImagen():
    with open('peliculas.json','r') as peliculasImagenData:
        peliculasImagen = json.load(peliculasImagenData)

    peliculasConImagen = []
    
    for peliculaImagen in peliculasImagen:
        if peliculaImagen["portada"] == " ":
            # no tiene portada
            continue
        else:
            peliculasConImagen.append(peliculaImagen)
            
    if len(peliculasConImagen) == 0:
        return("Esas peliculas no tienen portada")
    else:
        return peliculasConImagen         

def nuevaIdPeliculas():
    with open('peliculas.json', 'r') as datosPeliculas:
        peliculas = json.load(datosPeliculas)
    return str(int(peliculas[-1]["id"]) + 1)

@app.route('/peliculas/agregar', methods=['POST'])
def postPeliNueva():
    peliAgregar = request.get_json()  
    id = nuevaIdPeliculas()

    peliAgregar["id"] = id
    with open('peliculas.json', 'r') as datosPeliculas:
        peliculas = json.load(datosPeliculas)
    peliculas.append(peliAgregar)

    #Actualizando JSONs
    with open('peliculas.json', 'w') as datosPeliculas:
        json.dump(peliculas, datosPeliculas)

    return 'Pelicula registrada.' 


@app.route("/peliculas/<id>/UsuarioID/<UsuarioID>/eliminar", methods=['DELETE'])
def deletePelicula(id, idUsuario):
    with open('peliculas.json', 'r') as datosPeliculas:
        peliculas = json.load(datosPeliculas)
    comentarios = fc.obtenerComentarios()
    comentariosOtrosUsuarios = False
    valor = {}

    for pelicula in peliculas:
        if pelicula["id"] == id:
            for comentarioRecorrido in pelicula["idComentarios"]:
                for comentario in comentarios:
                    if comentarioRecorrido == comentario["id"]  and comentario["idUsuario"] != idUsuario:
                        comentariosOtrosUsuarios = True
        if comentariosOtrosUsuarios == False and pelicula["id"] == id:
            valor = pelicula 
            for peliculaIdComentarios in valor["idComentarios"]:
                for comentario in comentarios:
                    if comentario['id'] == peliculaIdComentarios:
                        comentarios.remove(comentario)

    if comentariosOtrosUsuarios == True:
        return 'Borrado no exitoso, tiene comentarios de otros usuarios o no se pudo eliminar correctamente'
    else:
        peliculas.remove(valor)
        #Actualizando JSONs
        with open('jsons/peliculas.json', 'w') as archivoJson:
            json.dump(peliculas, archivoJson, indent=4)
        with open('jsons/comentarios.json', 'w') as archivoJson:
            json.dump(comentarios, archivoJson, indent=4)
        return 'Borrado exitoso'


        
if __name__ == '__main__':
    app.run(debug=True)
    

    
