# -*- coding: utf-8 -*-
"""
Started on Wed Sep 13 15:55:22 2017

@author: carlos.arana

Descripcion: Creación de dataset para el parámetro P0712 "Número de Accidentes"

"""

import pandas as pd
import numpy as np
import sys

# Librerias locales utilizadas
module_path = r'D:\PCCS\01_Dmine\Scripts'
if module_path not in sys.path:
    sys.path.append(module_path)

from SUN.asignar_sun import asignar_sun
from SUN_integridad.SUN_integridad import SUN_integridad
from PCCS_variables.PCCS_variables import variables
from ParametroEstandar.ParametroEstandar import ParametroEstandar
from AsignarDimension.AsignarDimension import AsignarDimension
from DocumentarParametro.DocumentarParametro import DocumentarParametro
from VarInt.VarInt import VarInt

"""
Las librerias locales utilizadas renglones arriba se encuentran disponibles en las siguientes direcciones:
SCRIPT:             | DISPONIBLE EN:
------              | ------------------------------------------------------------------------------------
asignar_sun         | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/SUN
SUN_integridad      | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/SUN_integridad
variables           | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/PCCS_variables
ParametroEstandar   | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/ParametroEstandar
AsignarDimension    | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/AsignarDimension
DocumentarParametro 1 https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/DocumentarParametro
"""

# Documentacion del Parametro ---------------------------------------------------------------------------------------
# Descripciones del Parametro
ClaveParametro = 'P0712'
DescParam = 'Número de accidentes en zonas urbanas'
UnidadesParam = 'unidades'
PeriodoParam = '2015'
NombreParametro = 'Numero de accidentes'
TituloParametro = 'Accidentes'                              # Para nombrar la columna del parametro

# Descripciones del proceso de Minería
ClaveDataset = 'MV02'
NomDataset = r'Accidentes de tránsito en zonas urbanas y suburbanas'
DescDataset = r'Numero de accidentes de transito de acuerdo al lugar donde sucedieron (Zona urbana o suburbana),' \
              r'agregados a nivel municipal, de 1997 a 2015'
ContenidoHojaDatos = 'Accidentes en zonas urbanas, de 1997 a 2015, agregados a nivel municipal para municipios ' \
                     'que forman parte del subsistema principal del SUN'
Notas = 'S/N'
DescVarIntegridad = 'La variable de integridad municipal para esta Dataset es binaria: \n' \
                    '1 =  El municipio cuenta con informacion \n0 = El municipio no cuenta con información'
NomFuente = 'INEGI (Microdatos)'
UrlFuente = 'http://www.beta.inegi.org.mx/proyectos/registros/economicas/accidentes/'
ActDatos = '2015'
DispTemp = '1997 a 2015'
PeriodoAct = 'Anual'
DesagrMax = 'Municipal'

# Descripciones generadas desde la clave del parámetro
DirFuente = r'D:\PCCS\01_Dmine\Datasets\{}'.format(ClaveDataset)
DSBase = '"{}.xlsx", disponible en ' \
         'https://github.com/INECC-PCCS/01_Dmine/tree/master/Datasets/{}'.format(ClaveDataset, ClaveDataset)
ClaveDimension = ClaveParametro[1:3]
NomDimension = AsignarDimension(ClaveDimension)['nombre']
DirDimension = ClaveDimension + "_" + AsignarDimension(ClaveDimension)['directorio']
RepoMina = 'https://github.com/INECC-PCCS/01_Dmine/tree/master/{}/{}'.format(DirDimension, ClaveParametro)
DirDestino = r'D:\PCCS\01_Dmine\{}'.format(ClaveDimension+"_"+AsignarDimension(ClaveDimension)['directorio'])

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Dataset Inicial
dataset = pd.read_excel(DirFuente + r'\{}.xlsx'.format(ClaveDataset),
                        sheetname="ACCIDENTES_URBANA", dtype={'CVE_MUN': str})
dataset.set_index('CVE_MUN', inplace=True)

# Generar dataset para parámetro y Variable de Integridad
par_dataset = dataset['2015'].rename('Total_Parametro').to_frame()
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo = 1)

# Consolidar datos por ciudad para parametro
# par_dataset['CVE_MUN'] = par_dataset.index
variables_SUN = ['CVE_MUN', 'NOM_MUN', 'CVE_SUN', 'NOM_SUN', 'NOM_ENT']
DatosLimpios = asignar_sun(par_dataset, vars=variables_SUN)
OrdenColumnas = (variables_SUN + variables_dataset)
DatosLimpios = DatosLimpios[OrdenColumnas]    # Reordenar las columnas

# Consolidar datos por ciudad para hoja_datos
dataset.columns = [ClaveParametro+"_"+i for i in list(dataset)]
var_disponibles = list(dataset)
dataset['CVE_MUN'] = dataset.index
hoja_datos = asignar_sun(dataset)
hoja_datos = hoja_datos[(['CVE_MUN', 'CVE_SUN', 'NOM_SUN', 'TIPO_SUN'] + var_disponibles)].set_index('CVE_MUN')

# Revision de integridad
integridad_parametro = SUN_integridad(DatosLimpios)
info_completa = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 1)      # Para generar grafico de integridad
info_sin_info = sum(integridad_parametro['INTEGRIDAD']['INTEGRIDAD'] == 0)      # Para generar grafico de integridad
info_incomple = 135 - info_completa - info_sin_info                             # Para generar grafico de integridad

# Construccion del Parametro
param_dataset = DatosLimpios.set_index('CVE_SUN')
param_dataset['CVE_SUN'] = param_dataset.index
param = param_dataset.groupby(level=0).agg('sum')['Total_Parametro']       # Agregacion por ciudad
intparam = param_dataset.groupby(level=0).agg('mean')['VAR_INTEGRIDAD']    # Integridad por ciudad
Tipo_Sun = integridad_parametro['EXISTENCIA']['TIPO_SUN']
Tipo_Sun = Tipo_Sun.groupby(Tipo_Sun.index).first()
std_nomsun = param_dataset['CVE_SUN'].map(str)+' - '+param_dataset['NOM_SUN']   # Nombres estandar CVE_SUN + NOM_SUN
std_nomsun.drop_duplicates(keep='first', inplace=True)
Parametro = pd.DataFrame()
Parametro['CIUDAD'] = std_nomsun
Parametro['TIPO_SUN'] = Tipo_Sun
Parametro[ClaveParametro] = param
Parametro['INTEGRIDAD'] = intparam
Parametro = Parametro.sort_index()

# Lista de Variables
variables_locales = sorted(list(set(list(DatosLimpios) +
                                    list(integridad_parametro['INTEGRIDAD']) +
                                    list(integridad_parametro['EXISTENCIA']) +
                                    list(Parametro))))
metavariables = variables(variables_locales)

# Metadatos
d_parametro = {
    'DESCRIPCION DEL PARAMETRO': np.nan,
    'Clave': ClaveParametro,
    'Nombre del Parametro': NombreParametro,
    'Descripcion del Parametro': DescParam,
    'Periodo' : PeriodoParam,
    'Unidades': UnidadesParam
}

d_hojas = {
    'METADATOS': 'Descripciones y notas relativas al Dataset',
    'PARAMETRO': 'Dataset resultado de la minería, agregado por clave del Sistema Urbano Nacional, '
                 'para utilizarse en la construcción de Indicadores',
    'DATOS': ContenidoHojaDatos,
    'INTEGRIDAD': 'Revision de integridad de la información POR CLAVE DEL SUN. ' 
                  'Promedio de VAR_INTEGRIDAD de los municipios que componen una ciudad. '
                  'Si no se tiene información para el municipio, VAR_INTEGRIDAD es igual a cero',
    'EXISTENCIA': 'Revision de integridad de la información POR MUNICIPIO.',
    '     ': np.nan,
    'DESCRIPCION DE VARIABLES': np.nan
}

d_mineria = {
    '  ': np.nan,
    'DESCRIPCION DEL PROCESO DE MINERIA:': np.nan,
    'Nombre del Dataset': NomDataset,
    'Descripcion del dataset': DescDataset,
    'Disponibilidad Temporal': DispTemp,
    'Periodo de actualizacion': PeriodoAct,
    'Nivel de Desagregacion': DesagrMax,
    'Notas': Notas,
    'Fuente': NomFuente,
    'URL_Fuente': UrlFuente,
    'Dataset base': DSBase,
    'Repositorio de mineria': RepoMina,
    'VAR_INTEGRIDAD': DescVarIntegridad,
    ' ': np.nan,
    'HOJAS INCLUIDAS EN EL LIBRO': np.nan
}

descripcion_parametro = pd.DataFrame.from_dict(d_parametro, orient='index').rename(columns={0: 'DESCRIPCION'})
descripcion_mineria = pd.DataFrame.from_dict(d_mineria, orient='index').rename(columns={0: 'DESCRIPCION'})
descripcion_hojas = pd.DataFrame.from_dict(d_hojas, orient='index').rename(columns={0: 'DESCRIPCION'})
MetaParametro = descripcion_parametro.append(descripcion_mineria).append(descripcion_hojas).append(metavariables)

# Diccionario de Descripciones
DescParametro = {
    'ClaveParametro': ClaveParametro,
    'NombreParametro': NombreParametro,
    'info_completa': info_completa,
    'info_sin_info': info_sin_info,
    'info_incomple': info_incomple,
    'RutaSalida': DirDestino,
    'Clave de Dimension': ClaveDimension,
    'Nombre de Dimension': NomDimension,
    'Titulo de Columna': TituloParametro,
    'Actualizacion de datos': ActDatos
}

# Crear archivo de Excel y documentar parametro
ParametroEstandar(DescParametro, MetaParametro, Parametro, DatosLimpios, integridad_parametro, hoja_datos)
DocumentarParametro(DescParametro, MetaParametro, Parametro)
