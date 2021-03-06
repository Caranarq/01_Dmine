# -*- coding: utf-8 -*-
"""
Started on tue, feb 06th, 2018

@author: carlos.arana

"""

# Librerias utilizadas
import pandas as pd
import sys
module_path = r'D:\PCCS\01_Dmine\Scripts'
if module_path not in sys.path:
    sys.path.append(module_path)
from VarInt.VarInt import VarInt
from classes.Meta import Meta
from Compilador.Compilador import compilar

"""
Las librerias locales utilizadas renglones arriba se encuentran disponibles en las siguientes direcciones:
SCRIPT:             | DISPONIBLE EN:
------              | ------------------------------------------------------------------------------------
VarInt              | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/VarInt
Meta                | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/Classes
Compilador          | https://github.com/INECC-PCCS/01_Dmine/tree/master/Scripts/Compilador
"""

# Documentacion del Parametro ---------------------------------------------------------------------------------------
# Descripciones del Parametro
M = Meta
M.ClaveParametro = 'P1003'
M.NombreParametro = 'Número de municipios con disponibilidad de servicios relacionados con los RSU'
M.DescParam = 'Número de municipios que envian al menos una fracción de sus Residuos a plantas de tratamiento'
M.UnidadesParam = 'Numero de municipios'
M.TituloParametro = 'MUNGRSU'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2015'
M.TipoInt = 1

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'sum'

# Descripciones del proceso de Minería
M.nomarchivodataset = M.ClaveParametro
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Datos disponibles por municipio para 2015, utilizados para la construcción del parametro'
M.ClaveDataset = 'CNGMD'
M.ActDatos = '2015'
M.Agregacion = 'Este parámetro utiliza la variable "P1" y "P10" de la base de datos del Censo Nacional de Gobiernos ' \
               'Municipales y Delegacionales 2015, que indican respectivamente para cada municipio si cuenta con ' \
               'servicios de recolección si este envia al menos una parte de sus Residuos Solidos Urbanos (RSU) ' \
               'hacia una planta de tratamiento. Se transformaron los valores de cada columna de modo que:' \
               '\n1 = true' \
               '\n0 = false' \
               '\nNone = Informacion no disponible.' \
               '\nPara agregar la información y construir el parámetro, se verifica que el municipio cuente al ' \
               'menos con uno de los dos servicios. Si cuenta con alguno servicio, se asigna un valor de 1 (true) al ' \
               'municipio en la variable DSRSU. Posteriormente se realiza un conteo de todos los municipios de los ' \
               'que componen cada ciudad del SUN en donde DSRSU es igual a 1. ' \
               'De este modo, el valor de P1003 indica el numero de los municipios que componen la ciudad, que ' \
               'cuentan con estudios de generacion de RSU.'

M.getmetafromds = 1

# Descripciones generadas desde la clave del parámetro
Meta.fillmeta(M)

M.Notas = 's/n'

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(M.DirFuente + '\\' + M.ArchivoDataset,
                        sheetname=M.nomarchivodataset, dtype={'CVE_MUN': 'str'})
dataset.set_index('CVE_MUN', inplace=True)
dataset = dataset.apply(pd.to_numeric).where((pd.notnull(dataset)), None)
dataset = dataset.rename_axis('CVE_MUN')

Utiliza las dos variables del dataset. Corrigelo cuando se necesite.
# Generar dataset para parámetro y Variable de Integridad
# si_no = {2:0}   # Reemplaza el valor 2 por 0, a manera de que 1 = True y 0 = False
# par_dataset = dataset['p10'].to_frame(name = M.ClaveParametro)
# par_dataset[M.ClaveParametro] = par_dataset[M.ClaveParametro].map(si_no)
# par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
