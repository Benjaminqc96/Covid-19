library(sparklyr)
library(dplyr)

sc <- spark_connect(master = "local")

base_em <- spark_read_csv(sc = sc, path = file.choose())

base_covid <- base_em %>% select(SEXO, TIPO_PACIENTE, FECHA_DEF, INTUBADO, NEUMONIA,
                                 EDAD, DIABETES, ASMA, EPOC, INMUSUPR, HIPERTENSION,
                                 CARDIOVASCULAR, OBESIDAD, RENAL_CRONICA, TABAQUISMO,
                                 CLASIFICACION_FINAL)


spark_write_csv(x = base_covid, path = '/home/benjamin/Escritorio/covid/base_cov.csv')

spark_disconnect(sc = sc)


