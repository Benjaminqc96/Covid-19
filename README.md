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

Una vez balanceado el conjunto de datos se hace la regresión teniendo como variable dependiente la 'clase' y como variables dependientes el género, la edad, y las demás relacionadas a los padecimientos de enfermedades. Para la seleccion de las variables se emplea la eliminación recursiva de variables (*Recursive Feature Elimination*) fijando como objetivo 5 variables.


<p align="center">
  Resumen del modelo 
</p>

<p align="center">
  <img width="500" src="https://github.com/Benjaminqc96/Covid-19/blob/main/resumen.png">
</p>

Las variables resultantes con un nivel superior al 95% de confianza son:
- fijo: toma valor de 1 si el paciente fue internado en un hospital covid.
- int: toma valor de 1 si el paciente fue intubado
- neu: toma valor de 1 si el paciente presentó neumonía.
- asma: toma valor de 1 si el paciente padece de asma.
- edad: vector numerico transformado de la edad.

Así mismo, se hizo el procedimiento de validación cruzada en 10 pliegues al conjunto preparado obteniendo una precisión promedio de 90.74%, con una desviación estandar de 0.46%, lo que nos indica que es un modelo robusto, estable y escalable. La curva ROC nos indica que el modelo en general tiene un 87% de probabilidad de clasificar adecuadamente los casos en los que los pacientes sobreviven o fallecen a causa de covid-19.

<p align="center">
  Curva ROC 
</p>

<p align="center">
  <img width="500" src="https://github.com/Benjaminqc96/Covid-19/blob/main/ROC.png">
</p>


## Dicusión de Resultados

En los análisis previos algunas variables que supondrían ser un predictor fiable para la clasificación no lo fueron al correr el modelo, esto debido a que no se contemplan los enfectos netos sino efectos conjuntos. En ésta investigación se encuentra evidencia científica de que el hecho de llevar a un paciente con sintomas de la enfermedad reduce sus probabilidades de fallecer, tal y como lo indica el coeficiente de la variable 'fijo', otra variable que reduce la probabilidad de que el paciente pierda la vida es el padecer asma, situación que puede ser explicada por los efectos positivos de los medicamentos contra el asma en pacientes que se infectaron de covid-19 como lo establece la universidad de Oxford https://www.forbes.com.mx/noticias-medicina-asma-oxford-estudio-reduce-probabilidad-hospitalizacion-covid-19/. Por otro lado los coeficientes positivos del modelo son de las varibles de la edad como lo mostró el análisis grafico en un principio;
el padecimiento de neumonia tiene secuelas graves como la disnea que puede afectar a los pacientes aún despues de su recuperacion https://www.clinicbarcelona.org/noticias/la-neumonia-causada-por-la-covid-19-puede-dejar-importantes-secuelas-respiratorias; la variable 'int' es la de mayor peso positivo en nuestra ecuación, debido a que es un procedimiento invasivo y poco recomendado cuando se presenta hipoxia en el paciente https://vapotherm.com/es/blog/se-debe-intubar-a-los-pacientes-con-covid-19/. 

Dada la extension de la base de datos fue posible calcular la presición del modelo construido con nuevos datos y determinar si en efecto fue un modelo robusto, estable e incluso escalable, por lo que se evaluaron las demás particiones hechas en R (6 particiones, una para análisis) obteniendo precisiones de entre 90% y 91% para las 5 particiones restantes.

