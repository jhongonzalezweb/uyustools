import os
import bs4
import math
import json
import pandas
import requests
from bs4 import BeautifulSoup

os.system("clear")
print("Ingresa e link de UYUSTOOLS: ")
website = input()  #"https://www.uyustools.cl/producto/tornillo-banco-6-uyustools-tob206/"
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')

full_script = soup.find_all("script")
todo = str(full_script[2])
json_object = json.loads(todo[60:-9])

#Extraccion de imagen
name_god = json_object["@graph"][4]["name"]
print("Nombre del producto:", name_god)

#Extraccion de imagen
img_god = json_object["@graph"][2]["url"]
print("Link image:", img_god)

#Calculo de precio con formula
price_god = json_object["@graph"][4]["offers"]["priceSpecification"]["price"]
resultado = round(int(price_god) * 0.75)

print("Precio producto en pagina web:", price_god)
print("Precio producto en excel con formula:", resultado)

#Extraccion de SKU para Pandas
sku = json_object["@graph"][4]["sku"]
print("Sku:", sku)

#Extraccion de caracteristicas
caracteristicas = json_object["@graph"][4]["description"]
if "Venta mínima" in caracteristicas:
  reemplazo = caracteristicas.replace("Venta mínima","\nVenta mínima").replace(":",":\n")
  print(reemplazo)

df = pandas.read_csv('prod40.csv')
for i in df.index:
    if sku.upper() == str(df['Artículo'][i]):
        sku_template = df.loc[i]['Precio Final']

print(sku_template)

html = open("mensaje.html", "w")
mensaje = """

<!DOCTYPE html>
<html lang="es">

<head>
    <title>W3.CSS Template</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
        body { font-family: "Lato", sans-serif }
    </style>
</head>
<body>
    <!-- Page content -->
    <div class="w3-content" style="max-width:2000px;margin-top:46px">
        <!-- The Tour Section -->
        <div class="w3-black" id="tour">
            <div class="w3-container w3-content w3-padding-64" style="max-width:800px">
                <h2 class="w3-wide w3-center">""" + name_god + """</h2>
                <p class="w3-opacity w3-center"><i> Precio producto en pagina web: """ + str(price_god) + """</i></p>
                <p class="w3-opacity w3-center"><i> Sku: """ + str(sku) + """</i></p><br>
                <div class="w3-row-padding w3-padding-32" style="margin:0 -16px">
                    <div class="w3-third w3-margin-bottom">
                        <div class="w3-container w3-black">
                        </div>
                    </div>
                    <div class="w3-third w3-margin-bottom">
                        <img src='""" + img_god + """' alt='""" + img_god + """' style="width:100%" class="w3-hover-opacity">
                        <div class="w3-container w3-white">
                            <p><b>Precio producto con formula:</b></p>
                            <p><b>""" + str(resultado) + """</b></p>
                        </div>
                    </div>
                    <div class="w3-third w3-margin-bottom">
                        <div class="w3-container w3-black">
                        </div>
                    </div>
                </div>
                <p class="w3-opacity w3-center"><i> Precio producto 40 de descuento en Excel: """ + str(sku_template) + """</i></p>
            </div>
        </div>
    </div>
</body>

</html>
"""

html.write(mensaje)
html.close()

os.system("google-chrome mensaje.html")
exit()