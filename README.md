# Covid-19
Clasificación y predicción de defunciones por covid-19 en México

Para este proyecto se parte de la base de datos abiertos de la Dirección de Epidemiología, disponoble en la
liga https://www.gob.mx/salud/documentos/datos-abiertos-152127, la base con la que se trabaja fue consultada 
el 3 de febrero. La extensión original de la base de datos es de aproximadamente 700 megabytes, por lo que se 
procede a seleccionar las variables de interés y hacer la partición en R, usando la libreria sparklyR y dplyr.
Una vez hecha la selección y partición se procede a hacer el anális exploratorio de los datos, en particular
se analiza la distribución de las defunciones por edad, así como la supervivencia. La mortalidad tiene su punto
más alto alrededor de los 60 años, mientras que la supervivencia tiene su punto más alto alrededor de los 30
años.


![Gráfico de mortalidad](https://github.com/Benjaminqc96/Covid-19/blob/main/coviddistmort.png)


![Gráfico de supervivencia](https://github.com/Benjaminqc96/Covid-19/blob/main/coviddistsob.png)


