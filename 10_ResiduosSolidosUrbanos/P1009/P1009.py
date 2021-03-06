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
M.ClaveParametro = 'P1009'
M.NombreParametro = 'Número de municipios con estudios de generación de RSU'
M.DescParam = 'Número de municipios que cuentan con algún estudio sobre la generación de residuos sólidos urbanos.'
M.UnidadesParam = 'Numero de municipios'
M.TituloParametro = 'MUNERSU'                              # Para nombrar la columna del parametro
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
M.Agregacion = 'Este parámetro utiliza la variable "p12" de la base de datos del Censo Nacional de Gobiernos ' \
               'Municipales y Delegacionales 2015, que indica para cada municipio si este cuenta con estudios de ' \
               'generación de Residuos Solidos Urbanos (RSU). Se transformaron los valores de la columna de modo que:' \
               '\n1 = Cuenta con estudios,' \
               '\n0 = No Cuenta con estudios,' \
               '\nNone = Informacion no disponible.' \
               '\nPara agregar la información y construir el parámetro, se suma el valor de p12 en todos los ' \
               'municipios de los que componen cada ciudad del SUN. De este modo, el valor de P1009 indica elnumero ' \
               'de los municipios que componen la ciudad, que cuentan con estudios de generacion de RSU.'

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

# Generar dataset para parámetro y Variable de Integridad
existepgrsu = {2:0}   # Reemplaza el valor 2 por 0, a manera de que 1 = True y 0 = False
par_dataset = dataset['p12'].to_frame(name = M.ClaveParametro)
par_dataset[M.ClaveParametro] = par_dataset[M.ClaveParametro].map(existepgrsu)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
