import re
from bs4 import BeautifulSoup
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#Conectarse al sitio web
url = 'https://cienciasdelsur.com/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
links = soup.findAll('a',class_ ='td-image-wrap') #busco todos los enlaces de esa clase en especifica
enlaces = list() #creo una lista para guardar todos los enlaces del foro

for i in links: #se guardan los enlaces
    enlaces.append(i.get('href'))

#Scraping de todos los enlaces
texto = "" #en esta variable voy a guardar todo el documento que ira exportado a un archivo
i=4 #el contador empieza en 4, porque ahi esta el primer enlace
with open('EXTRACCION_TEXTOS.txt', 'w', encoding='utf-8') as f: #se crea el archivo y se guarda la informacion
    f.write(texto)

while i < len(enlaces): #con este while recorre mi lista de enlace para scrapear todos los enlaces
    url = enlaces[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titulo = soup.find('h1',class_ = 'entry-title').text #se extrae el titulo del articulo
    texto += titulo #se guarda el titulo para luego concatenar con el articulo
    articulo = soup.find('div', class_ = 'td-post-content tagdiv-type') #extraigo todo el contenido del articulo
    texto += articulo.get_text() #concateno el titulo del articulo con el articulo
    with open("EXTRACCION_TEXTOS.txt", "a", encoding='utf-8') as archivo: #se escribe el articulo en el archivo
        archivo.write(texto)
    i+=1 #paso al siguente enlace
    texto = "" #se reinicia la variable para el siguente enlace

with open("EXTRACCION_TEXTOS.txt", "r", encoding="utf-8") as archivo: #se lee el archivo
    file_content = archivo.read()

#busca todas las palabras del archivo basado en esa expresion regular, las convierte a minuscula y se guardan en la lista
word_array = re.findall(r'\b\w+\b', file_content.lower())

word_frequency = {} #diccionario que contendra las frecuencias de las palabras

#lista de palabras no deseadas
no_deseadas = ["yo", "tú", "él", "ella", "nosotros", "vosotros", "ellos", "ellas",
               "de", "la", "el", "las", "los", "del", "a", "al", "ante", "bajo", "cabe",
               "con", "contra", "de", "desde", "durante", "en", "entre", "hacia",
               "hasta", "mediante", "para", "por", "según", "sin", "so", "sobre",
               "tras", "y", "o","e", "pero", "aunque", "porque", "como", "si",
               "que", "cuando", "donde", "quien", "cual", "esto", "eso", "aquello",
               "tambien", "es", "un", "una", "uno", "se", "no", "tiene", "más", "este", "esta",
               "lo", "hay", "su", "muy", "ahí", "estar",
               "puede", "pero", "está", "sus", "son", "fue", "ser", "parte", "ha", "forma",
               "ya", "debe", "también","alejandra","además","%","sosa","otros","ejemplo","través","5","nos","the",
               "te","todo", "tienen","vez","cómo","están","estas","ni","gran","2022","así","dos","estos",
               "benítez","qué","que","sino","comentó","compartir","foto","otra","falta","cualquier","cada","luego",
               "pueden","p","about","adriana","alvarenga","sea","fabrizio","sebastián","aine","related","author","p",
               "ed","otras","tener","alberto","https://cienciasdelsur.com/author/glkuwssnkcrhomwm/","posts","https://cienciasdelsur.com/author/alesosa/",
               "¿qué", "https://cienciasdelsur.com/author/fabrizio-pomata/","of","r","toda","pues","p.","algunos","ésta","uso","algunas","R","r","le","solo",
               "min.","hace","existe","https://cienciasdelsur.com/author/ciencia-del-sur/","(foto::","pareció","josé","FOTO","com","https","cienciasdelsur",
               "personas","acceso","actualmente","4","trabajo"
                ]
#en este ciclo se guardan las palabras con sus apariciones
for word in word_array:
    if word not in no_deseadas:
        word_frequency[word] = word_frequency.setdefault(word, 0) + 1

top_words = sorted(word_frequency.items(), key=lambda x: -x[1])[:50] #se ordena el diccionario
print("Las 50 palabras mas repetidas:")
# Se muestran las 50 palabras mas repetidas
for word, frequency in top_words:
    print(f"{word}: {frequency}")

# Se escribe las palabras y sus frecuencias en un archivo
with open("FRECUENCIA_PALABRAS.txt", "w", encoding='utf-8') as file:
    for word, frequency in top_words:
        file.write(f"{word}: {frequency}\n")

#se lee el archivo donde se guardaron las palabras que mas aparecen
with open('FRECUENCIA_PALABRAS.txt', 'r', encoding="utf-8") as file:
    text = file.read()

# Se crea el objeto WordCloud para crear la nube de palabras
wordcloud = WordCloud(width=800, height=800, background_color='white', max_words=50, contour_width=3, contour_color='steelblue')

# Se genera el gráfico de nube de palabras
wordcloud.generate(text)
plt.figure(figsize=(6,6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

#Item 2
#Conectarse al sitio web
url = 'https://cienciasdelsur.com/'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
links = soup.findAll('a',class_ ='td-image-wrap') #busco todos los enlaces de esa clase en especifica
enlaces = list() #creo una lista para guardar todos los enlaces del foro

for i in links: #se guardan los enlaces
    enlaces.append(i.get('href'))

palabra_compuesta = input("Ingrese su palabra compuesta: ")
apariciones = 0 # variable para almacenar todas las apariciones de la palabra compuesta

#Scraping de todos los enlaces
i=4 #el contador empieza en 4, porque ahi esta el primer enlace

while i < len(enlaces): #básicamente lo mismo que el primer while
    url = enlaces[i]
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    if palabra_compuesta in text: # Se busca la palabra compuesta en el texto de la página
        apariciones +=1

    i+=1 #paso al siguente enlace

# Se muestra todas las apariciones encontradas de la palabra compuesta
if apariciones > 0:
    print('Se encontraron', apariciones, 'apariciones de la palabra compuesta: ', palabra_compuesta)
else:
    print('No se encontraron apariciones de la palabra compuesta.')
