# -*- coding: utf-8 -*-
"""
Started on wed, jul 25th, 2018
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
M.ClaveParametro = 'P0305'
M.NombreParametro = 'Superficie de la mancha urbana'
M.DescParam = 'Superficie de las localidades urbanas que componen una ciudad'
M.UnidadesParam = 'Hectareas'
M.TituloParametro = 'SUHA'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2000'
M.TipoInt = 2       # 1: Binaria; 2: Multivariable, 3: Integral

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'sum'

# Descripciones del proceso de Minería
M.nomarchivodataset = M.ClaveParametro
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Superficie Urbana en Hectareas desagregada a nivel muicipal'
M.ClaveDataset = 'SEDATU'
M.ActDatos = '2018'
M.Agregacion = 'Se sumó la superficie en hectáreas a partir de la identificación por CVE_MUN de los polígonos de ' \
               'localidades urbanas de cada ciudad' \

# Descripciones generadas desde la clave del parámetro
M.getmetafromds = 1
Meta.fillmeta(M)

# Construccion del Parámetro -----------------------------------------------------------------------------------------
# Cargar dataset inicial
dataset = pd.read_excel(M.DirFuente + '\\' + M.ArchivoDataset,
                        sheetname='DATOS', dtype={'CVE_MUN': 'str'})
dataset.set_index('CVE_MUN', inplace=True)
dataset = dataset.rename_axis('CVE_MUN')
dataset.head(2)
del(dataset['NOM_MUN'])
list(dataset)

# Generar dataset para parámetro y Variable de Integridad
var1 = 'Has'+M.PeriodoParam
par_dataset = dataset[var1]
par_dataset = dataset[var1].astype('float')
par_dataset = par_dataset.to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)
