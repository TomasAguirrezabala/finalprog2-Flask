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
    return str(int(peliculas[-1]["peliculaID"]) + 1)

@app.route('/peliculas/agregar', methods=['POST'])
def postPeliNueva():
    peliAgregar = request.get_json()  
    id = nuevaIdPeliculas()

    peliAgregar["peliculaID"] = id
    with open('peliculas.json', 'r') as datosPeliculas:
        peliculas = json.load(datosPeliculas)
    peliculas.append(peliAgregar)

    #Actualizando JSONs
    with open('peliculas.json', 'w') as datosPeliculas:
        json.dump(peliculas, datosPeliculas, indent=4)

    return 'Pelicula registrada.' 

@app.route("/ultimas_diez_peliculas")
def get_ultimas_diez_peliculas():
    contador = 0
    with open('peliculas.json', 'r') as datos_diez_peliculas:
        diez_pelis = json.load(datos_diez_peliculas)
    ultimas_diez_peliculas = []
    for pelicula in reversed(diez_pelis):
        contador = contador + 1
        ultimas_diez_peliculas.append(pelicula)
        if contador == 10:
            break
    return jsonify(ultimas_diez_peliculas)

@app.route("/peliculas/modif/", methods=['PUT'])
def modifPelicula():
    with open('peliculas.json', 'r') as datosPeliculas:
        peliculas = json.load(datosPeliculas)

    modificaciones_pelicula = request.get_json()

    for pelicula in peliculas:
        if pelicula["id"] == modificaciones_pelicula["id"]:
            if modificaciones_pelicula["nombre"] != '':
                pelicula["nombre"] = modificaciones_pelicula["nombre"]
            elif modificaciones_pelicula["directorID"] != '':
                pelicula["directorID"] = modificaciones_pelicula["directorID"]
            elif modificaciones_pelicula["generoPeli"] != '':
                pelicula["generoPeli"] = modificaciones_pelicula["generoPeli"]
            elif modificaciones_pelicula["anio"] != '':
                pelicula["anio"] = modificaciones_pelicula["anio"]
            elif modificaciones_pelicula["sinopsis"] != '':
                pelicula["sinopsis"] = modificaciones_pelicula["sinopsis"]
            elif modificaciones_pelicula["portada"] != '':
                pelicula["portada"] = modificaciones_pelicula["portada"]
                {"nombre": "", "directorID": "", "generoPeli": "", "anio": "", "id": "", "portada": "", "sinopsis": ""}

    #Actualizando JSONs
    with open('peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson)

        
@app.route("/peliculas/<peliculaID>/usuarioID/<usuarioID>/eliminar", methods=['DELETE'])
def deletePelicula(peliculaID, usuarioID):
    with open('peliculas.json', 'r') as datosPeliculas:
        peliculas = json.load(datosPeliculas)
    with open('comentarios.json', 'r') as datosComentarios:
        comentarios = json.load(datosComentarios)
    
    
    for pelicula in peliculas:
        if pelicula["peliculaID"] == peliculaID:
            for idComentarioPeli in pelicula["comentariosID"]:
                if idComentarioPeli != "0":
                # tiene comentarios, hay que ver si le pertenecen
                    for comentario in comentarios:
                        if comentario["comentarioID"] == idComentarioPeli:
                        # si le pertenece el comentario, borramos igual
                            if comentario["usuarioID"] == usuarioID:
                                comentarios.remove(comentario)
                                with open('comentarios.json', 'w') as archivoJson:
                                    json.dump(comentarios, archivoJson, indent=4) 
                                borrar = True
                                break     
                            # tiene comentarios pero no le pertenecen
                            else:
                                return "La pelicula tiene comentarios que no te pertenecen, no puede ser eliminada"
                # no tiene comentarios
                else:
                    borrar = True 
            if borrar == True:
                peliculas.remove(pelicula)
                with open('peliculas.json', 'w') as archivoJson:
                    json.dump(peliculas, archivoJson, indent=4)
                return "Pelicula eliminada con exito"
            else:
                return "La pelicula tiene comentarios que no te pertenecen o no puede ser eliminada"
    return "Pelicula no encontrada"
        
if __name__ == '__main__':
    app.run(debug=True)
    

    
