# Covid-19
Clasificación y predicción de defunciones por covid-19 en México


Para este proyecto se parte de la base de datos abiertos de la Dirección de Epidemiología, disponible en la liga https://www.gob.mx/salud/documentos/datos-abiertos-152127, la base con la que se trabaja fue consultada el 3 de febrero. La extensión original de la base de datos es de aproximadamente 700 megabytes, por lo que se  procede a seleccionar las variables de interés y hacer la partición en R, usando la libreria sparklyR y dplyr. Las variables de interés en este caso son la edad, género, el tipo de paciente (ambulatorio o internado), la fecha de defunción, el diagnóstico recibido (positivo para covid-19) y las relacionadas a padecimientos como: diabetes, neumonía, asma, EPOC, inmunosupresión, hipertensión, enfermedades cardiovasculares, obesidad, enfermedades renales crónicas y tabaquismo.

Una vez hecha la selección de las variables se hace un subconjunto donde solo hay observaciones con diagóstico positivo a covid-19 (310206 observaciones), se procede a hacer el análisis exploratorio de los datos, en particular se analiza la distribución de las defunciones por edad, así como la supervivencia. La mortalidad tiene su punto más alto alrededor de los 60 años, mientras que la supervivencia tiene su punto más alto alrededor de los 30 años.

<p align="center">
  Gráfico de mortalidad 
</p>

<p align="center"> 
  <img width="500" src="https://github.com/Benjaminqc96/Covid-19/blob/main/coviddistmort.png">
</p>

<p align="center">
  Gráfico de supervivencia 
</p>

<p align="center">
  <img width="500" src="https://github.com/Benjaminqc96/Covid-19/blob/main/coviddistsob.png">
</p>


Dado que la edad es la única variable numérica, solo se hace gráfica de la distribución de dicha variable, las demás variables se analizan como variables *dummies*, debido a que describen la presencia o ausencia de las enfermedades o padecimientos previamente mencionados, así como el género. La edad es modificada en escala debido a que las demás variables toman valores de 0 o 1, por lo que se *normaliza* la variable, pasando de una escala de 0 a 100 a una escala de 0 a 1.


De las 310206 observaciones se hace un muestreo aleatorio simple del cual se eligen 24816 casos, con los cuales se hizo una regresión logística binaria con el propósito de predecir el fallecimiento de pacientes infectados por covid-19 con las variables seleccionadas. Al analizar los gráficos la edad parece ser un predictor fiable para el modelo, así como tambien la variable de diabetes debido a que 30% de las defunciones padecian diabetes; la variable de género mostró que la mortalidad en los hombres es aproximadamente el doble (66%) que en las mujeres (34%) por lo que podría ser un buen predictor. 

<p align="center">
  Gráfico de casos 
</p>

<p align="center">
  <img width="500" src="https://github.com/Benjaminqc96/Covid-19/blob/main/casos.png">
</p>


De la muestra obtenida se observa una diferencia considerable entre la clase 0 (sobreviven) y la clase 1 (fallecen), hay que aplicar muestreo informativo previo al entrenemiento de la regresón logística, por lo que se generan muestras sintéticas con la técnica *Syntetic Minority Oversampling Technique* (SMOTE)

