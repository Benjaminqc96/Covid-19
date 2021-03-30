import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

base = pd.read_csv('/home/benjamin/Escritorio/covid/base_cov.csv/p1.csv')
base.head()

casos_positivos = base[(base['CLASIFICACION_FINAL'] == 1) |
                       (base['CLASIFICACION_FINAL'] == 2) |
                       (base['CLASIFICACION_FINAL'] == 3)]

casos_positivos = casos_positivos[casos_positivos['EDAD'] > 5]
#Sexo
casos_positivos = casos_positivos[(casos_positivos['SEXO'] == 1) |
                                  (casos_positivos['SEXO'] == 2)]

#NEUMONIA
casos_positivos = casos_positivos[(casos_positivos['NEUMONIA'] == 1) |
                                  (casos_positivos['NEUMONIA'] == 2)]

#DIABETES
casos_positivos = casos_positivos[(casos_positivos['DIABETES'] == 1) |
                                  (casos_positivos['DIABETES'] == 2)]

#ASMA
casos_positivos = casos_positivos[(casos_positivos['ASMA'] == 1) |
                                  (casos_positivos['ASMA'] == 2)]

#EPOC
casos_positivos = casos_positivos[(casos_positivos['EPOC'] == 1) |
                                  (casos_positivos['EPOC'] == 2)]

#INMUSUPR
casos_positivos = casos_positivos[(casos_positivos['INMUSUPR'] == 1) |
                                  (casos_positivos['INMUSUPR'] == 2)]

#HIPERTENSION
casos_positivos = casos_positivos[(casos_positivos['HIPERTENSION'] == 1) |
                                  (casos_positivos['HIPERTENSION'] == 2)]

#CARDIOVASCULAR
casos_positivos = casos_positivos[(casos_positivos['CARDIOVASCULAR'] == 1) |
                                  (casos_positivos['CARDIOVASCULAR'] == 2)]

#OBESIDAD
casos_positivos = casos_positivos[(casos_positivos['OBESIDAD'] == 1) |
                                  (casos_positivos['OBESIDAD'] == 2)]

#RENAL
casos_positivos = casos_positivos[(casos_positivos['RENAL_CRONICA'] == 1) |
                                  (casos_positivos['RENAL_CRONICA'] == 2)]

#TABAQUISMO
casos_positivos = casos_positivos[(casos_positivos['TABAQUISMO'] == 1) |
                                  (casos_positivos['TABAQUISMO'] == 2)]

#tipo_paciente
casos_positivos = casos_positivos[(casos_positivos['TIPO_PACIENTE'] == 1) |
                                  (casos_positivos['TIPO_PACIENTE'] == 2)]

sob = casos_positivos[casos_positivos['FECHA_DEF'] == '9999-99-99']
dif = casos_positivos[casos_positivos['FECHA_DEF'] != '9999-99-99']

dist_edad_s = Counter(sob['EDAD'])
dist_edad_d = Counter(dif['EDAD'])

plt.figure()
plt.bar(dist_edad_d.keys(), dist_edad_d.values())
plt.xlabel('Edad')
plt.ylabel('Numero de muertes')
plt.show()
#plt.savefig('/home/benjamin/Escritorio/coviddistmort.png')

plt.figure()
plt.bar(dist_edad_s.keys(), dist_edad_s.values())
plt.xlabel('Edad')
plt.ylabel('Numero de sobrevivientes')
plt.show()
#plt.savefig('/home/benjamin/Escritorio/coviddistsob.png')

#Fecha de defuncion variable binaria dependiente
casos_positivos['DEF'] = np.where(casos_positivos['FECHA_DEF'].str.contains('9999-99-99'), 0,1)

#categoricas: sexo, tipo_pac, intubado, neumonia, diabetes, asma, epoc, inmuspr,
#hipertension, cardiovascular, obesidad, renal, tabaquismo
categoricas = casos_positivos.loc[:, ['SEXO', 'TIPO_PACIENTE', 'INTUBADO',
                                      'NEUMONIA', 'DIABETES', 'ASMA', 'EPOC',
                                      'INMUSUPR', 'HIPERTENSION',
                                      'CARDIOVASCULAR', 'OBESIDAD', 'RENAL_CRONICA',
                                      'TABAQUISMO']]

categoricas['SEXO'] = categoricas['SEXO'].astype('category')
categoricas['TIPO_PACIENTE'] = categoricas['TIPO_PACIENTE'].astype('category')
categoricas['INTUBADO'] = categoricas['INTUBADO'].astype('category')
categoricas['NEUMONIA'] = categoricas['NEUMONIA'].astype('category')
categoricas['DIABETES'] = categoricas['DIABETES'].astype('category')
categoricas['ASMA'] = categoricas['ASMA'].astype('category')
categoricas['EPOC'] = categoricas['EPOC'].astype('category')
categoricas['INMUSUPR'] = categoricas['INMUSUPR'].astype('category')
categoricas['HIPERTENSION'] = categoricas['HIPERTENSION'].astype('category')
categoricas['CARDIOVASCULAR'] = categoricas['CARDIOVASCULAR'].astype('category')
categoricas['OBESIDAD'] = categoricas['OBESIDAD'].astype('category')
categoricas['RENAL_CRONICA'] = categoricas['RENAL_CRONICA'].astype('category')
categoricas['TABAQUISMO'] = categoricas['TABAQUISMO'].astype('category')

categoricas = pd.get_dummies(categoricas)
categoricas = categoricas.drop(['INTUBADO_97', 'INTUBADO_99', 'TIPO_PACIENTE_2',
                                'INTUBADO_2', 'NEUMONIA_2', 'DIABETES_2', 'ASMA_2',
                                'EPOC_2', 'INMUSUPR_2', 'HIPERTENSION_2',
                                'CARDIOVASCULAR_2', 'OBESIDAD_2', 'RENAL_CRONICA_2',
                                'TABAQUISMO_2'], 1)

import sklearn.preprocessing as sk
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from imblearn.over_sampling import SMOTE
import statsmodels.api as sm
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.feature_selection import RFE
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score


edad = pd.DataFrame(sk.minmax_scale(casos_positivos['EDAD']))
edad.columns.name = 'edad'
clas_def = casos_positivos[['DEF']].astype('category')

base_final = categoricas
base_final['EDAD'] = edad.values
base_final['CLASE'] = clas_def.values
base_final.columns = ['hombre', 'mujer', 'fijo', 'int', 'neu',
                      'diab', 'asma', 'epoc', 'inm', 'hip', 'car', 'obe',
                           'ren', 'tab', 'edad', 'clase']

variables = ['hombre', 'mujer', 'fijo', 'int', 'neu',
                      'diab', 'asma', 'epoc', 'inm', 'hip', 'car', 'obe',
                           'ren', 'tab', 'edad']

base_final = base_final.sample(frac = 0.08)

conjunto_x = base_final.loc[:, variables]
conjunto_y = base_final.loc[:, 'clase']


#balanceo del conjunto de datos
over_samp = SMOTE(random_state=634)
X_train,X_test,y_train,y_test = train_test_split(conjunto_x, conjunto_y,
                                                 test_size = 0.3, random_state = 634)

os_dx,os_dy = over_samp.fit_resample(X_train, y_train)
os_dxp,os_dyp = over_samp.fit_resample(X_test,y_test)
x_comp, y_comp = over_samp.fit_resample(conjunto_x, conjunto_y)


estimador = LogisticRegression()
selector = RFE(estimator= estimador, n_features_to_select= 5)

selec = selector.fit(os_dx, os_dy)
posiciones = list(selec.support_)
os_dx_2 = os_dx.loc[:, posiciones]
os_dxp_2 = os_dxp.loc[:, posiciones]


reg_log2 = sm.Logit(exog = os_dx_2, endog = os_dy).fit()
print(reg_log2.summary())

reg_log = LogisticRegression()
reg_log.fit(X = os_dx_2, y = os_dy)
reg_log.score(X = os_dxp_2, y = os_dyp)
x_eval = conjunto_x.loc[:, posiciones]

reg_log.score(X = x_eval, y = conjunto_y)

val_cru = cross_val_score(estimator = reg_log, X = x_eval,
                          y = conjunto_y, cv = 10)

np.mean(val_cru)
np.std(val_cru)

rl_rocauc = roc_auc_score(y_true = os_dyp,
                          y_score = reg_log.predict(os_dxp_2))
fpr, tpr, thresholds = roc_curve(os_dyp,
                       reg_log.predict_proba(os_dxp_2)[:,1])

plt.figure()
plt.plot(fpr, tpr, label = 'Regresión logística (area = %0.2f)'%
         rl_rocauc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Falsos Positivos')
plt.ylabel('Verdaderos Positivos ')
plt.legend(loc="lower right")
#plt.savefig('/home/benjamin/Escritorio/ROC.png')




base2 = pd.read_csv('/home/benjamin/Escritorio/covid/base_cov.csv/p3.csv')

cp_2 = base2[(base2['CLASIFICACION_FINAL'] == 1) |
                       (base2['CLASIFICACION_FINAL'] == 2) |
                       (base2['CLASIFICACION_FINAL'] == 3) ]

cp_2 = cp_2[cp_2['EDAD'] > 0]

fecha_2 = pd.DataFrame(np.where(cp_2['FECHA_DEF'].str.contains('9999-99-99'), 0, 1))
casos_positivos_2 = cp_2[['TIPO_PACIENTE', 'INTUBADO', 'NEUMONIA', 'ASMA', 'EDAD']]


tip_pac = np.where(casos_positivos_2['TIPO_PACIENTE'] == 1, 1, 0)

intub = np.where(casos_positivos_2['INTUBADO'] == 1, 1, 0)

neum = np.where(casos_positivos_2['NEUMONIA'] == 1, 1, 0)

asma = np.where(casos_positivos_2['ASMA'] == 1, 1, 0)

edad_2 = sk.minmax_scale(casos_positivos_2['EDAD'])

cx_2 = pd.DataFrame()
cx_2['fijo'] = tip_pac
cx_2['int'] = intub
cx_2['neu'] = neum
cx_2['asma'] = asma
cx_2['edad'] = edad_2

cy_2 = fecha_2.astype('category')
reg_log.score(X = cx_2, y = cy_2)


