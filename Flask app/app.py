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

@app.route('/usuarios')
def getUsuarios():
    with open('usuarios.json', 'r') as datosUsuarios:
        usuarios = json.load(datosUsuarios)
    return jsonify(usuarios)

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

def nuevoIdPeliculas():
    with open('peliculas.json', 'r') as datosPeliculas:
        peliculas = json.load(datosPeliculas)
    return str(int(peliculas[-1]["peliculaID"]) + 1)

@app.route('/peliculas/agregar', methods=['POST'])
def postPeliNueva():
    peliAgregar = request.get_json()  
    id = nuevoIdPeliculas()

    peliAgregar["peliculaID"] = id
    with open('peliculas.json', 'r') as datosPeliculas:
        peliculas = json.load(datosPeliculas)
    peliculas.append(peliAgregar)

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

    with open('peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson)

        
@app.route("/peliculas/<peliculaID>/usuarioID/<usuarioID>/eliminar", methods=['DELETE'])
def borrarPeli(peliculaID, usuarioID):
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

# id comentarios
def nuevoIdComentario():
    with open('comentarios.json', 'r') as datosComentarios:
        comentarios = json.load(datosComentarios)
    return str(int(comentarios[-1]["comentarioID"]) + 1)

#ABM Comentarios
@app.route("/pelicula/<peliculaID>/comentarios/agregar", methods=['POST'])
def agregarComentario(peliculaID):
    with open('comentarios.json', 'r') as comentariosData:
        comentarios = json.load(comentariosData)
    with open('peliculas.json', 'r') as pelisData:
        peliculas = json.load(pelisData)
    id = nuevoIdComentario()    

    comentarioNuevo = request.get_json()
    comentarioNuevo["comentarioID"] = id
    comentarios.append(comentarioNuevo)
    
    for pelicula in peliculas:
        if pelicula['peliculaID'] == peliculaID:
            pelicula['comentariosID'].append(id)

    #Actulizando jsons
    with open('comentarios.json', 'w') as archivoJson:
        json.dump(comentarios, archivoJson, indent=4)
    with open('peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson, indent=4)

    return 'Creacion de comentario exitosa'

@app.route("/comentarios/<comentarioID>/usuarioID/<usuarioID>/borrar", methods=['DELETE'])
def borrarComentario(comentarioID,usuarioID):
    with open('comentarios.json', 'r') as comentariosData:
        comentarios = json.load(comentariosData)
    with open('peliculas.json', 'r') as pelisData:
        peliculas = json.load(pelisData)
    borrado = False
    print(comentarioID)
    print(usuarioID)
    for comentario in comentarios:
        if comentario["usuarioID"] == usuarioID and comentario["comentarioID"] == comentarioID:
            comentarios.remove(comentario)
            for pelicula in peliculas:                                   
                pelicula["comentariosID"].remove(comentarioID)
                borrado = True
                break

    with open('comentarios.json', 'w') as archivoJson:
        json.dump(comentarios, archivoJson, indent=4)
    with open('peliculas.json', 'w') as archivoJson:
        json.dump(peliculas, archivoJson, indent=4)

    if borrado == True:
        return "El comentario fue eliminado con exito"
    else:
        return "Algo salio mal, el comentario no fue eliminado"

@app.route("/comentarios/usuarioID/<usuarioID>")
def getComentariosUsuarioID(usuarioID):
    with open('comentarios.json', 'r') as comentariosData:
        comentarios = json.load(comentariosData)

    listaComentariosUsuarioID = []

    for comentario in comentarios:
        if comentario["usuarioID"] == usuarioID:
            listaComentariosUsuarioID.append(comentario)

    return jsonify(listaComentariosUsuarioID)


# @app.route("/comentario/save", methods=['PUT'])
# def modifComentario():
#     #Obteneniendo JSONs
#     comentarios = fc.obtenerComentarios()
    
#     comentarioNuevoLista = request.get_json()

#     for comentario in comentarios:
#         if comentario['id'] == comentarioNuevoLista['id'] and comentario['idUsuario'] == comentarioNuevoLista['idUsuario']:
#             comentario['comentario'] = comentarioNuevoLista['comentario']

#     #Actulizando JSONs
#     with open('jsons/comentarios.json', 'w') as archivoJson:
#         json.dump(comentarios, archivoJson, indent=4)

#     return 'Modificacion con exito'

# @app.route("/peliculas/<idPelicula>/comentarios/")
# def getComentarios(idPelicula):
#     #Obteneniendo JSONs
#     comentarios = fc.obtenerComentarios()
#     peliculas = fc.obtenerPeliculas()

#     listaComentarios = []

#     for pelicula in peliculas:
#         if pelicula['id'] == idPelicula:
#             for comentarioRecorrido in pelicula["idComentarios"]:
#                 for comentario in comentarios:
#                     if comentario['id'] == comentarioRecorrido:
#                         listaComentarios.append(comentario)
#                 return jsonify(listaComentarios)

#     return Response("{}", status=HTTPStatus.NOT_FOUND)




if __name__ == '__main__':
    app.run(debug=True)
    

    
