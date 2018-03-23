# -*- coding: utf-8 -*-
"""
Started on tue, feb 09th, 2018

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
M.ClaveParametro = 'P0704'
M.NombreParametro = 'Vialidades con recubrimiento de la calle'
M.DescParam = 'Vialidades con recubrimiento de la calle (Pavimento, concreto, empedrado o adoquin)'
M.UnidadesParam = 'Numero de vialidades'
M.TituloParametro = 'Vrec'                              # Para nombrar la columna del parametro
M.PeriodoParam = '2014'
M.TipoInt = 1

# Handlings
M.ParDtype = 'float'
M.TipoVar = 'C'     # (Tipos de Variable: [C]ontinua, [D]iscreta [O]rdinal, [B]inaria o [N]ominal)
M.array = []
M.TipoAgr = 'sum'

# Descripciones del proceso de Minería
M.nomarchivodataset = M.ClaveParametro
M.extarchivodataset = 'xlsx'
M.ContenidoHojaDatos = 'Numero de vialidades según tipo de recubrimiento de la calle'
M.ClaveDataset = 'CLEU'
M.ActDatos = '2014'
M.Agregacion = 'Se agregaron a una sola columna las vialidades cuyo recubrimiento es Pavimento o concreto y Empedrado' \
               ' o adoquin. Para la agregación de datos ' \
               'municipales a ciudades del SUN, se suma el numero de vialidades en todos los municipios que integran ' \
               'cada ciudad del SUN'

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

# Generar dataset para parámetro y Variable de Integridad
pc = 'Pavimento o concreto'
ea = 'Empedrado o adoquín'
par_dataset = dataset[pc]+dataset[ea]
par_dataset = par_dataset.to_frame(name = M.ClaveParametro)
par_dataset, variables_dataset = VarInt(par_dataset, dataset, tipo=M.TipoInt)

# Compilacion
compilar(M, dataset, par_dataset, variables_dataset)