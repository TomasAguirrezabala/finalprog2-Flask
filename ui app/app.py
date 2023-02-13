import requests as rq

peliculas = rq.get('http://127.0.0.1:5000/pelis')
print(type(peliculas))