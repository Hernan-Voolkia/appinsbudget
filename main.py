from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import warnings
import datetime
import re
import pandas as pd
import numpy as np
import sqlalchemy as db
from sqlalchemy import text, exc
import logging

from streamlit import context

import param
import paramal
import paramsuv
import paramsuval
import search
import marca
import index
import admvalue
import dbstatus

warnings.filterwarnings("ignore")
np.set_printoptions(suppress=True)

LOG_FILE_NAME = 'log.csv'
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s',filename=LOG_FILE_NAME,filemode='a')
logger = logging.getLogger(__name__)

#MARCA-MODELO
try:
    dfModelo = pd.read_csv('./data/ClaseMarcaModelo.csv',sep=';',encoding='latin-1',decimal='.',
                        dtype={'CLASE':'int16','MARCA':'int16','MODELO':'int16','DMARCA':'object','DMODELO':'object'})
except FileNotFoundError:
    logger.error(f"Error: ClaseMarcaModelo.csv no fue encontrado.")
#MARCA-MODELO-NUEVO
try:
    dfModeloNuevo = pd.read_csv('./data/ClaseMarcaModeloNuevosRed.csv',sep=';',encoding='latin-1',decimal='.',
                            dtype={'CLASE':'int16','MARCA':'int16','MODELO':'int16'})
except FileNotFoundError:
    logger.error(f"Error: ClaseMarcaModeloNuevosRed.csv no fue encontrado.")
#PORTON
try:
    dfPorton = pd.read_csv('./data/dfPortonV2.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'COD_CLASE':'int16','COD_MARCA':'int8','COD_MODELO':'int8'})
except FileNotFoundError:
    logger.error(f"Error: dfPortonV2.csv no fue encontrado.")
#SEGMENTOS
try:
    dfSEGMENTO = pd.read_csv('./data/_dfSEGMENTACION_V1.csv',sep=';',encoding='utf-8',decimal='.',
                            dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16','SEG':'int8'})
except FileNotFoundError:
    logger.error(f"Error: _dfSEGMENTACION_V1.csv no fue encontrado.")
#VALOR-REPUESTO
try:
    dfVALOR_REPUESTO_MO_Unif = pd.read_csv('./data/_dfVALOR_REPUESTO_ALL_V7.csv',sep=';',encoding='utf-8',decimal='.',parse_dates = ['FECHA'],
                            dtype = {'SEG':'int8','COD_CLASE':'int16','COD_MARCA':'int8','COD_MODELO':'int8',
                                    'COD_PARTE':'int8','DESC_ELEM':'str','PRECIO_MEAN':'float64','VIEJO':'bool'})
except FileNotFoundError:
    logger.error(f"Error: _dfVALOR_REPUESTO_ALL_V7.csv no fue encontrado.")
#VALOR-MO-FRENTE
try:
    dfVALOR_MO_UNIF_FRENTE = pd.read_csv('./data/_dfVALOR_REPARA_MO&PINT_FRENTEV7.csv',sep=';',encoding='utf-8',decimal='.',
                            dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                    'VALOR_MO_MEAN':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                    'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                    'RATIO_HS_PINT_STD':'float64','CANT_HS_PINT_STD':'float64',
                                    'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_ST':'float64',
                                    'ORIG_MAT_PINT_MEAN':'float64','ORIG_MAT_PINT_STD':'float64'})
except FileNotFoundError:
    logger.error(f"Error: _dfVALOR_REPARA_MO&PINT_FRENTEV7.csv no fue encontrado.")
#VALOR-MO-TRASERO
try:
    dfVALOR_MO_UNIF_TRASERO = pd.read_csv('./data/_dfVALOR_REPARA_MO&PINT_TRASEROV7.csv',sep=';',encoding='utf-8',decimal='.',
                            dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                    'VALOR_MO_MEAN':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                    'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                    'RATIO_HS_PINT_STD':'float64','CANT_HS_PINT_STD':'float64',
                                    'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_ST':'float64',
                                    'ORIG_MAT_PINT_MEAN':'float64','ORIG_MAT_PINT_STD':'float64'})
except FileNotFoundError:
    logger.error(f"Error: _dfVALOR_REPARA_MO&PINT_TRASEROV7.csv no fue encontrado.")
#VALOR-MO-LATERAL
try:
    dfVALOR_MO_UNIF_LATERAL = pd.read_csv('./data/_dfVALOR_REPARA_MO&PINT_LATERALV7.csv',sep=';',encoding='utf-8',decimal='.',
                            dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                    'VALOR_MO_MEAN':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                    'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                    'RATIO_HS_PINT_STD':'float64','CANT_HS_PINT_STD':'float64',
                                    'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_ST':'float64',
                                    'ORIG_MAT_PINT_MEAN':'float64','ORIG_MAT_PINT_STD':'float64'})
except FileNotFoundError:
    logger.error(f"Error: _dfVALOR_REPARA_MO&PINT_LATERALV7.csv no fue encontrado.")
#VALRO-MO-PINT-FRENTE
try:
    dfVALOR_REPUESTO_VALOR_MAT_FRENTE = pd.read_csv('./data/_dfVALOR_REPUESTO_MO&PINT_FRENTEV7.csv',sep=';',encoding='utf-8',decimal='.',
                            dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                    'VALOR_MO':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                    'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                    'RATIO_HS_PINT_MEAN':'float64','RATIO_HS_PINT_STD':'float64',
                                    'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_STD':'float64'})
except FileNotFoundError:
    logger.error(f"Error: _dfVALOR_REPUESTO_MO&PINT_FRENTEV7.csv no fue encontrado.")
#VALRO-MO-PINT-TRASERO
try:
    dfVALOR_REPUESTO_VALOR_MAT_TRASERO = pd.read_csv('./data/_dfVALOR_REPUESTO_MO&PINT_TRASEROV7.csv',sep=';',encoding='utf-8',decimal='.',
                            dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                    'VALOR_MO':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                    'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                    'RATIO_HS_PINT_MEAN':'float64','RATIO_HS_PINT_STD':'float64',
                                    'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_STD':'float64'})
except FileNotFoundError:
    logger.error(f"Error: _dfVALOR_REPUESTO_MO&PINT_TRASEROV7.csv no fue encontrado.")
#VALRO-MO-PINT-LATERAL
try:
    dfVALOR_REPUESTO_VALOR_MAT_LATERAL = pd.read_csv('./data/_dfVALOR_REPUESTO_MO&PINT_LATERALV7.csv',sep=';',encoding='utf-8',decimal='.',
                            dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                    'VALOR_MO':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                    'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                    'RATIO_HS_PINT_MEAN':'float64','RATIO_HS_PINT_STD':'float64',
                                    'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_STD':'float64'})
except FileNotFoundError:
    logger.error(f"Error: _dfVALOR_REPUESTO_MO&PINT_LATERALV7.csv no fue encontrado.")
#MOLDURAS
try:
    dfMOLDURA = pd.read_csv('./data/MolduraValueMin.csv',sep=';',encoding='utf-8',decimal='.',
                            dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                                    'COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                                    'COD_ELEM':'int64','VALOR':'float64','VIEJO':'bool'})
except FileNotFoundError:
    logger.error(f"Error: MolduraValueMin.csv no fue encontrado.")
#ESPEJO
try:
    dfESPEJO = pd.read_csv('./data/PuertaEspejoValueMin.csv',sep=';',encoding='utf-8',decimal='.',
                            dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                                    'COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                                    'COD_ELEM':'int64','VALOR': 'float64','VIEJO':'bool'})
except FileNotFoundError:
    logger.error(f"Error: PuertaEspejoValueMin.csv no fue encontrado.")
#FARO
try:
    dfFARO = pd.read_csv('./data/FaroOnlyValueMin.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                                'COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                                'COD_ELEM':'int64','VALOR': 'float64','VIEJO':'bool'})
except FileNotFoundError:
    logger.error(f"Error: FaroOnlyValueMin.csv no fue encontrado.")
#CRISTAL
try:
    dfCRISTAL = pd.read_csv('./data/PuertaCristalValueMin.csv',sep=';',encoding='utf-8',decimal='.',
                            dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                                    'COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                                    'COD_ELEM':'int64','VALOR': 'float64','VIEJO':'bool'})
except FileNotFoundError:
    logger.error(f"Error: PuertaCristalValueMin.csv no fue encontrado.")
#MANIJA
try:
    dfMANIJA = pd.read_csv('./data/PuertaManijaValueMin.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                                    'COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                                    'COD_ELEM':'int64','VALOR': 'float64','VIEJO':'bool'})
except FileNotFoundError:
    logger.error(f"Error: PuertaManijaValueMin.csv no fue encontrado.")
#MOTOS
try:
    dfMOTO = pd.read_csv('./data/motos.csv',sep=';',encoding='utf-8',na_values=['NA', '?'], on_bad_lines='warn',
                        dtype={'CLASE':int,'MARCA':int,'MODELO':int,'DMARCA':str,'DMODELO':str})
except FileNotFoundError:
    logger.error(f"Error: motos.csv no fue encontrado.")
#DBVALUES
cEnv = ""
try:
    with open('.env', 'r') as file: 
        cEnv=file.read().strip()
        #logger.info(f"ENV: {cEnv}")
except FileNotFoundError:
    logger.error(f"Error: .env no fue encontrado.")
except Exception as e:
    logger.error(f"Error: .env", exc_info=True)

if cEnv == 'PROD':
    cDBConnValue = 'postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb'
else:    
    cDBConnValue = 'sqlite:///appinsbudget.sqlite3'
engine = db.create_engine(cDBConnValue)
conn = engine.connect()
result = conn.execute(text('SELECT stname,flvalue FROM admvalue;'))
for row in result:
    if row[0] == 'Tercero'  : param.bfTercero   = float(row[1])
    if row[0] == 'MObra'    : param.bfMObra     = float(row[1])
    if row[0] == 'MOMinimo' : param.bfMOMinimo  = float(row[1])
    if row[0] == 'Pintura'  : param.bfPintura   = float(row[1])
    if row[0] == 'Ajuste'   : param.bfAjuste    = float(row[1])
    if row[0] == 'Asegurado': param.bfAsegurado = float(row[1])
conn.close()
engine.dispose()

app = FastAPI()
app.mount("/img", StaticFiles(directory="img"), name='img')
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return index.bfHTML

@app.get("/log", response_class=PlainTextResponse)
async def log(iLines:int=1):
    bfLog = leer_ultimas_lineas_log(iLines)
    return "Lines:" + str(iLines) + str(bfLog)

@app.post("/vh", response_class=PlainTextResponse)
async def modelo(CLASE  : int = 0):
    bfVH = ''
    if   CLASE == 901: bfVH = marca.bfMarca901
    elif CLASE == 907: bfVH = marca.bfMarca907
    elif CLASE == 908: bfVH = marca.bfMarca908
    return bfVH

@app.post("/modelo", response_class=PlainTextResponse)
async def modelo(CLASE:int=901, MARCA:int=0):
    bfOptions = '<option id=0></option>'
    if   CLASE == 901 or CLASE == 907:
        dfModeloSearch = dfModelo.loc[(dfModelo['CLASE']==CLASE) & (dfModelo['MARCA']==MARCA)]
    elif CLASE == 908 or CLASE == 909 or CLASE == 910 or CLASE == 911 or CLASE == 912:
        dfModeloSearch = dfMOTO.loc[(dfMOTO['MARCA']==MARCA)]

    dfModeloSearch = dfModeloSearch.sort_values(['MODELO'], ascending=[False])
    for index, row in dfModeloSearch.iterrows():
        bfOptions += "<option id=" + str(row['MODELO']) + ">" + str(row['DMODELO']) + "</option>"

    return bfOptions

@app.get("/consulta", response_class=HTMLResponse)
async def consulta():
    #TODO: Cargar todas las tablas nuevas con valores de repuetos promedio
    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvalue;'))
    for row in result:
        if row[0] == 'Tercero':   param.bfTercero   = float(row[1])
        if row[0] == 'MObra':     param.bfMObra     = float(row[1])
        if row[0] == 'MOMinimo':  param.bfMOMinimo  = float(row[1])
        if row[0] == 'Pintura':   param.bfPintura   = float(row[1])
        if row[0] == 'Ajuste':    param.bfAjuste    = float(row[1])
        if row[0] == 'Asegurado': param.bfAsegurado = float(row[1])
    conn.close()
    engine.dispose()
    
    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvalueslat;'))
    for row in result:
        if row[0] == 'Lat_Cristal_Delantero': param.bfLat_Cristal_Delantero = float(row[1])
        if row[0] == 'Lat_Cristal_Trasero':   param.bfLat_Cristal_Trasero   = float(row[1])
        if row[0] == 'Lat_Espejo_Electrico':  param.bfLat_Espejo_Electrico  = float(row[1])
        if row[0] == 'Lat_Espejo_Manual':     param.bfLat_Espejo_Manual     = float(row[1])
        if row[0] == 'Lat_Manija_Pta_Del':    param.bfLat_Manija_Pta_Del    = float(row[1])
        if row[0] == 'Lat_Manija_Pta_Tras':   param.bfLat_Manija_Pta_Tras   = float(row[1])
        if row[0] == 'Lat_Moldura_Pta_Del':   param.bfLat_Moldura_Pta_Del   = float(row[1])
        if row[0] == 'Lat_Moldura_Pta_Tras':  param.bfLat_Moldura_Pta_Tras  = float(row[1])
        if row[0] == 'Lat_Puerta_Delantera':  param.bfLat_Puerta_Delantera  = float(row[1])
        if row[0] == 'Lat_Puerta_Trasera':    param.bfLat_Puerta_Trasera    = float(row[1])
        if row[0] == 'Lat_Zocalo':            param.bfLat_Zocalo            = float(row[1])
    conn.close()
    engine.dispose()

    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvalueslatSUV;'))
    for row in result:
        if row[0] == 'Lat_Cristal_Delantero': paramsuv.bfLat_Cristal_Delantero = float(row[1])
        if row[0] == 'Lat_Cristal_Trasero':   paramsuv.bfLat_Cristal_Trasero   = float(row[1])
        if row[0] == 'Lat_Espejo_Electrico':  paramsuv.bfLat_Espejo_Electrico  = float(row[1])
        if row[0] == 'Lat_Espejo_Manual':     paramsuv.bfLat_Espejo_Manual     = float(row[1])
        if row[0] == 'Lat_Manija_Pta_Del':    paramsuv.bfLat_Manija_Pta_Del    = float(row[1])
        if row[0] == 'Lat_Manija_Pta_Tras':   paramsuv.bfLat_Manija_Pta_Tras   = float(row[1])
        if row[0] == 'Lat_Moldura_Pta_Del':   paramsuv.bfLat_Moldura_Pta_Del   = float(row[1])
        if row[0] == 'Lat_Moldura_Pta_Tras':  paramsuv.bfLat_Moldura_Pta_Tras  = float(row[1])
        if row[0] == 'Lat_Puerta_Delantera':  paramsuv.bfLat_Puerta_Delantera  = float(row[1])
        if row[0] == 'Lat_Puerta_Trasera':    paramsuv.bfLat_Puerta_Trasera    = float(row[1])
        if row[0] == 'Lat_Zocalo':            paramsuv.bfLat_Zocalo            = float(row[1])
    conn.close()
    engine.dispose()

    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvalueslatal;'))
    for row in result:
        if row[0] == 'Lat_Cristal_Delantero': paramal.bfLat_Cristal_Delantero = float(row[1])
        if row[0] == 'Lat_Cristal_Trasero':   paramal.bfLat_Cristal_Trasero   = float(row[1])
        if row[0] == 'Lat_Espejo_Electrico':  paramal.bfLat_Espejo_Electrico  = float(row[1])
        if row[0] == 'Lat_Espejo_Manual':     paramal.bfLat_Espejo_Manual     = float(row[1])
        if row[0] == 'Lat_Manija_Pta_Del':    paramal.bfLat_Manija_Pta_Del    = float(row[1])
        if row[0] == 'Lat_Manija_Pta_Tras':   paramal.bfLat_Manija_Pta_Tras   = float(row[1])
        if row[0] == 'Lat_Moldura_Pta_Del':   paramal.bfLat_Moldura_Pta_Del   = float(row[1])
        if row[0] == 'Lat_Moldura_Pta_Tras':  paramal.bfLat_Moldura_Pta_Tras  = float(row[1])
        if row[0] == 'Lat_Puerta_Delantera':  paramal.bfLat_Puerta_Delantera  = float(row[1])
        if row[0] == 'Lat_Puerta_Trasera':    paramal.bfLat_Puerta_Trasera    = float(row[1])
        if row[0] == 'Lat_Zocalo':            paramal.bfLat_Zocalo            = float(row[1])
    conn.close()
    engine.dispose()

    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvalueslatalSUV;'))
    for row in result:
        if row[0] == 'Lat_Cristal_Delantero': paramsuval.bfLat_Cristal_Delantero = float(row[1])
        if row[0] == 'Lat_Cristal_Trasero':   paramsuval.bfLat_Cristal_Trasero   = float(row[1])
        if row[0] == 'Lat_Espejo_Electrico':  paramsuval.bfLat_Espejo_Electrico  = float(row[1])
        if row[0] == 'Lat_Espejo_Manual':     paramsuval.bfLat_Espejo_Manual     = float(row[1])
        if row[0] == 'Lat_Manija_Pta_Del':    paramsuval.bfLat_Manija_Pta_Del    = float(row[1])
        if row[0] == 'Lat_Manija_Pta_Tras':   paramsuval.bfLat_Manija_Pta_Tras   = float(row[1])
        if row[0] == 'Lat_Moldura_Pta_Del':   paramsuval.bfLat_Moldura_Pta_Del   = float(row[1])
        if row[0] == 'Lat_Moldura_Pta_Tras':  paramsuval.bfLat_Moldura_Pta_Tras  = float(row[1])
        if row[0] == 'Lat_Puerta_Delantera':  paramsuval.bfLat_Puerta_Delantera  = float(row[1])
        if row[0] == 'Lat_Puerta_Trasera':    paramsuval.bfLat_Puerta_Trasera    = float(row[1])
        if row[0] == 'Lat_Zocalo':            paramsuval.bfLat_Zocalo            = float(row[1])
    conn.close()
    engine.dispose()
    
    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvaluesdel;'))
    for row in result:
        if row[0] == 'Del_Paragolpe_Ctro'   : param.bfFrt_GM_Del_Paragolpe_Ctro    = float(row[1])
        if row[0] == 'Del_Paragolpe_Rejilla': param.bfFrt_GM_Del_Paragolpe_Rejilla = float(row[1])
        if row[0] == 'Del_Paragolpe_Alma'   : param.bfFrt_GM_Del_Paragolpe_Alma    = float(row[1])
        if row[0] == 'Del_Rejilla_Radiador' : param.bfFrt_GM_Del_Rejilla_Radiador  = float(row[1])
        if row[0] == 'Del_Frente'           : param.bfFrt_GM_Del_Frente            = float(row[1])
        if row[0] == 'Del_Guardabarro'      : param.bfFrt_GM_Del_Guardabarro       = float(row[1])
        if row[0] == 'Del_Faro'             : param.bfFrt_GM_Del_Faro              = float(row[1])
        if row[0] == 'Del_Faro_Auxiliar'    : param.bfFrt_GM_Del_Faro_Auxiliar     = float(row[1])
        if row[0] == 'Del_Farito'           : param.bfFrt_GM_Del_Farito            = float(row[1])
        if row[0] == 'Del_Capot'            : param.bfFrt_GM_Del_Capot             = float(row[1])
        if row[0] == 'Del_Parabrisas'       : param.bfFrt_GM_Del_Parabrisas        = float(row[1])
    conn.close()
    engine.dispose()

    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvaluesdelSUV;'))
    for row in result:
        if row[0] == 'Del_Paragolpe_Ctro'   : paramsuv.bfFrt_GM_Del_Paragolpe_Ctro    = float(row[1])
        if row[0] == 'Del_Paragolpe_Rejilla': paramsuv.bfFrt_GM_Del_Paragolpe_Rejilla = float(row[1])
        if row[0] == 'Del_Paragolpe_Alma'   : paramsuv.bfFrt_GM_Del_Paragolpe_Alma    = float(row[1])
        if row[0] == 'Del_Rejilla_Radiador' : paramsuv.bfFrt_GM_Del_Rejilla_Radiador  = float(row[1])
        if row[0] == 'Del_Frente'           : paramsuv.bfFrt_GM_Del_Frente            = float(row[1])
        if row[0] == 'Del_Guardabarro'      : paramsuv.bfFrt_GM_Del_Guardabarro       = float(row[1])
        if row[0] == 'Del_Faro'             : paramsuv.bfFrt_GM_Del_Faro              = float(row[1])
        if row[0] == 'Del_Faro_Auxiliar'    : paramsuv.bfFrt_GM_Del_Faro_Auxiliar     = float(row[1])
        if row[0] == 'Del_Farito'           : paramsuv.bfFrt_GM_Del_Farito            = float(row[1])
        if row[0] == 'Del_Capot'            : paramsuv.bfFrt_GM_Del_Capot             = float(row[1])
        if row[0] == 'Del_Parabrisas'       : paramsuv.bfFrt_GM_Del_Parabrisas        = float(row[1])
    conn.close()
    engine.dispose()
    
    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvaluesdelal;'))
    for row in result:
        if row[0] == 'Del_Paragolpe_Ctro'   : paramal.bfFrt_GA_Del_Paragolpe_Ctro    = float(row[1])
        if row[0] == 'Del_Paragolpe_Rejilla': paramal.bfFrt_GA_Del_Paragolpe_Rejilla = float(row[1])
        if row[0] == 'Del_Paragolpe_Alma'   : paramal.bfFrt_GA_Del_Paragolpe_Alma    = float(row[1])
        if row[0] == 'Del_Rejilla_Radiador' : paramal.bfFrt_GA_Del_Rejilla_Radiador  = float(row[1])
        if row[0] == 'Del_Frente'           : paramal.bfFrt_GA_Del_Frente            = float(row[1])
        if row[0] == 'Del_Guardabarro'      : paramal.bfFrt_GA_Del_Guardabarro       = float(row[1])
        if row[0] == 'Del_Faro'             : paramal.bfFrt_GA_Del_Faro              = float(row[1])
        if row[0] == 'Del_Faro_Auxiliar'    : paramal.bfFrt_GA_Del_Faro_Auxiliar     = float(row[1])
        if row[0] == 'Del_Farito'           : paramal.bfFrt_GA_Del_Farito            = float(row[1])
        if row[0] == 'Del_Capot'            : paramal.bfFrt_GA_Del_Capot             = float(row[1])
        if row[0] == 'Del_Parabrisas'       : paramal.bfFrt_GA_Del_Parabrisas        = float(row[1])
    conn.close()
    engine.dispose()

    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvaluesdelalSUV;'))
    for row in result:
        if row[0] == 'Del_Paragolpe_Ctro'   : paramsuval.bfFrt_GA_Del_Paragolpe_Ctro    = float(row[1])
        if row[0] == 'Del_Paragolpe_Rejilla': paramsuval.bfFrt_GA_Del_Paragolpe_Rejilla = float(row[1])
        if row[0] == 'Del_Paragolpe_Alma'   : paramsuval.bfFrt_GA_Del_Paragolpe_Alma    = float(row[1])
        if row[0] == 'Del_Rejilla_Radiador' : paramsuval.bfFrt_GA_Del_Rejilla_Radiador  = float(row[1])
        if row[0] == 'Del_Frente'           : paramsuval.bfFrt_GA_Del_Frente            = float(row[1])
        if row[0] == 'Del_Guardabarro'      : paramsuval.bfFrt_GA_Del_Guardabarro       = float(row[1])
        if row[0] == 'Del_Faro'             : paramsuval.bfFrt_GA_Del_Faro              = float(row[1])
        if row[0] == 'Del_Faro_Auxiliar'    : paramsuval.bfFrt_GA_Del_Faro_Auxiliar     = float(row[1])
        if row[0] == 'Del_Farito'           : paramsuval.bfFrt_GA_Del_Farito            = float(row[1])
        if row[0] == 'Del_Capot'            : paramsuval.bfFrt_GA_Del_Capot             = float(row[1])
        if row[0] == 'Del_Parabrisas'       : paramsuval.bfFrt_GA_Del_Parabrisas        = float(row[1])
    conn.close()
    engine.dispose()
    
    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvaluestra;'))
    for row in result:
        if row[0] == 'Baul_Porton': param.bfBaul_Porton = float(row[1])
        if row[0] == 'Faro_Ext'   : param.bfFaro_Ext    = float(row[1])
        if row[0] == 'Faro_Int'   : param.bfFaro_Int    = float(row[1])
        if row[0] == 'Guardabarro': param.bfGuardabarro = float(row[1])
        if row[0] == 'Luneta'     : param.bfLuneta      = float(row[1])
        if row[0] == 'Moldura'    : param.bfMoldura     = float(row[1])
        if row[0] == 'Panel_Cola' : param.bfPanel_Cola  = float(row[1])
        if row[0] == 'Paragolpe'  : param.bfParagolpe   = float(row[1])
    conn.close()
    engine.dispose()

    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvaluestraal;'))
    for row in result:
        if row[0] == 'Baul_Porton': paramal.bfBaul_Porton = float(row[1])
        if row[0] == 'Faro_Ext'   : paramal.bfFaro_Ext    = float(row[1])
        if row[0] == 'Faro_Int'   : paramal.bfFaro_Int    = float(row[1])
        if row[0] == 'Guardabarro': paramal.bfGuardabarro = float(row[1])
        if row[0] == 'Luneta'     : paramal.bfLuneta      = float(row[1])
        if row[0] == 'Moldura'    : paramal.bfMoldura     = float(row[1])
        if row[0] == 'Panel_Cola' : paramal.bfPanel_Cola  = float(row[1])
        if row[0] == 'Paragolpe'  : paramal.bfParagolpe   = float(row[1])
    conn.close()
    engine.dispose()

    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvaluestraSUV;'))
    for row in result:
        if row[0] == 'Baul_Porton': paramsuv.bfBaul_Porton = float(row[1])
        if row[0] == 'Faro_Ext'   : paramsuv.bfFaro_Ext    = float(row[1])
        if row[0] == 'Faro_Int'   : paramsuv.bfFaro_Int    = float(row[1])
        if row[0] == 'Guardabarro': paramsuv.bfGuardabarro = float(row[1])
        if row[0] == 'Luneta'     : paramsuv.bfLuneta      = float(row[1])
        if row[0] == 'Moldura'    : paramsuv.bfMoldura     = float(row[1])
        if row[0] == 'Panel_Cola' : paramsuv.bfPanel_Cola  = float(row[1])
        if row[0] == 'Paragolpe'  : paramsuv.bfParagolpe   = float(row[1])
    conn.close()
    engine.dispose()
    
    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text('SELECT stname,flvalue FROM admvaluestraalSUV;'))
    for row in result:
        if row[0] == 'Baul_Porton': paramsuval.bfBaul_Porton = float(row[1])
        if row[0] == 'Faro_Ext'   : paramsuval.bfFaro_Ext    = float(row[1])
        if row[0] == 'Faro_Int'   : paramsuval.bfFaro_Int    = float(row[1])
        if row[0] == 'Guardabarro': paramsuval.bfGuardabarro = float(row[1])
        if row[0] == 'Luneta'     : paramsuval.bfLuneta      = float(row[1])
        if row[0] == 'Moldura'    : paramsuval.bfMoldura     = float(row[1])
        if row[0] == 'Panel_Cola' : paramsuval.bfPanel_Cola  = float(row[1])
        if row[0] == 'Paragolpe'  : paramsuval.bfParagolpe   = float(row[1])
    conn.close()
    engine.dispose()

    return search.bfHTML
##############################################################
# Reporte de Valores de Valores Genericos
##############################################################
@app.get("/admvalue", response_class=HTMLResponse)
async def adminValues():
    #DBVALUES
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT stname,flvalue FROM admvalue;'))
        for row in result:
            if row[0] == 'Tercero'  : param.bfTercero   = float(row[1])
            if row[0] == 'MObra'    : param.bfMObra     = float(row[1])
            if row[0] == 'MOMinimo' : param.bfMOMinimo  = float(row[1])
            if row[0] == 'Pintura'  : param.bfPintura   = float(row[1])
            if row[0] == 'Ajuste'   : param.bfAjuste    = float(row[1])
            if row[0] == 'Asegurado': param.bfAsegurado = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        param.bfTercero = ""
        param.bfMObra = ""
        param.bfMOMinimo = ""
        param.bfPintura = ""
        param.bfAjuste = ""
        param.bfAsegurado = ""
        logger.error(f"Error: no se puedo acceder a admvalue.")

    bfAdminValues = admvalue.bfHTML
    bfAdminValues = bfAdminValues.replace('rplBfAsegurado',str(param.bfAsegurado))
    bfAdminValues = bfAdminValues.replace('rplBfTercero',str(param.bfTercero))
    bfAdminValues = bfAdminValues.replace('rplBfMObra',str(param.bfMObra))
    bfAdminValues = bfAdminValues.replace('rplBfMOMinimo',str(param.bfMOMinimo))
    bfAdminValues = bfAdminValues.replace('rplBfPintura',str(param.bfPintura))
    bfAdminValues = bfAdminValues.replace('rplBfAjuste',str(param.bfAjuste))
    return bfAdminValues
#==========================================================
@app.post("/admvaluesave", response_class=PlainTextResponse)
async def adminValuesSave(ASEGURADO:str="",TERCERO:str="",MOBRA:str="",MOMINIMO:str="",PINTURA:str="",AJUSTE:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue);
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(TERCERO).replace(',','.') + ' WHERE stName=\'Tercero\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(ASEGURADO).replace(',','.') + ' WHERE stName=\'Asegurado\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(MOBRA).replace(',','.') + ' WHERE stName=\'MObra\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(MOMINIMO).replace(',','.') + ' WHERE stName=\'MOMinimo\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(PINTURA).replace(',','.') + ' WHERE stName=\'Pintura\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(AJUSTE).replace(',','.') + ' WHERE stName=\'Ajuste\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)
       logger.error(f"Error: admvalue - "+str(e))
    return bfMsg
##############################################################
# Reporte de Ratios Delantero
##############################################################
@app.get("/admdelratio", response_class=HTMLResponse)
async def admDelRatio(request: Request):
    context = {"request": request,
               "Capot_Ratio": "",
               "Guardabarro_Ratio":"",
               "Frente_Ratio":"",
               "Paragolpe_Alma_Ratio":"",
               "Paragolpe_Ctro_Ratio":"",
              }
    return templates.TemplateResponse("admrdel.html", context)

@app.post("/admrdelsel", response_class=HTMLResponse)
async def admrdelsel(Clase: int, Segmento: int):
    parametros_dict = {"seg": "","clase": "","stName": "","flMO": "","flPT": ""}
    ratios_from_db = {}
    conn = None  
    engine = None 
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        query = text("SELECT stname, flMO, flPT FROM admrdel WHERE clase = :clase AND seg = :seg")
        result = conn.execute(query, {"clase": Clase, "seg": Segmento})
        
        for row in result:
            stname = row.stName
            
            try:
                flmo_val = float(row.flMO)
            except (ValueError, TypeError):
                flmo_val = 0.0
                logger.warning(f"Valor 'flMO' no válido para '{stname}'. Usando 0.0.")

            try:
                flpt_val = float(row.flPT)
            except (ValueError, TypeError):
                flpt_val = 0.0
                logger.warning(f"Valor 'flPT' no válido para '{stname}'. Usando 0.0.")

            ratios_from_db[stname] = {
                "flMO": flmo_val,
                "flPT": flpt_val
            } 
                   
        if not ratios_from_db:
            logger.error(f"No se encontraron valores en la tabla admvalue para clase={Clase} y seg={Segmento}.")
        
        return JSONResponse(content=ratios_from_db)

    except Exception as e:
        logger.error(f"Error al acceder a la base de datos 'admvalue': {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail="Error interno del servidor al consultar los valores."
        )
    finally:
        if conn:
            conn.close()
            logger.debug("Conexión a la base de datos cerrada.")
        if engine:
            engine.dispose()
            logger.debug("Engine de base de datos dispuesto.")
#==========================================================
@app.post("/admrdelsave", response_class=PlainTextResponse)
async def admRDelSave(clase:str="",segmento:str="",Capot_Ratio:str="",Guardabarro_Ratio:str="",Frente_Ratio:str="",Paragolpe_Alma_Ratio:str="",Paragolpe_Ctro_Ratio:str="",Capot_Ratio_PT:str="",Guardabarro_Ratio_PT:str="",Frente_Ratio_PT:str="",Paragolpe_Alma_Ratio_PT:str="",Paragolpe_Ctro_Ratio_PT:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    engine = db.create_engine(cDBConnValue)
    with engine.begin() as conn:
        try:
            p_seg   = int(segmento) if segmento else 0
            p_clase = int(clase)    if clase else 0
            ###CAPOT M.O.###
            sql_capot = text(
                """
                UPDATE admrdel 
                SET flMO = :flmo 
                WHERE seg = :seg AND clase = :clase AND stName = :stname
                """
            )
            conn.execute(sql_capot, {
                "flmo": float(Capot_Ratio.replace(',', '.')) if Capot_Ratio else 0.0,
                "seg": p_seg,
                "clase": p_clase,
                "stname": "CAPOT"
            })
            ###GUARDABARRO M.O.###
            sql_guardabarro = text(
                """
                UPDATE admrdel 
                SET flMO = :flmo 
                WHERE seg = :seg AND clase = :clase AND stName = :stname
                """
            )
            conn.execute(sql_guardabarro, {
                "flmo": float(Guardabarro_Ratio.replace(',', '.')) if Guardabarro_Ratio else 0.0,
                "seg": p_seg,
                "clase": p_clase,
                "stname": "GUARDABARRO" 
            })
            ###FRENTE M.O.###
            sql_frente = text(
                """
                UPDATE admrdel 
                SET flMO = :flmo 
                WHERE seg = :seg AND clase = :clase AND stName = :stname
                """
            )
            conn.execute(sql_frente, {
                "flmo": float(Frente_Ratio.replace(',', '.')) if Frente_Ratio else 0.0,
                "seg": p_seg,
                "clase": p_clase,
                "stname": "FRENTE" 
            })
            ###PARAGOLPE_ALMA M.O.###
            sql_frente = text(
                """
                UPDATE admrdel 
                SET flMO = :flmo 
                WHERE seg = :seg AND clase = :clase AND stName = :stname
                """
            )
            conn.execute(sql_frente, {
                "flmo": float(Paragolpe_Alma_Ratio.replace(',', '.')) if Paragolpe_Alma_Ratio else 0.0,
                "seg": p_seg,
                "clase": p_clase,
                "stname": "PARAGOLPE_ALMA" 
            })
            ###PARAGOLPE_CTRO M.O.###
            sql_frente = text(
                """
                UPDATE admrdel 
                SET flMO = :flmo 
                WHERE seg = :seg AND clase = :clase AND stName = :stname
                """
            )
            conn.execute(sql_frente, {
                "flmo": float(Paragolpe_Ctro_Ratio.replace(',', '.')) if Paragolpe_Ctro_Ratio else 0.0,
                "seg": p_seg,
                "clase": p_clase,
                "stname": "PARAGOLPE_CTRO" 
            })
            ###CAPOT PINTURA###
            sql_capot = text(
                """
                UPDATE admrdel 
                SET flPT = :flpt 
                WHERE seg = :seg AND clase = :clase AND stName = :stname
                """
            )
            conn.execute(sql_capot, {
                "flpt": float(Capot_Ratio_PT.replace(',', '.')) if Capot_Ratio_PT else 0.0,
                "seg": p_seg,
                "clase": p_clase,
                "stname": "CAPOT"
            })
            ###GUARDABARRO PINTURA###
            sql_guardabarro = text(
                """
                UPDATE admrdel 
                SET flPT = :flpt 
                WHERE seg = :seg AND clase = :clase AND stName = :stname
                """
            )
            conn.execute(sql_guardabarro, {
                "flpt": float(Guardabarro_Ratio_PT.replace(',', '.')) if Guardabarro_Ratio_PT else 0.0,
                "seg": p_seg,
                "clase": p_clase,
                "stname": "GUARDABARRO" 
            })
            ###FRENTE PINTURA###
            sql_frente = text(
                """
                UPDATE admrdel 
                SET flPT = :flpt 
                WHERE seg = :seg AND clase = :clase AND stName = :stname
                """
            )
            conn.execute(sql_frente, {
                "flpt": float(Frente_Ratio_PT.replace(',', '.')) if Frente_Ratio_PT else 0.0,
                "seg": p_seg,
                "clase": p_clase,
                "stname": "FRENTE" 
            })
            ###PARAGOLPE_ALMA PINTURA###
            sql_frente = text(
                """
                UPDATE admrdel 
                SET flPT = :flpt 
                WHERE seg = :seg AND clase = :clase AND stName = :stname
                """
            )
            conn.execute(sql_frente, {
                "flpt": float(Paragolpe_Alma_Ratio_PT.replace(',', '.')) if Paragolpe_Alma_Ratio_PT else 0.0,
                "seg": p_seg,
                "clase": p_clase,
                "stname": "PARAGOLPE_ALMA" 
            })
            ###PARAGOLPE_CTRO PINTURA###
            sql_frente = text(
                """
                UPDATE admrdel 
                SET flPT = :flpt 
                WHERE seg = :seg AND clase = :clase AND stName = :stname
                """
            )
            conn.execute(sql_frente, {
                "flpt": float(Paragolpe_Ctro_Ratio_PT.replace(',', '.')) if Paragolpe_Ctro_Ratio_PT else 0.0,
                "seg": p_seg,
                "clase": p_clase,
                "stname": "PARAGOLPE_CTRO" 
            })

        except ValueError as e:
            bfMsg = f"Error: Uno de los valores no es un número válido. {e}"
        except Exception as e:
            bfMsg =f"Error de base de datos: {e}"
            raise    
       
    return bfMsg
##############################################################
# Reporte de Ratios Lateral
##############################################################
@app.get("/admlatratio", response_class=HTMLResponse)
async def admLatRatio(request: Request):
    #DBVALUES
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT stname,flvalue FROM admvalue;'))
        for row in result:
            if row[0] == 'Tercero'  : param.bfTercero   = float(row[1])
            if row[0] == 'MObra'    : param.bfMObra     = float(row[1])
            if row[0] == 'MOMinimo' : param.bfMOMinimo  = float(row[1])
            if row[0] == 'Pintura'  : param.bfPintura   = float(row[1])
            if row[0] == 'Ajuste'   : param.bfAjuste    = float(row[1])
            if row[0] == 'Asegurado': param.bfAsegurado = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        param.bfTercero = ""
        param.bfMObra = ""
        param.bfMOMinimo = ""
        param.bfPintura = ""
        param.bfAjuste = ""
        param.bfAsegurado = ""
        logger.error(f"Error: no se puedo acceder a admvalue.")

    bfAdminValues = admvalue.bfHTML
    bfAdminValues = bfAdminValues.replace('rplBfAsegurado',str(param.bfAsegurado))
    bfAdminValues = bfAdminValues.replace('rplBfTercero',str(param.bfTercero))
    bfAdminValues = bfAdminValues.replace('rplBfMObra',str(param.bfMObra))
    bfAdminValues = bfAdminValues.replace('rplBfMOMinimo',str(param.bfMOMinimo))
    bfAdminValues = bfAdminValues.replace('rplBfPintura',str(param.bfPintura))
    bfAdminValues = bfAdminValues.replace('rplBfAjuste',str(param.bfAjuste))
    return bfAdminValues
#==========================================================
@app.post("/admlatratiosave", response_class=PlainTextResponse)
async def admLatRatioSave(ASEGURADO:str="",TERCERO:str="",MOBRA:str="",MOMINIMO:str="",PINTURA:str="",AJUSTE:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue);
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(TERCERO).replace(',','.') + ' WHERE stName=\'Tercero\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(ASEGURADO).replace(',','.') + ' WHERE stName=\'Asegurado\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(MOBRA).replace(',','.') + ' WHERE stName=\'MObra\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(MOMINIMO).replace(',','.') + ' WHERE stName=\'MOMinimo\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(PINTURA).replace(',','.') + ' WHERE stName=\'Pintura\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(AJUSTE).replace(',','.') + ' WHERE stName=\'Ajuste\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)
       logger.error(f"Error: admvalue - "+str(e))
    return bfMsg
##############################################################
# Reporte de Ratios Trasero
##############################################################
@app.get("/admtraratio", response_class=HTMLResponse)
async def admTraRatio(request: Request):
    #DBVALUES
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT stname,flvalue FROM admvalue;'))
        for row in result:
            if row[0] == 'Tercero'  : param.bfTercero   = float(row[1])
            if row[0] == 'MObra'    : param.bfMObra     = float(row[1])
            if row[0] == 'MOMinimo' : param.bfMOMinimo  = float(row[1])
            if row[0] == 'Pintura'  : param.bfPintura   = float(row[1])
            if row[0] == 'Ajuste'   : param.bfAjuste    = float(row[1])
            if row[0] == 'Asegurado': param.bfAsegurado = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        param.bfTercero = ""
        param.bfMObra = ""
        param.bfMOMinimo = ""
        param.bfPintura = ""
        param.bfAjuste = ""
        param.bfAsegurado = ""
        logger.error(f"Error: no se puedo acceder a admvalue.")

    bfAdminValues = admvalue.bfHTML
    bfAdminValues = bfAdminValues.replace('rplBfAsegurado',str(param.bfAsegurado))
    bfAdminValues = bfAdminValues.replace('rplBfTercero',str(param.bfTercero))
    bfAdminValues = bfAdminValues.replace('rplBfMObra',str(param.bfMObra))
    bfAdminValues = bfAdminValues.replace('rplBfMOMinimo',str(param.bfMOMinimo))
    bfAdminValues = bfAdminValues.replace('rplBfPintura',str(param.bfPintura))
    bfAdminValues = bfAdminValues.replace('rplBfAjuste',str(param.bfAjuste))
    return bfAdminValues
#==========================================================
@app.post("/admtraratiosave", response_class=PlainTextResponse)
async def admTraRatioSave(ASEGURADO:str="",TERCERO:str="",MOBRA:str="",MOMINIMO:str="",PINTURA:str="",AJUSTE:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue);
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(TERCERO).replace(',','.') + ' WHERE stName=\'Tercero\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(ASEGURADO).replace(',','.') + ' WHERE stName=\'Asegurado\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(MOBRA).replace(',','.') + ' WHERE stName=\'MObra\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(MOMINIMO).replace(',','.') + ' WHERE stName=\'MOMinimo\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(PINTURA).replace(',','.') + ' WHERE stName=\'Pintura\''))
       result = conn.execute(text('UPDATE admvalue SET flValue =' + str(AJUSTE).replace(',','.') + ' WHERE stName=\'Ajuste\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)
       logger.error(f"Error: admvalue - "+str(e))
    return bfMsg
##############################################################
# Reporte de Valores de Partes Laterales
##############################################################
@app.get("/admreplat", response_class=HTMLResponse)
async def admreplat(request: Request):
    context = {"request": request,
               "Lat_Cristal_Delantero":"Cristal Delantero","Lat_Cristal_Delantero_Val":0.0,
               "Lat_Cristal_Trasero":"Cristal Trasero","Lat_Cristal_Trasero_Val":0.0,
               "Lat_Espejo_Electrico":"Espejo Eléctrico","Lat_Espejo_Eléctrico_Val":0.0,
               "Lat_Espejo_Manual":"Espejo Manual","Lat_Espejo_Manual_Val":0.0,
               "Lat_Manija_Pta_Del":"Manija Puerta Delantera","Lat_Manija_Pta_Del_Val":0.0,
               "Lat_Manija_Pta_Tras":"Manija Puerta Trasera","Lat_Manija_Pta_Tras_Val":0.0,
               "Lat_Moldura_Pta_Del":"Moldura Puerta Delantera","Lat_Moldura_Pta_Del_Val":0.0,
               "Lat_Moldura_Pta_Tras":"Moldura Puerta Trasera","Lat_Moldura_Pta_Tras_Val":0.0,
               "Lat_Puerta_Delantera":"Puerta Delantera","Lat_Puerta_Delantera_Val":0.0,
               "Lat_Puerta_Trasera":"Puerta Trasera","Lat_Puerta_Trasera_Val":0.0,
               "Lat_Zocalo":"Zocalo","Lat_Zocalo_Val":0.0,
               "MensajeRetorno":""}
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT stname,flvalue FROM admvalueslat;'))
        for row in result:
            if row[0] == 'Lat_Cristal_Delantero': context["Lat_Cristal_Delantero_Val"] = float(row[1])
            if row[0] == 'Lat_Cristal_Trasero'  : context["Lat_Cristal_Trasero_Val"] = float(row[1])
            if row[0] == 'Lat_Espejo_Electrico' : context["Lat_Espejo_Electrico_Val"] = float(row[1])
            if row[0] == 'Lat_Espejo_Manual'    : context["Lat_Espejo_Manual_Val"] = float(row[1])
            if row[0] == 'Lat_Manija_Pta_Del'   : context["Lat_Manija_Pta_Del_Val"] = float(row[1])
            if row[0] == 'Lat_Manija_Pta_Tras'  : context["Lat_Manija_Pta_Tras_Val"] = float(row[1])
            if row[0] == 'Lat_Moldura_Pta_Del'  : context["Lat_Moldura_Pta_Del_Val"] = float(row[1])
            if row[0] == 'Lat_Moldura_Pta_Tras' : context["Lat_Moldura_Pta_Tras_Val"] = float(row[1])
            if row[0] == 'Lat_Puerta_Delantera' : context["Lat_Puerta_Delantera_Val"] = float(row[1])
            if row[0] == 'Lat_Puerta_Trasera'   : context["Lat_Puerta_Trasera_Val"] = float(row[1])
            if row[0] == 'Lat_Zocalo'           : context["Lat_Zocalo_Val"] = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))
    return templates.TemplateResponse("admreplat.html", context)
#==========================================================
@app.post("/admvalueslat", response_class=PlainTextResponse)
async def admvalueslat(request: Request, Lat_Cristal_Delantero:str="",Lat_Cristal_Trasero:str="",\
                       Lat_Espejo_Electrico:str="",Lat_Espejo_Manual:str="",Lat_Manija_Pta_Del:str="",\
                       Lat_Manija_Pta_Tras:str="",Lat_Moldura_Pta_Del:str="",Lat_Moldura_Pta_Tras:str="",\
                       Lat_Puerta_Delantera:str="",Lat_Puerta_Trasera:str="",Lat_Zocalo:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue)
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Cristal_Delantero).replace(',','.') + ' WHERE stName=\'Lat_Cristal_Delantero\''))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Cristal_Trasero).replace(',','.') + ' WHERE stName=\'Lat_Cristal_Trasero\''))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Espejo_Electrico).replace(',','.') + ' WHERE stName=\'Lat_Espejo_Electrico\''))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Espejo_Manual).replace(',','.') + ' WHERE stName=\'Lat_Espejo_Manual\''))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Manija_Pta_Del).replace(',','.') + ' WHERE stName=\'Lat_Manija_Pta_Del\''))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Manija_Pta_Tras).replace(',','.') + ' WHERE stName=\'Lat_Manija_Pta_Tras\''))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Moldura_Pta_Del).replace(',','.') + ' WHERE stName=\'Lat_Moldura_Pta_Del\''))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Moldura_Pta_Tras).replace(',','.') + ' WHERE stName=\'Lat_Moldura_Pta_Tras\''))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Puerta_Trasera).replace(',','.') + ' WHERE stName=\'Lat_Puerta_Trasera\''))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Zocalo).replace(',','.') + ' WHERE stName=\'Lat_Zocalo\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar, comuniquese con el administrador " + str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
#####################################################
@app.get("/admreplatsuv", response_class=HTMLResponse)
async def admreplatsuv(request: Request):
    context = {"request": request,
               "Lat_Cristal_Delantero":"Cristal Delantero","Lat_Cristal_Delantero_Val":0.0,
               "Lat_Cristal_Trasero":"Cristal Trasero","Lat_Cristal_Trasero_Val":0.0,
               "Lat_Espejo_Electrico":"Espejo Eléctrico","Lat_Espejo_Eléctrico_Val":0.0,
               "Lat_Espejo_Manual":"Espejo Manual","Lat_Espejo_Manual_Val":0.0,
               "Lat_Manija_Pta_Del":"Manija Puerta Delantera","Lat_Manija_Pta_Del_Val":0.0,
               "Lat_Manija_Pta_Tras":"Manija Puerta Trasera","Lat_Manija_Pta_Tras_Val":0.0,
               "Lat_Moldura_Pta_Del":"Moldura Puerta Delantera","Lat_Moldura_Pta_Del_Val":0.0,
               "Lat_Moldura_Pta_Tras":"Moldura Puerta Trasera","Lat_Moldura_Pta_Tras_Val":0.0,
               "Lat_Puerta_Delantera":"Puerta Delantera","Lat_Puerta_Delantera_Val":0.0,
               "Lat_Puerta_Trasera":"Puerta Trasera","Lat_Puerta_Trasera_Val":0.0,
               "Lat_Zocalo":"Zocalo","Lat_Zocalo_Val":0.0,
               "MensajeRetorno":""}
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT stname,flvalue FROM admvalueslatsuv;'))
        for row in result:
            if row[0] == 'Lat_Cristal_Delantero': context["Lat_Cristal_Delantero_Val"] = float(row[1])
            if row[0] == 'Lat_Cristal_Trasero'  : context["Lat_Cristal_Trasero_Val"] = float(row[1])
            if row[0] == 'Lat_Espejo_Electrico' : context["Lat_Espejo_Electrico_Val"] = float(row[1])
            if row[0] == 'Lat_Espejo_Manual'    : context["Lat_Espejo_Manual_Val"] = float(row[1])
            if row[0] == 'Lat_Manija_Pta_Del'   : context["Lat_Manija_Pta_Del_Val"] = float(row[1])
            if row[0] == 'Lat_Manija_Pta_Tras'  : context["Lat_Manija_Pta_Tras_Val"] = float(row[1])
            if row[0] == 'Lat_Moldura_Pta_Del'  : context["Lat_Moldura_Pta_Del_Val"] = float(row[1])
            if row[0] == 'Lat_Moldura_Pta_Tras' : context["Lat_Moldura_Pta_Tras_Val"] = float(row[1])
            if row[0] == 'Lat_Puerta_Delantera' : context["Lat_Puerta_Delantera_Val"] = float(row[1])
            if row[0] == 'Lat_Puerta_Trasera'   : context["Lat_Puerta_Trasera_Val"] = float(row[1])
            if row[0] == 'Lat_Zocalo'           : context["Lat_Zocalo_Val"] = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))
    return templates.TemplateResponse("admreplatsuv.html", context)
#==========================================================
@app.post("/admvalueslatsuv", response_class=PlainTextResponse)
async def admvalueslatsuv(request: Request, Lat_Cristal_Delantero:str="",Lat_Cristal_Trasero:str="",\
                         Lat_Espejo_Electrico:str="",Lat_Espejo_Manual:str="",Lat_Manija_Pta_Del:str="",\
                         Lat_Manija_Pta_Tras:str="",Lat_Moldura_Pta_Del:str="",Lat_Moldura_Pta_Tras:str="",\
                         Lat_Puerta_Delantera:str="",Lat_Puerta_Trasera:str="",Lat_Zocalo:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue)
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvalueslatsuv SET flValue =' + str(Lat_Cristal_Delantero).replace(',','.') + ' WHERE stName=\'Lat_Cristal_Delantero\''))
       result = conn.execute(text('UPDATE admvalueslatsuv SET flValue =' + str(Lat_Cristal_Trasero).replace(',','.') + ' WHERE stName=\'Lat_Cristal_Trasero\''))
       result = conn.execute(text('UPDATE admvalueslatsuv SET flValue =' + str(Lat_Espejo_Electrico).replace(',','.') + ' WHERE stName=\'Lat_Espejo_Electrico\''))
       result = conn.execute(text('UPDATE admvalueslatsuv SET flValue =' + str(Lat_Espejo_Manual).replace(',','.') + ' WHERE stName=\'Lat_Espejo_Manual\''))
       result = conn.execute(text('UPDATE admvalueslatsuv SET flValue =' + str(Lat_Manija_Pta_Del).replace(',','.') + ' WHERE stName=\'Lat_Manija_Pta_Del\''))
       result = conn.execute(text('UPDATE admvalueslatsuv SET flValue =' + str(Lat_Manija_Pta_Tras).replace(',','.') + ' WHERE stName=\'Lat_Manija_Pta_Tras\''))
       result = conn.execute(text('UPDATE admvalueslatsuv SET flValue =' + str(Lat_Moldura_Pta_Del).replace(',','.') + ' WHERE stName=\'Lat_Moldura_Pta_Del\''))
       result = conn.execute(text('UPDATE admvalueslatsuv SET flValue =' + str(Lat_Moldura_Pta_Tras).replace(',','.') + ' WHERE stName=\'Lat_Moldura_Pta_Tras\''))
       result = conn.execute(text('UPDATE admvalueslatsuv SET flValue =' + str(Lat_Puerta_Delantera).replace(',','.') + ' WHERE stName=\'Lat_Puerta_Delantera\''))
       result = conn.execute(text('UPDATE admvalueslatsuv SET flValue =' + str(Lat_Puerta_Trasera).replace(',','.') + ' WHERE stName=\'Lat_Puerta_Trasera\''))
       result = conn.execute(text('UPDATE admvalueslatsuv SET flValue =' + str(Lat_Zocalo).replace(',','.') + ' WHERE stName=\'Lat_Zocalo\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar, comuniquese con el administrador " + str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
####################################################
@app.get("/admreplatag", response_class=HTMLResponse)
async def admreplatag(request: Request):
    context = {"request": request,
               "Lat_Cristal_Delantero":"Cristal Delantero","Lat_Cristal_Delantero_Val":0.0,
               "Lat_Cristal_Trasero":"Cristal Trasero","Lat_Cristal_Trasero_Val":0.0,
               "Lat_Espejo_Electrico":"Espejo Eléctrico","Lat_Espejo_Eléctrico_Val":0.0,
               "Lat_Espejo_Manual":"Espejo Manual","Lat_Espejo_Manual_Val":0.0,
               "Lat_Manija_Pta_Del":"Manija Puerta Delantera","Lat_Manija_Pta_Del_Val":0.0,
               "Lat_Manija_Pta_Tras":"Manija Puerta Trasera","Lat_Manija_Pta_Tras_Val":0.0,
               "Lat_Moldura_Pta_Del":"Moldura Puerta Delantera","Lat_Moldura_Pta_Del_Val":0.0,
               "Lat_Moldura_Pta_Tras":"Moldura Puerta Trasera","Lat_Moldura_Pta_Tras_Val":0.0,
               "Lat_Puerta_Delantera":"Puerta Delantera","Lat_Puerta_Delantera_Val":0.0,
               "Lat_Puerta_Trasera":"Puerta Trasera","Lat_Puerta_Trasera_Val":0.0,
               "Lat_Zocalo":"Zocalo","Lat_Zocalo_Val":0.0,
               "MensajeRetorno":""}
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT stname,flvalue FROM admvalueslatal;'))
        for row in result:
            if row[0] == 'Lat_Cristal_Delantero': context["Lat_Cristal_Delantero_Val"] = float(row[1])
            if row[0] == 'Lat_Cristal_Trasero'  : context["Lat_Cristal_Trasero_Val"] = float(row[1])
            if row[0] == 'Lat_Espejo_Electrico' : context["Lat_Espejo_Electrico_Val"] = float(row[1])
            if row[0] == 'Lat_Espejo_Manual'    : context["Lat_Espejo_Manual_Val"] = float(row[1])
            if row[0] == 'Lat_Manija_Pta_Del'   : context["Lat_Manija_Pta_Del_Val"] = float(row[1])
            if row[0] == 'Lat_Manija_Pta_Tras'  : context["Lat_Manija_Pta_Tras_Val"] = float(row[1])
            if row[0] == 'Lat_Moldura_Pta_Del'  : context["Lat_Moldura_Pta_Del_Val"] = float(row[1])
            if row[0] == 'Lat_Moldura_Pta_Tras' : context["Lat_Moldura_Pta_Tras_Val"] = float(row[1])
            if row[0] == 'Lat_Puerta_Delantera' : context["Lat_Puerta_Delantera_Val"] = float(row[1])
            if row[0] == 'Lat_Puerta_Trasera'   : context["Lat_Puerta_Trasera_Val"] = float(row[1])
            if row[0] == 'Lat_Zocalo'           : context["Lat_Zocalo_Val"] = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))
    return templates.TemplateResponse("admreplatag.html", context)
#==========================================================
@app.post("/admvalueslatag", response_class=PlainTextResponse)
async def admvalueslatag(request: Request, Lat_Cristal_Delantero:str="",Lat_Cristal_Trasero:str="",\
                         Lat_Espejo_Electrico:str="",Lat_Espejo_Manual:str="",Lat_Manija_Pta_Del:str="",\
                         Lat_Manija_Pta_Tras:str="",Lat_Moldura_Pta_Del:str="",Lat_Moldura_Pta_Tras:str="",\
                         Lat_Puerta_Delantera:str="",Lat_Puerta_Trasera:str="",Lat_Zocalo:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue)
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvalueslatal SET flValue =' + str(Lat_Cristal_Delantero).replace(',','.') + ' WHERE stName=\'Lat_Cristal_Delantero\''))
       result = conn.execute(text('UPDATE admvalueslatal SET flValue =' + str(Lat_Cristal_Trasero).replace(',','.') + ' WHERE stName=\'Lat_Cristal_Trasero\''))
       result = conn.execute(text('UPDATE admvalueslatal SET flValue =' + str(Lat_Espejo_Electrico).replace(',','.') + ' WHERE stName=\'Lat_Espejo_Electrico\''))
       result = conn.execute(text('UPDATE admvalueslatal SET flValue =' + str(Lat_Espejo_Manual).replace(',','.') + ' WHERE stName=\'Lat_Espejo_Manual\''))
       result = conn.execute(text('UPDATE admvalueslatal SET flValue =' + str(Lat_Manija_Pta_Del).replace(',','.') + ' WHERE stName=\'Lat_Manija_Pta_Del\''))
       result = conn.execute(text('UPDATE admvalueslatal SET flValue =' + str(Lat_Manija_Pta_Tras).replace(',','.') + ' WHERE stName=\'Lat_Manija_Pta_Tras\''))
       result = conn.execute(text('UPDATE admvalueslatal SET flValue =' + str(Lat_Moldura_Pta_Del).replace(',','.') + ' WHERE stName=\'Lat_Moldura_Pta_Del\''))
       result = conn.execute(text('UPDATE admvalueslatal SET flValue =' + str(Lat_Moldura_Pta_Tras).replace(',','.') + ' WHERE stName=\'Lat_Moldura_Pta_Tras\''))
       result = conn.execute(text('UPDATE admvalueslatal SET flValue =' + str(Lat_Puerta_Delantera).replace(',','.') + ' WHERE stName=\'Lat_Puerta_Delantera\''))
       result = conn.execute(text('UPDATE admvalueslatal SET flValue =' + str(Lat_Puerta_Trasera).replace(',','.') + ' WHERE stName=\'Lat_Puerta_Trasera\''))
       result = conn.execute(text('UPDATE admvalueslatal SET flValue =' + str(Lat_Zocalo).replace(',','.') + ' WHERE stName=\'Lat_Zocalo\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar, comuniquese con el administrador " + str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
########################################################
@app.get("/admreplatagsuv", response_class=HTMLResponse)
async def admreplatag(request: Request):
    context = {"request": request,
               "Lat_Cristal_Delantero":"Cristal Delantero","Lat_Cristal_Delantero_Val":0.0,
               "Lat_Cristal_Trasero":"Cristal Trasero","Lat_Cristal_Trasero_Val":0.0,
               "Lat_Espejo_Electrico":"Espejo Eléctrico","Lat_Espejo_Eléctrico_Val":0.0,
               "Lat_Espejo_Manual":"Espejo Manual","Lat_Espejo_Manual_Val":0.0,
               "Lat_Manija_Pta_Del":"Manija Puerta Delantera","Lat_Manija_Pta_Del_Val":0.0,
               "Lat_Manija_Pta_Tras":"Manija Puerta Trasera","Lat_Manija_Pta_Tras_Val":0.0,
               "Lat_Moldura_Pta_Del":"Moldura Puerta Delantera","Lat_Moldura_Pta_Del_Val":0.0,
               "Lat_Moldura_Pta_Tras":"Moldura Puerta Trasera","Lat_Moldura_Pta_Tras_Val":0.0,
               "Lat_Puerta_Delantera":"Puerta Delantera","Lat_Puerta_Delantera_Val":0.0,
               "Lat_Puerta_Trasera":"Puerta Trasera","Lat_Puerta_Trasera_Val":0.0,
               "Lat_Zocalo":"Zocalo","Lat_Zocalo_Val":0.0,
               "MensajeRetorno":""}
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT stname,flvalue FROM admvalueslatalsuv;'))
        for row in result:
            if row[0] == 'Lat_Cristal_Delantero': context["Lat_Cristal_Delantero_Val"] = float(row[1])
            if row[0] == 'Lat_Cristal_Trasero'  : context["Lat_Cristal_Trasero_Val"] = float(row[1])
            if row[0] == 'Lat_Espejo_Electrico' : context["Lat_Espejo_Electrico_Val"] = float(row[1])
            if row[0] == 'Lat_Espejo_Manual'    : context["Lat_Espejo_Manual_Val"] = float(row[1])
            if row[0] == 'Lat_Manija_Pta_Del'   : context["Lat_Manija_Pta_Del_Val"] = float(row[1])
            if row[0] == 'Lat_Manija_Pta_Tras'  : context["Lat_Manija_Pta_Tras_Val"] = float(row[1])
            if row[0] == 'Lat_Moldura_Pta_Del'  : context["Lat_Moldura_Pta_Del_Val"] = float(row[1])
            if row[0] == 'Lat_Moldura_Pta_Tras' : context["Lat_Moldura_Pta_Tras_Val"] = float(row[1])
            if row[0] == 'Lat_Puerta_Delantera' : context["Lat_Puerta_Delantera_Val"] = float(row[1])
            if row[0] == 'Lat_Puerta_Trasera'   : context["Lat_Puerta_Trasera_Val"] = float(row[1])
            if row[0] == 'Lat_Zocalo'           : context["Lat_Zocalo_Val"] = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))
    return templates.TemplateResponse("admreplatagsuv.html", context)
#==========================================================
@app.post("/admvalueslatagsuv", response_class=PlainTextResponse)
async def admvalueslatagsuv(request: Request, Lat_Cristal_Delantero:str="",Lat_Cristal_Trasero:str="",\
                           Lat_Espejo_Electrico:str="",Lat_Espejo_Manual:str="",Lat_Manija_Pta_Del:str="",\
                           Lat_Manija_Pta_Tras:str="",Lat_Moldura_Pta_Del:str="",Lat_Moldura_Pta_Tras:str="",\
                           Lat_Puerta_Delantera:str="",Lat_Puerta_Trasera:str="",Lat_Zocalo:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue)
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvalueslatalsuv SET flValue =' + str(Lat_Cristal_Delantero).replace(',','.') + ' WHERE stName=\'Lat_Cristal_Delantero\''))
       result = conn.execute(text('UPDATE admvalueslatalsuv SET flValue =' + str(Lat_Cristal_Trasero).replace(',','.') + ' WHERE stName=\'Lat_Cristal_Trasero\''))
       result = conn.execute(text('UPDATE admvalueslatalsuv SET flValue =' + str(Lat_Espejo_Electrico).replace(',','.') + ' WHERE stName=\'Lat_Espejo_Electrico\''))
       result = conn.execute(text('UPDATE admvalueslatalsuv SET flValue =' + str(Lat_Espejo_Manual).replace(',','.') + ' WHERE stName=\'Lat_Espejo_Manual\''))
       result = conn.execute(text('UPDATE admvalueslatalsuv SET flValue =' + str(Lat_Manija_Pta_Del).replace(',','.') + ' WHERE stName=\'Lat_Manija_Pta_Del\''))
       result = conn.execute(text('UPDATE admvalueslatalsuv SET flValue =' + str(Lat_Manija_Pta_Tras).replace(',','.') + ' WHERE stName=\'Lat_Manija_Pta_Tras\''))
       result = conn.execute(text('UPDATE admvalueslatalsuv SET flValue =' + str(Lat_Moldura_Pta_Del).replace(',','.') + ' WHERE stName=\'Lat_Moldura_Pta_Del\''))
       result = conn.execute(text('UPDATE admvalueslatalsuv SET flValue =' + str(Lat_Moldura_Pta_Tras).replace(',','.') + ' WHERE stName=\'Lat_Moldura_Pta_Tras\''))
       result = conn.execute(text('UPDATE admvalueslatalsuv SET flValue =' + str(Lat_Puerta_Delantera).replace(',','.') + ' WHERE stName=\'Lat_Puerta_Delantera\''))
       result = conn.execute(text('UPDATE admvalueslatalsuv SET flValue =' + str(Lat_Puerta_Trasera).replace(',','.') + ' WHERE stName=\'Lat_Puerta_Trasera\''))
       result = conn.execute(text('UPDATE admvalueslatalsuv SET flValue =' + str(Lat_Zocalo).replace(',','.') + ' WHERE stName=\'Lat_Zocalo\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar, comuniquese con el administrador " + str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
##############################################################
# Reporte de Valores de Partes Traseras
##############################################################
@app.get("/admreptra", response_class=HTMLResponse)
async def admreptra(request: Request):
    context = {"request": request,
               "Baul_Porton":"Baul Portón","Baul_Porton_Val":0.0,
               "Faro_Ext":"Faro Externo","Faro_Ext_Val":0.0,
               "Faro_Int":"Faro Interno","Faro_Int_Val":0.0,
               "Guardabarro":"Guardabarro","Guardabarro_Val":0.0,
               "Luneta":"Luneta","Luneta_Val":0.0,
               "Moldura":"Moldura","Moldura_Val":0.0,
               "Panel_Cola":"Panel Cola","Panel_Cola_Val":0.0,
               "Paragolpe":"Paragolpe","Paragolpe_Val":0.0,
               "MensajeRetorno":""
               }
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT * FROM admvaluestra;'))
        for row in result:
            if row[0] == 'Baul_Porton': context["Baul_Porton_Val"]= float(row[1])
            if row[0] == 'Faro_Ext'   : context["Faro_Ext_Val"]   = float(row[1])
            if row[0] == 'Faro_Int'   : context["Faro_Int_Val"]   = float(row[1])
            if row[0] == 'Guardabarro': context["Guardabarro_Val"]= float(row[1])
            if row[0] == 'Luneta'     : context["Luneta_Val"]     = float(row[1])
            if row[0] == 'Moldura'    : context["Moldura_Val"]    = float(row[1])
            if row[0] == 'Panel_Cola' : context["Panel_Cola_Val"] = float(row[1])
            if row[0] == 'Paragolpe'  : context["Paragolpe_Val"]  = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))

    return templates.TemplateResponse("admreptra.html", context)
#===========================================================
@app.post("/admvaluestra", response_class=PlainTextResponse)
async def admvaluestra(Baul_Porton:str="",Faro_Ext:str="",Faro_Int:str="",Guardabarro:str="",Luneta:str="",\
                      Moldura:str="",Panel_Cola:str="",Paragolpe:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue);
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Baul_Porton).replace(',','.') + ' WHERE stName=\'Baul_Porton\''))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Faro_Ext).replace(',','.') + ' WHERE stName=\'Faro_Ext\''))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Faro_Int).replace(',','.') + ' WHERE stName=\'Faro_Int\''))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Guardabarro).replace(',','.') + ' WHERE stName=\'Guardabarro\''))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Luneta).replace(',','.') + ' WHERE stName=\'Luneta\''))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Moldura).replace(',','.') + ' WHERE stName=\'Moldura\''))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Panel_Cola).replace(',','.') + ' WHERE stName=\'Panel_Cola\''))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Paragolpe).replace(',','.') + ' WHERE stName=\'Paragolpe\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
######################################################
@app.get("/admreptrasuv", response_class=HTMLResponse)
async def admreptrasuv(request: Request):
    context = {"request": request,
               "Baul_Porton":"Baul Portón","Baul_Porton_Val":0.0,
               "Faro_Ext":"Faro Externo","Faro_Ext_Val":0.0,
               "Faro_Int":"Faro Interno","Faro_Int_Val":0.0,
               "Guardabarro":"Guardabarro","Guardabarro_Val":0.0,
               "Luneta":"Luneta","Luneta_Val":0.0,
               "Moldura":"Moldura","Moldura_Val":0.0,
               "Panel_Cola":"Panel Cola","Panel_Cola_Val":0.0,
               "Paragolpe":"Paragolpe","Paragolpe_Val":0.0,
               "MensajeRetorno":""
               }
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT * FROM admvaluestrasuv;'))
        for row in result:
            if row[0] == 'Baul_Porton': context["Baul_Porton_Val"]= float(row[1])
            if row[0] == 'Faro_Ext'   : context["Faro_Ext_Val"]   = float(row[1])
            if row[0] == 'Faro_Int'   : context["Faro_Int_Val"]   = float(row[1])
            if row[0] == 'Guardabarro': context["Guardabarro_Val"]= float(row[1])
            if row[0] == 'Luneta'     : context["Luneta_Val"]     = float(row[1])
            if row[0] == 'Moldura'    : context["Moldura_Val"]    = float(row[1])
            if row[0] == 'Panel_Cola' : context["Panel_Cola_Val"] = float(row[1])
            if row[0] == 'Paragolpe'  : context["Paragolpe_Val"]  = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))
    return templates.TemplateResponse("admreptrasuv.html", context)
#=============================================================
@app.post("/admvaluestrasuv", response_class=PlainTextResponse)
async def admvaluestrasuv(Baul_Porton:str="",Faro_Ext:str="",Faro_Int:str="",Guardabarro:str="",Luneta:str="",\
                          Moldura:str="",Panel_Cola:str="",Paragolpe:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue);
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvaluestrasuv SET flValue =' + str(Baul_Porton).replace(',','.') + ' WHERE stName=\'Baul_Porton\''))
       result = conn.execute(text('UPDATE admvaluestrasuv SET flValue =' + str(Faro_Ext).replace(',','.') + ' WHERE stName=\'Faro_Ext\''))
       result = conn.execute(text('UPDATE admvaluestrasuv SET flValue =' + str(Faro_Int).replace(',','.') + ' WHERE stName=\'Faro_Int\''))
       result = conn.execute(text('UPDATE admvaluestrasuv SET flValue =' + str(Guardabarro).replace(',','.') + ' WHERE stName=\'Guardabarro\''))
       result = conn.execute(text('UPDATE admvaluestrasuv SET flValue =' + str(Luneta).replace(',','.') + ' WHERE stName=\'Luneta\''))
       result = conn.execute(text('UPDATE admvaluestrasuv SET flValue =' + str(Moldura).replace(',','.') + ' WHERE stName=\'Moldura\''))
       result = conn.execute(text('UPDATE admvaluestrasuv SET flValue =' + str(Panel_Cola).replace(',','.') + ' WHERE stName=\'Panel_Cola\''))
       result = conn.execute(text('UPDATE admvaluestrasuv SET flValue =' + str(Paragolpe).replace(',','.') + ' WHERE stName=\'Paragolpe\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
#####################################################
@app.get("/admreptraag", response_class=HTMLResponse)
async def admreptraag(request: Request):
    context = {"request": request,
               "Baul_Porton":"Baul Portón","Baul_Porton_Val":0.0,
               "Faro_Ext":"Faro Externo","Faro_Ext_Val":0.0,
               "Faro_Int":"Faro Interno","Faro_Int_Val":0.0,
               "Guardabarro":"Guardabarro","Guardabarro_Val":0.0,
               "Luneta":"Luneta","Luneta_Val":0.0,
               "Moldura":"Moldura","Moldura_Val":0.0,
               "Panel_Cola":"Panel Cola","Panel_Cola_Val":0.0,
               "Paragolpe":"Paragolpe","Paragolpe_Val":0.0,
               "MensajeRetorno":""
               }
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT * FROM admvaluestraal;'))
        for row in result:
            if row[0] == 'Baul_Porton': context["Baul_Porton_Val"]= float(row[1])
            if row[0] == 'Faro_Ext'   : context["Faro_Ext_Val"]   = float(row[1])
            if row[0] == 'Faro_Int'   : context["Faro_Int_Val"]   = float(row[1])
            if row[0] == 'Guardabarro': context["Guardabarro_Val"]= float(row[1])
            if row[0] == 'Luneta'     : context["Luneta_Val"]     = float(row[1])
            if row[0] == 'Moldura'    : context["Moldura_Val"]    = float(row[1])
            if row[0] == 'Panel_Cola' : context["Panel_Cola_Val"] = float(row[1])
            if row[0] == 'Paragolpe'  : context["Paragolpe_Val"]  = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))
    return templates.TemplateResponse("admreptraag.html", context)
#==========================================================
@app.post("/admvaluestraag", response_class=PlainTextResponse)
async def admvaluestraag(Baul_Porton:str="",Faro_Ext:str="",Faro_Int:str="",Guardabarro:str="",Luneta:str="",\
                         Moldura:str="",Panel_Cola:str="",Paragolpe:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue);
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvaluestraal SET flValue =' + str(Baul_Porton).replace(',','.') + ' WHERE stName=\'Baul_Porton\''))
       result = conn.execute(text('UPDATE admvaluestraal SET flValue =' + str(Faro_Ext).replace(',','.') + ' WHERE stName=\'Faro_Ext\''))
       result = conn.execute(text('UPDATE admvaluestraal SET flValue =' + str(Faro_Int).replace(',','.') + ' WHERE stName=\'Faro_Int\''))
       result = conn.execute(text('UPDATE admvaluestraal SET flValue =' + str(Guardabarro).replace(',','.') + ' WHERE stName=\'Guardabarro\''))
       result = conn.execute(text('UPDATE admvaluestraal SET flValue =' + str(Luneta).replace(',','.') + ' WHERE stName=\'Luneta\''))
       result = conn.execute(text('UPDATE admvaluestraal SET flValue =' + str(Moldura).replace(',','.') + ' WHERE stName=\'Moldura\''))
       result = conn.execute(text('UPDATE admvaluestraal SET flValue =' + str(Panel_Cola).replace(',','.') + ' WHERE stName=\'Panel_Cola\''))
       result = conn.execute(text('UPDATE admvaluestraal SET flValue =' + str(Paragolpe).replace(',','.') + ' WHERE stName=\'Paragolpe\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
#######################################################
@app.get("/admreptraagsuv", response_class=HTMLResponse)
async def admreptraagsuv(request: Request):
    context = {"request": request,
               "Baul_Porton":"Baul Portón","Baul_Porton_Val":0.0,
               "Faro_Ext":"Faro Externo","Faro_Ext_Val":0.0,
               "Faro_Int":"Faro Interno","Faro_Int_Val":0.0,
               "Guardabarro":"Guardabarro","Guardabarro_Val":0.0,
               "Luneta":"Luneta","Luneta_Val":0.0,
               "Moldura":"Moldura","Moldura_Val":0.0,
               "Panel_Cola":"Panel Cola","Panel_Cola_Val":0.0,
               "Paragolpe":"Paragolpe","Paragolpe_Val":0.0,
               "MensajeRetorno":""
               }
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT * FROM admvaluestraalsuv;'))
        for row in result:
            if row[0] == 'Baul_Porton': context["Baul_Porton_Val"]= float(row[1])
            if row[0] == 'Faro_Ext'   : context["Faro_Ext_Val"]   = float(row[1])
            if row[0] == 'Faro_Int'   : context["Faro_Int_Val"]   = float(row[1])
            if row[0] == 'Guardabarro': context["Guardabarro_Val"]= float(row[1])
            if row[0] == 'Luneta'     : context["Luneta_Val"]     = float(row[1])
            if row[0] == 'Moldura'    : context["Moldura_Val"]    = float(row[1])
            if row[0] == 'Panel_Cola' : context["Panel_Cola_Val"] = float(row[1])
            if row[0] == 'Paragolpe'  : context["Paragolpe_Val"]  = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))
    return templates.TemplateResponse("admreptraagsuv.html", context)
#=============================================================
@app.post("/admvaluestraagsuv", response_class=PlainTextResponse)
async def admvaluestraagsuv(Baul_Porton:str="",Faro_Ext:str="",Faro_Int:str="",Guardabarro:str="",Luneta:str="",\
                         Moldura:str="",Panel_Cola:str="",Paragolpe:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue);
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvaluestraalsuv SET flValue =' + str(Baul_Porton).replace(',','.') + ' WHERE stName=\'Baul_Porton\''))
       result = conn.execute(text('UPDATE admvaluestraalsuv SET flValue =' + str(Faro_Ext).replace(',','.') + ' WHERE stName=\'Faro_Ext\''))
       result = conn.execute(text('UPDATE admvaluestraalsuv SET flValue =' + str(Faro_Int).replace(',','.') + ' WHERE stName=\'Faro_Int\''))
       result = conn.execute(text('UPDATE admvaluestraalsuv SET flValue =' + str(Guardabarro).replace(',','.') + ' WHERE stName=\'Guardabarro\''))
       result = conn.execute(text('UPDATE admvaluestraalsuv SET flValue =' + str(Luneta).replace(',','.') + ' WHERE stName=\'Luneta\''))
       result = conn.execute(text('UPDATE admvaluestraalsuv SET flValue =' + str(Moldura).replace(',','.') + ' WHERE stName=\'Moldura\''))
       result = conn.execute(text('UPDATE admvaluestraalsuv SET flValue =' + str(Panel_Cola).replace(',','.') + ' WHERE stName=\'Panel_Cola\''))
       result = conn.execute(text('UPDATE admvaluestraalsuv SET flValue =' + str(Paragolpe).replace(',','.') + ' WHERE stName=\'Paragolpe\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
######################################################
# Reporte de Valores de Partes Delanteras
######################################################
@app.get("/admrepdel", response_class=HTMLResponse)
async def admrepdel(request: Request):
    context = {"request": request,
               "Paragolpe_Ctro":"Paragolpe Centro"      ,"Paragolpe_Ctro_Val":0.0,
               "Paragolpe_Rejilla":"Paragolpe Rejilla"  ,"Paragolpe_Rejilla_Val":0.0,
               "Paragolpe_Alma":"Paragolpe Alma"        ,"Paragolpe_Alma_Val":0.0,
               "Rejilla_Radiador":"Rejilla Radiador"    ,"Rejilla_Radiador_Val":0.0,
               "Frente":"Frente"                        ,"Frente_Val":0.0,
               "Guardabarro":"Guardabarro"              ,"Guardabarro_Val":0.0,
               "Faro":"Faro"                            ,"Faro_Val":0.0,
               "Faro_Auxiliar":"Faro Auxiliar"          ,"Faro_Auxiliar_Val":0.0,
               "Farito":"Farito"                        ,"Farito_Val":0.0,
               "Capot":"Capot"                          ,"Capot_Val":0.0,
               "Parabrisas":"Parabrisas"                ,"Parabrisas_Val":0.0,
               "MensajeRetorno":""
               }
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT * FROM admvaluesdel;'))
        for row in result:
            if row[0] == 'Del_Paragolpe_Ctro'    : context["Paragolpe_Ctro_Val"]    = float(row[1])
            if row[0] == 'Del_Paragolpe_Rejilla' : context["Paragolpe_Rejilla_Val"] = float(row[1])
            if row[0] == 'Del_Paragolpe_Alma'    : context["Paragolpe_Alma_Val"]    = float(row[1])
            if row[0] == 'Del_Rejilla_Radiador'  : context["Rejilla_Radiador_Val"]  = float(row[1])
            if row[0] == 'Del_Frente'            : context["Frente_Val"]            = float(row[1])
            if row[0] == 'Del_Guardabarro'       : context["Guardabarro_Val"]       = float(row[1])
            if row[0] == 'Del_Faro'              : context["Faro_Val"]              = float(row[1])
            if row[0] == 'Del_Faro_Auxiliar'     : context["Faro_Auxiliar_Val"]     = float(row[1])
            if row[0] == 'Del_Farito'            : context["Farito_Val"]            = float(row[1])
            if row[0] == 'Del_Capot'             : context["Capot_Val"]             = float(row[1])
            if row[0] == 'Del_Parabrisas'        : context["Parabrisas_Val"]        = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))
    return templates.TemplateResponse("admrepdel.html", context)
#===========================================================
@app.post("/admvaluesdel", response_class=PlainTextResponse)
async def admvaluesdel(Paragolpe_Ctro:str="",Paragolpe_Rejilla:str="",Paragolpe_Alma:str="",Rejilla_Radiador:str="",Frente:str="",\
                      Guardabarro:str="",Faro:str="",Faro_Auxiliar:str="",Farito:str="",Capot:str="",Parabrisas:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue);
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvaluesdel SET flValue =' + str(Paragolpe_Ctro).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Ctro\''))
       result = conn.execute(text('UPDATE admvaluesdel SET flValue =' + str(Paragolpe_Rejilla).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Rejilla\''))
       result = conn.execute(text('UPDATE admvaluesdel SET flValue =' + str(Paragolpe_Alma).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Alma\''))
       result = conn.execute(text('UPDATE admvaluesdel SET flValue =' + str(Rejilla_Radiador).replace(',','.') + ' WHERE stName=\'Del_Rejilla_Radiador\''))
       result = conn.execute(text('UPDATE admvaluesdel SET flValue =' + str(Frente).replace(',','.') + ' WHERE stName=\'Del_Frente\''))
       result = conn.execute(text('UPDATE admvaluesdel SET flValue =' + str(Guardabarro).replace(',','.') + ' WHERE stName=\'Del_Guardabarro\''))
       result = conn.execute(text('UPDATE admvaluesdel SET flValue =' + str(Faro).replace(',','.') + ' WHERE stName=\'Del_Faro\''))
       result = conn.execute(text('UPDATE admvaluesdel SET flValue =' + str(Faro_Auxiliar).replace(',','.') + ' WHERE stName=\'Del_Faro_Auxiliar\''))
       result = conn.execute(text('UPDATE admvaluesdel SET flValue =' + str(Farito).replace(',','.') + ' WHERE stName=\'Del_Farito\''))
       result = conn.execute(text('UPDATE admvaluesdel SET flValue =' + str(Capot).replace(',','.') + ' WHERE stName=\'Del_Capot\''))
       result = conn.execute(text('UPDATE admvaluesdel SET flValue =' + str(Parabrisas).replace(',','.') + ' WHERE stName=\'Del_Parabrisas\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
######################################################
@app.get("/admrepdelsuv", response_class=HTMLResponse)
async def admrepdel(request: Request):
    context = {"request": request,
               "Paragolpe_Ctro":"Paragolpe Centro"      ,"Paragolpe_Ctro_Val":0.0,
               "Paragolpe_Rejilla":"Paragolpe Rejilla"  ,"Paragolpe_Rejilla_Val":0.0,
               "Paragolpe_Alma":"Paragolpe Alma"        ,"Paragolpe_Alma_Val":0.0,
               "Rejilla_Radiador":"Rejilla Radiador"    ,"Rejilla_Radiador_Val":0.0,
               "Frente":"Frente"                        ,"Frente_Val":0.0,
               "Guardabarro":"Guardabarro"              ,"Guardabarro_Val":0.0,
               "Faro":"Faro"                            ,"Faro_Val":0.0,
               "Faro_Auxiliar":"Faro Auxiliar"          ,"Faro_Auxiliar_Val":0.0,
               "Farito":"Farito"                        ,"Farito_Val":0.0,
               "Capot":"Capot"                          ,"Capot_Val":0.0,
               "Parabrisas":"Parabrisas"                ,"Parabrisas_Val":0.0,
               "MensajeRetorno":""
               }
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT * FROM admvaluesdelsuv;'))
        for row in result:
            if row[0] == 'Del_Paragolpe_Ctro'    : context["Paragolpe_Ctro_Val"]    = float(row[1])
            if row[0] == 'Del_Paragolpe_Rejilla' : context["Paragolpe_Rejilla_Val"] = float(row[1])
            if row[0] == 'Del_Paragolpe_Alma'    : context["Paragolpe_Alma_Val"]    = float(row[1])
            if row[0] == 'Del_Rejilla_Radiador'  : context["Rejilla_Radiador_Val"]  = float(row[1])
            if row[0] == 'Del_Frente'            : context["Frente_Val"]            = float(row[1])
            if row[0] == 'Del_Guardabarro'       : context["Guardabarro_Val"]       = float(row[1])
            if row[0] == 'Del_Faro'              : context["Faro_Val"]              = float(row[1])
            if row[0] == 'Del_Faro_Auxiliar'     : context["Faro_Auxiliar_Val"]     = float(row[1])
            if row[0] == 'Del_Farito'            : context["Farito_Val"]            = float(row[1])
            if row[0] == 'Del_Capot'             : context["Capot_Val"]             = float(row[1])
            if row[0] == 'Del_Parabrisas'        : context["Parabrisas_Val"]        = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))
    return templates.TemplateResponse("admrepdelsuv.html", context)
#===========================================================
@app.post("/admvaluesdelsuv", response_class=PlainTextResponse)
async def admvaluesdelsuv(Paragolpe_Ctro:str="",Paragolpe_Rejilla:str="",Paragolpe_Alma:str="",Rejilla_Radiador:str="",Frente:str="",\
                          Guardabarro:str="",Faro:str="",Faro_Auxiliar:str="",Farito:str="",Capot:str="",Parabrisas:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue);
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvaluesdelsuv SET flValue =' + str(Paragolpe_Ctro).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Ctro\''))
       result = conn.execute(text('UPDATE admvaluesdelsuv SET flValue =' + str(Paragolpe_Rejilla).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Rejilla\''))
       result = conn.execute(text('UPDATE admvaluesdelsuv SET flValue =' + str(Paragolpe_Alma).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Alma\''))
       result = conn.execute(text('UPDATE admvaluesdelsuv SET flValue =' + str(Rejilla_Radiador).replace(',','.') + ' WHERE stName=\'Del_Rejilla_Radiador\''))
       result = conn.execute(text('UPDATE admvaluesdelsuv SET flValue =' + str(Frente).replace(',','.') + ' WHERE stName=\'Del_Frente\''))
       result = conn.execute(text('UPDATE admvaluesdelsuv SET flValue =' + str(Guardabarro).replace(',','.') + ' WHERE stName=\'Del_Guardabarro\''))
       result = conn.execute(text('UPDATE admvaluesdelsuv SET flValue =' + str(Faro).replace(',','.') + ' WHERE stName=\'Del_Faro\''))
       result = conn.execute(text('UPDATE admvaluesdelsuv SET flValue =' + str(Faro_Auxiliar).replace(',','.') + ' WHERE stName=\'Del_Faro_Auxiliar\''))
       result = conn.execute(text('UPDATE admvaluesdelsuv SET flValue =' + str(Farito).replace(',','.') + ' WHERE stName=\'Del_Farito\''))
       result = conn.execute(text('UPDATE admvaluesdelsuv SET flValue =' + str(Capot).replace(',','.') + ' WHERE stName=\'Del_Capot\''))
       result = conn.execute(text('UPDATE admvaluesdelsuv SET flValue =' + str(Parabrisas).replace(',','.') + ' WHERE stName=\'Del_Parabrisas\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
#####################################################
@app.get("/admrepdelag", response_class=HTMLResponse)
async def admrepdelag(request: Request):
    context = {"request": request,
               "Paragolpe_Ctro":"Paragolpe Centro"      ,"Paragolpe_Ctro_Val":0.0,
               "Paragolpe_Rejilla":"Paragolpe Rejilla"  ,"Paragolpe_Rejilla_Val":0.0,
               "Paragolpe_Alma":"Paragolpe Alma"        ,"Paragolpe_Alma_Val":0.0,
               "Rejilla_Radiador":"Rejilla Radiador"    ,"Rejilla_Radiador_Val":0.0,
               "Frente":"Frente"                        ,"Frente_Val":0.0,
               "Guardabarro":"Guardabarro"              ,"Guardabarro_Val":0.0,
               "Faro":"Faro"                            ,"Faro_Val":0.0,
               "Faro_Auxiliar":"Faro Auxiliar"          ,"Faro_Auxiliar_Val":0.0,
               "Farito":"Farito"                        ,"Farito_Val":0.0,
               "Capot":"Capot"                          ,"Capot_Val":0.0,
               "Parabrisas":"Parabrisas"                ,"Parabrisas_Val":0.0,
               "MensajeRetorno":""
               }
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT * FROM admvaluesdelal;'))
        for row in result:
            if row[0] == 'Del_Paragolpe_Ctro'    : context["Paragolpe_Ctro_Val"]    = float(row[1])
            if row[0] == 'Del_Paragolpe_Rejilla' : context["Paragolpe_Rejilla_Val"] = float(row[1])
            if row[0] == 'Del_Paragolpe_Alma'    : context["Paragolpe_Alma_Val"]    = float(row[1])
            if row[0] == 'Del_Rejilla_Radiador'  : context["Rejilla_Radiador_Val"]  = float(row[1])
            if row[0] == 'Del_Frente'            : context["Frente_Val"]            = float(row[1])
            if row[0] == 'Del_Guardabarro'       : context["Guardabarro_Val"]       = float(row[1])
            if row[0] == 'Del_Faro'              : context["Faro_Val"]              = float(row[1])
            if row[0] == 'Del_Faro_Auxiliar'     : context["Faro_Auxiliar_Val"]     = float(row[1])
            if row[0] == 'Del_Farito'            : context["Farito_Val"]            = float(row[1])
            if row[0] == 'Del_Capot'             : context["Capot_Val"]             = float(row[1])
            if row[0] == 'Del_Parabrisas'        : context["Parabrisas_Val"]        = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))
    return templates.TemplateResponse("admrepdelag.html", context)
#===========================================================
@app.post("/admvaluesdelag", response_class=PlainTextResponse)
async def admvaluesdelag(Paragolpe_Ctro:str="",Paragolpe_Rejilla:str="",Paragolpe_Alma:str="",Rejilla_Radiador:str="",Frente:str="",\
                          Guardabarro:str="",Faro:str="",Faro_Auxiliar:str="",Farito:str="",Capot:str="",Parabrisas:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue);
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvaluesdelal SET flValue =' + str(Paragolpe_Ctro).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Ctro\''))
       result = conn.execute(text('UPDATE admvaluesdelal SET flValue =' + str(Paragolpe_Rejilla).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Rejilla\''))
       result = conn.execute(text('UPDATE admvaluesdelal SET flValue =' + str(Paragolpe_Alma).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Alma\''))
       result = conn.execute(text('UPDATE admvaluesdelal SET flValue =' + str(Rejilla_Radiador).replace(',','.') + ' WHERE stName=\'Del_Rejilla_Radiador\''))
       result = conn.execute(text('UPDATE admvaluesdelal SET flValue =' + str(Frente).replace(',','.') + ' WHERE stName=\'Del_Frente\''))
       result = conn.execute(text('UPDATE admvaluesdelal SET flValue =' + str(Guardabarro).replace(',','.') + ' WHERE stName=\'Del_Guardabarro\''))
       result = conn.execute(text('UPDATE admvaluesdelal SET flValue =' + str(Faro).replace(',','.') + ' WHERE stName=\'Del_Faro\''))
       result = conn.execute(text('UPDATE admvaluesdelal SET flValue =' + str(Faro_Auxiliar).replace(',','.') + ' WHERE stName=\'Del_Faro_Auxiliar\''))
       result = conn.execute(text('UPDATE admvaluesdelal SET flValue =' + str(Farito).replace(',','.') + ' WHERE stName=\'Del_Farito\''))
       result = conn.execute(text('UPDATE admvaluesdelal SET flValue =' + str(Capot).replace(',','.') + ' WHERE stName=\'Del_Capot\''))
       result = conn.execute(text('UPDATE admvaluesdelal SET flValue =' + str(Parabrisas).replace(',','.') + ' WHERE stName=\'Del_Parabrisas\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
#########################################################
@app.get("/admrepdelagsuv", response_class=HTMLResponse)
async def admrepdelagsuv(request: Request):
    context = {"request": request,
               "Paragolpe_Ctro":"Paragolpe Centro"      ,"Paragolpe_Ctro_Val":0.0,
               "Paragolpe_Rejilla":"Paragolpe Rejilla"  ,"Paragolpe_Rejilla_Val":0.0,
               "Paragolpe_Alma":"Paragolpe Alma"        ,"Paragolpe_Alma_Val":0.0,
               "Rejilla_Radiador":"Rejilla Radiador"    ,"Rejilla_Radiador_Val":0.0,
               "Frente":"Frente"                        ,"Frente_Val":0.0,
               "Guardabarro":"Guardabarro"              ,"Guardabarro_Val":0.0,
               "Faro":"Faro"                            ,"Faro_Val":0.0,
               "Faro_Auxiliar":"Faro Auxiliar"          ,"Faro_Auxiliar_Val":0.0,
               "Farito":"Farito"                        ,"Farito_Val":0.0,
               "Capot":"Capot"                          ,"Capot_Val":0.0,
               "Parabrisas":"Parabrisas"                ,"Parabrisas_Val":0.0,
               "MensajeRetorno":""
               }
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text('SELECT * FROM admvaluesdelalsuv;'))
        for row in result:
            if row[0] == 'Del_Paragolpe_Ctro'    : context["Paragolpe_Ctro_Val"]    = float(row[1])
            if row[0] == 'Del_Paragolpe_Rejilla' : context["Paragolpe_Rejilla_Val"] = float(row[1])
            if row[0] == 'Del_Paragolpe_Alma'    : context["Paragolpe_Alma_Val"]    = float(row[1])
            if row[0] == 'Del_Rejilla_Radiador'  : context["Rejilla_Radiador_Val"]  = float(row[1])
            if row[0] == 'Del_Frente'            : context["Frente_Val"]            = float(row[1])
            if row[0] == 'Del_Guardabarro'       : context["Guardabarro_Val"]       = float(row[1])
            if row[0] == 'Del_Faro'              : context["Faro_Val"]              = float(row[1])
            if row[0] == 'Del_Faro_Auxiliar'     : context["Faro_Auxiliar_Val"]     = float(row[1])
            if row[0] == 'Del_Farito'            : context["Farito_Val"]            = float(row[1])
            if row[0] == 'Del_Capot'             : context["Capot_Val"]             = float(row[1])
            if row[0] == 'Del_Parabrisas'        : context["Parabrisas_Val"]        = float(row[1])
        conn.close()
        engine.dispose()
    except Exception as e:
        context["MensajeRetorno"] = "Se produjo un error al recuperar los valores, comuniquese con el administrador"
        logger.error(f"Error: "+str(e))
    return templates.TemplateResponse("admrepdelagsuv.html", context)
#===============================================================
@app.post("/admvaluesdelagsuv", response_class=PlainTextResponse)
async def admvaluesdelagsuv(Paragolpe_Ctro:str="",Paragolpe_Rejilla:str="",Paragolpe_Alma:str="",Rejilla_Radiador:str="",Frente:str="",\
                            Guardabarro:str="",Faro:str="",Faro_Auxiliar:str="",Farito:str="",Capot:str="",Parabrisas:str=""):
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       engine = db.create_engine(cDBConnValue);
       conn = engine.connect()
       result = conn.execute(text('UPDATE admvaluesdelalsuv SET flValue =' + str(Paragolpe_Ctro).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Ctro\''))
       result = conn.execute(text('UPDATE admvaluesdelalsuv SET flValue =' + str(Paragolpe_Rejilla).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Rejilla\''))
       result = conn.execute(text('UPDATE admvaluesdelalsuv SET flValue =' + str(Paragolpe_Alma).replace(',','.') + ' WHERE stName=\'Del_Paragolpe_Alma\''))
       result = conn.execute(text('UPDATE admvaluesdelalsuv SET flValue =' + str(Rejilla_Radiador).replace(',','.') + ' WHERE stName=\'Del_Rejilla_Radiador\''))
       result = conn.execute(text('UPDATE admvaluesdelalsuv SET flValue =' + str(Frente).replace(',','.') + ' WHERE stName=\'Del_Frente\''))
       result = conn.execute(text('UPDATE admvaluesdelalsuv SET flValue =' + str(Guardabarro).replace(',','.') + ' WHERE stName=\'Del_Guardabarro\''))
       result = conn.execute(text('UPDATE admvaluesdelalsuv SET flValue =' + str(Faro).replace(',','.') + ' WHERE stName=\'Del_Faro\''))
       result = conn.execute(text('UPDATE admvaluesdelalsuv SET flValue =' + str(Faro_Auxiliar).replace(',','.') + ' WHERE stName=\'Del_Faro_Auxiliar\''))
       result = conn.execute(text('UPDATE admvaluesdelalsuv SET flValue =' + str(Farito).replace(',','.') + ' WHERE stName=\'Del_Farito\''))
       result = conn.execute(text('UPDATE admvaluesdelalsuv SET flValue =' + str(Capot).replace(',','.') + ' WHERE stName=\'Del_Capot\''))
       result = conn.execute(text('UPDATE admvaluesdelalsuv SET flValue =' + str(Parabrisas).replace(',','.') + ' WHERE stName=\'Del_Parabrisas\''))
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)
       logger.error(f"Error: "+str(e))
    return bfMsg
#########################################################
@app.get("/admrdel", response_class=HTMLResponse)
async def admrepdelagsuv(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("admrdel.html", context)
#########################################################
@app.get("/dbread", response_class=HTMLResponse)
async def dbRead(request: Request):
    lsResult        = []
    lsTimeStamp     = []
    lsReparaTrasero = []
    lsCambiaTrasero = []
    lsReparaLateral = []
    lsCambiaLateral = []
    lsReparaFrente  = []
    lsCambiaFrente  = []
    context = {"request": request,"result":'',"timestamp":'',
               "reparatrasero":'',"cambiatrasero":'',
               "reparalateral":'',"cambialateral":''}
    
    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    try:
        result = conn.execute(text('''SELECT * FROM logpresupuestosV1;'''))
        for record in result:
            lsResult.append(record)
            lsTimeStamp.append(datetime.datetime.fromtimestamp(float(record.timestamp)).strftime('%Y-%m-%d %H:%M:%S'))
            lsReparaTrasero.append(fnRepTrasero(record.trasero))
            lsCambiaTrasero.append(fnCmbTrasero(record.trasero))
            lsReparaLateral.append(fnRepLateral(record.lateralr))
            lsCambiaLateral.append(fnCmbLateral(record.lateralr))
            #lsReparaFrente.append(fnRepLateral(record.frente))
            #lsCambiaFrente.append(fnCmbLateral(record.frente))

    except exc.SQLAlchemyError as e:
        bfValue = 'dbInsertAdminValue Error: '+str(e)
        logger.error(f"Error: "+str(e))
    conn.close()
    engine.dispose()
    context["result"] = lsResult
    context["restimestamp"]  = lsTimeStamp
    context["reparatrasero"] = lsReparaTrasero
    context["cambiatrasero"] = lsCambiaTrasero
    context["reparalateral"] = lsReparaLateral
    context["cambialateral"] = lsCambiaLateral
    #context["reparafrente"]  = lsReparaFrente
    #context["cambiafrente"]  = lsCambiaFrente

    return templates.TemplateResponse("readlog.html", context)

def fnRepTrasero(input):
    valores = input.split('-')
    cBaul_Porton_DerRep = 2
    cGuardabarro_DerRep = 8
    cGuardabarro_IzaRep = 10
    cPanel_Cola_DerRep  = 14
    cParagolpe_DerRep   = 16
    bfDisplay = ''

    for indice, valor in enumerate(valores):
        if valor == '1':
            if indice+1 == cBaul_Porton_DerRep:
                bfDisplay += 'B'
            elif indice+1 == cGuardabarro_DerRep:
                bfDisplay += 'Gd'
            elif indice+1 == cGuardabarro_IzaRep:
                bfDisplay += 'Gi'
            elif indice+1 == cPanel_Cola_DerRep:
                bfDisplay += 'C'
            elif indice+1 == cParagolpe_DerRep:
                bfDisplay += 'P'
    return bfDisplay

def fnCmbTrasero(input):
    valores = input.split('-')
    cBaul_Portón_DerCam =1
    cGuardabarro_DerCam =7
    cGuardabarro_IzaCam =9
    cPanel_Cola_DerCam  =13
    cParagolpe_DerCam   =15
    bfDisplay = ''

    for indice, valor in enumerate(valores):
        if valor == '1':
            if indice+1 == cBaul_Portón_DerCam:
                bfDisplay += 'B'
            elif indice+1 == cGuardabarro_DerCam:
                bfDisplay += 'Gd'
            elif indice+1 == cGuardabarro_IzaCam:
                bfDisplay += 'Gi'
            elif indice+1 == cPanel_Cola_DerCam:
                bfDisplay += 'C'
            elif indice+1 == cParagolpe_DerCam:
                bfDisplay += 'P'
    return bfDisplay

def fnRepLateral(input):
    valores = input.split('-')
    cPosPUERTA_DEL_PANELReparaDer=20
    cPosPUERTA_DEL_PANELReparaIzq=21
    cPosPUERTA_TRA_PANELReparaDer=22
    cPosPUERTA_TRA_PANELReparaIzq=23
    cPosZOCALOReparaDer=25
    cPosZOCALOReparaIzq=27
    bfDisplay = ''

    for indice, valor in enumerate(valores):
        if valor == '1':
            if indice == cPosPUERTA_DEL_PANELReparaDer:
                bfDisplay += 'Pdd'
            elif indice == cPosPUERTA_DEL_PANELReparaIzq:
                bfDisplay += 'Pdi'
            elif indice == cPosPUERTA_TRA_PANELReparaDer:
                bfDisplay += 'Ptd'
            elif indice == cPosPUERTA_TRA_PANELReparaIzq:
                bfDisplay += 'Pti'
            elif indice == cPosZOCALOReparaDer:
                bfDisplay += 'Zd'
            elif indice == cPosZOCALOReparaIzq:
                bfDisplay += 'Zi'
    return bfDisplay

def fnCmbLateral(input):
    valores = input.split('-')
    cPosPUERTA_DELCambiaDer=16
    cPosPUERTA_DELCambiaIzq=17
    cPosPUERTA_TRACambiaDer=18
    cPosPUERTA_TRACambiaIzq=19
    cPosZOCALOCambiaDer=24
    cPosZOCALOCambiaIzq=26
    bfDisplay = ''

    for indice, valor in enumerate(valores):
        if valor == '1':
            if indice == cPosPUERTA_DELCambiaDer:
                bfDisplay += 'Pdd'
            elif indice == cPosPUERTA_DELCambiaIzq:
                bfDisplay += 'Pdi'
            elif indice == cPosPUERTA_TRACambiaDer:
                bfDisplay += 'Ptd'
            elif indice == cPosPUERTA_TRACambiaIzq:
                bfDisplay += 'Pti'
            elif indice == cPosZOCALOCambiaDer:
                bfDisplay += 'Zd'
            elif indice == cPosZOCALOCambiaIzq:
                bfDisplay += 'Zi'
    return bfDisplay

@app.post("/search", response_class=PlainTextResponse)
    #Segmenta Input
async def search_Data(CLIENTE:str="",CLASE:str="",MARCA:str="",MODELO:str="",SINIESTRO:str="",\
                      PERITO:str="",VALORPERITO:str="",FRENTE:str="",LATERAL:str="",TRASERO:str=""):
    lsFrente  = FRENTE.split('-')
    lsLateral = LATERAL.split('-')
    lsTrasero = TRASERO.split('-')
    ###FRENTE###
    lsFrenteCambiaElems               = []
    lsFrenteReparaElems               = []
    lsFrenteFaritoElemsDel            = []
    lsFrenteFaroElemsDel              = []
    lsFrenteFaro_AuxiliarElemsDel     = []
    lsFrenteParabrisasElemsDel        = []
    lsFrenteParagolpe_RejillaElemsDel = []
    lsFrenteRejilla_RadiadorElemsDel  = []
    flFrtValorReparaAve=0
    flFrtValorReponeElem=0
    flFrtValorReponePint=0
    flFrtValorReponeMoAv=0
    flFrtValorReponeFarito=0
    flFrtValorReponeFaro=0
    flFrtValorReponeFaro_Auxiliar=0
    flFrtValorReponeParabrisas=0
    flFrtValorReponeParagolpe_Rejilla=0
    flFrtValorReponeRejilla_Radiador=0
    ###LATERAL###
    lsLateralCambiaElems = []
    lsLateralReparaElems = []
    lsLateralMolduraElemsDel= []
    lsLateralMolduraElemsTra= []
    lsLateralEspejoElecElems= []
    lsLateralEspejoManElems= []
    lsLateralManijaElemsDel= []
    lsLateralManijaElemsTra= []
    lsLateralCristalElemDel= []
    lsLateralCristalElemTra= []
    flLatValorReparaAve=0
    flLatValorReponeElem=0
    flLatValorReponePint=0
    flLatValorReponeMoAv=0
    flLatValorReponeEspejoElec=0
    flLatValorReponeEspejoMan=0
    flLatValorReponeMolduraDel=0
    flLatValorReponeMolduraTra=0
    flLatValorReponeManDel=0
    flLatValorReponeManTra=0
    flLatValorReponeCriDel=0
    flLatValorReponeCriTra=0
    ###TRASERO###
    lsTraseroCambiaElems = []
    lsTraseroReparaElems = []
    lsTraseroMolduraElems= []
    lsTraseroFaroExtElems= []
    lsTraseroFaroIntElems= []
    ###RESULT###
    lsValuesResult = []

    flTraValorReparaAve=0
    flTraValorReponeElem=0
    flTraValorReponePint=0
    flTraValorReponeMoAv=0
    flTraValorReponeMoldura=0
    flTraValorReponeFaroExt=0
    flTraValorReponeFaroInt=0

    if CLASE == "908":
        isWrited = fnWriteLogBrief(CLIENTE,CLASE,MARCA,MODELO,SINIESTRO,PERITO,VALORPERITO)
        bfTmp = "Sugerido&nbsp$&nbsp" + VALORPERITO
        return bfTmp

    #ToDo: Agregar si no es numerico mensaje de error
    if CLASE.isdigit(): iCLASE = int(CLASE)
    if MARCA.isdigit(): iMARCA = int(MARCA)
    if MODELO.isdigit():iMODELO= int(MODELO)
    #Deteccion de Segmento y Gama
    iSEG = fnSegmento(iCLASE,iMARCA,iMODELO)
    isAlta = fnAltaGama(CLASE,MARCA,MODELO)
    #Output
    flFrente=0
    flLateral=0
    flTrasero=0

    
    logger.info(f"Nada: {lsValuesResult}")
    
    if '1' in lsFrente:
        lsFrenteCambiaElems, lsFrenteReparaElems, lsFrenteFaritoElemsDel, lsFrenteFaroElemsDel, lsFrenteFaro_AuxiliarElemsDel,\
        lsFrenteParabrisasElemsDel, lsFrenteParagolpe_RejillaElemsDel, lsFrenteRejilla_RadiadorElemsDel = fnGetFrentelElems(lsFrente)

        if len(lsFrenteReparaElems)>0:
            lsLatReparaAve=fnReparaFrente(iSEG,iCLASE,lsFrenteReparaElems)
            if len(lsLatReparaAve) == 0: lsLatReparaAve.append(0)
            flFrtValorReparaAve = np.round(sum(lsLatReparaAve),2)

        if len(lsFrenteCambiaElems)>0:
            lsLatReponeAve=fnCambiaFrente(iSEG,iCLASE,iMARCA,iMODELO,lsFrenteCambiaElems,isAlta)
            if len(lsLatReponeAve) == 0: lsLatReponeAve.append(0)
            flFrtValorReponeElem = np.round(sum(lsLatReponeAve),2)

            lsLatReponePintAve, lsLatReponeMoAv = fnCambiaPinturaFrente(iSEG,iCLASE,lsFrenteCambiaElems)
            if len(lsLatReponePintAve) == 0: lsLatReponePintAve.append(0)
            flFrtValorReponePint = np.round(sum(lsLatReponePintAve),2)

            if len(lsLatReponeMoAv)  == 0: lsLatReponeMoAv.append(0)
            flFrtValorReponeMoAv = np.round(sum(lsLatReponeMoAv),2)

        if len(lsFrenteFaritoElemsDel)>0:
            lsFrenteMean = fnFaritoFrente(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsFrenteMean) == 0: lsFrenteMean.append(0)
            flFrtValorReponeFarito = np.round(lsFrenteMean[0],2)

        if len(lsFrenteFaroElemsDel)>0:
            lsFrenteMean = fnFaroFrente(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsFrenteMean) == 0: lsFrenteMean.append(0)
            flFrtValorReponeFaro = np.round(lsFrenteMean[0],2)

        if len(lsFrenteFaro_AuxiliarElemsDel)>0:
            if isAlta: flFrtValorReponeFaro_Auxiliar = paramal.bfFrt_GA_Del_Faro_Auxiliar
            else:      flFrtValorReponeFaro_Auxiliar = param.bfFrt_GM_Del_Faro_Auxiliar

        if len(lsFrenteParabrisasElemsDel)>0:
            lsFrenteMean = fnParabrisas(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsFrenteMean) == 0: lsFrenteMean.append(0)
            flFrtValorReponeParabrisas = np.round(lsFrenteMean[0],2)

        if len(lsFrenteParagolpe_RejillaElemsDel)>0:
            lsFrenteMean = fnParagolpe_Rejilla(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsFrenteMean) == 0: lsFrenteMean.append(0)
            flFrtValorReponeParagolpe_Rejilla = np.round(lsFrenteMean[0],2)

        if len(lsFrenteRejilla_RadiadorElemsDel)>0:
            lsFrenteMean = fnRejilla_Radiador(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsFrenteMean) == 0: lsFrenteMean.append(0)
            flFrtValorReponeRejilla_Radiador = np.round(lsFrenteMean[0],2)

        flFrente=np.round(flFrtValorReparaAve + flFrtValorReponeElem + flFrtValorReponePint + flFrtValorReponeMoAv+\
                          flFrtValorReponeFarito + flFrtValorReponeFaro + flFrtValorReponeFaro_Auxiliar + flFrtValorReponeParabrisas+\
                          flFrtValorReponeParagolpe_Rejilla + flFrtValorReponeRejilla_Radiador,2)

        lsValuesResult.append(flFrtValorReparaAve)
        lsValuesResult.append(flFrtValorReponeElem)
        lsValuesResult.append(flFrtValorReponePint)
        lsValuesResult.append(flFrtValorReponeMoAv)
        lsValuesResult.append(flFrtValorReponeFarito)
        lsValuesResult.append(flFrtValorReponeFaro)
        lsValuesResult.append(flFrtValorReponeFaro_Auxiliar)
        lsValuesResult.append(flFrtValorReponeParabrisas)
        lsValuesResult.append(flFrtValorReponeParagolpe_Rejilla)
        lsValuesResult.append(flFrtValorReponeRejilla_Radiador)
        lsValuesResult.append(flFrente)
    else:
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)

    logger.info(f"Frente: {lsValuesResult}")
    
    if '1' in lsLateral:
        lsLateralCambiaElems,lsLateralReparaElems, lsLateralMolduraElemsDel,lsLateralMolduraElemsTra, lsLateralEspejoElecElems,lsLateralEspejoManElems,\
        lsLateralManijaElemsDel,lsLateralManijaElemsTra, lsLateralCristalElemDel, lsLateralCristalElemTra = fnGetLateralElems(lsLateral)

        if len(lsLateralReparaElems)>0:
            lsLatReparaAve=fnReparaLateral(iSEG,iCLASE,lsLateralReparaElems)
            if len(lsLatReparaAve) == 0: lsLatReparaAve.append(0)
            flLatValorReparaAve = np.round(sum(lsLatReparaAve),2)

        if len(lsLateralCambiaElems)>0:
            lsLatReponeAve=fnCambiaLateral(iSEG,iCLASE,iMARCA,iMODELO,lsLateralCambiaElems,isAlta)
            if len(lsLatReponeAve) == 0: lsLatReponeAve.append(0)
            flLatValorReponeElem = np.round(sum(lsLatReponeAve),2)

            lsLatReponePintAve,lsLatReponeMoAv = fnCambiaPinturaLateral(iSEG,iCLASE,lsLateralCambiaElems)
            if len(lsLatReponePintAve) == 0: lsLatReponePintAve.append(0)
            flLatValorReponePint = np.round(sum(lsLatReponePintAve),2)
            if len(lsLatReponeMoAv)  == 0: lsLatReponeMoAv.append(0)
            flLatValorReponeMoAv = np.round(sum(lsLatReponeMoAv),2)

        if len(lsLateralMolduraElemsDel)>0:
            lsLatMeanMod = fnMolduraLateralDel(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsLatMeanMod) == 0: lsLatMeanMod.append(0)
            flLatValorReponeMolduraDel = np.round(lsLatMeanMod[0],2)
            if len(lsLateralMolduraElemsDel)== 2: flLatValorReponeMolduraDel*=2

        if len(lsLateralMolduraElemsTra)>0:
            lsLatMeanMod = fnMolduraLateralTra(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsLatMeanMod) == 0: lsLatMeanMod.append(0)
            flLatValorReponeMolduraTra = np.round(lsLatMeanMod[0],2)
            if len(lsLateralMolduraElemsTra)== 2: flLatValorReponeMolduraTra*=2

        if len(lsLateralEspejoElecElems)>0:
            lsLatMeanEsp = fnEspejoLateralElec(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsLatMeanEsp) == 0: lsLatMeanEsp.append(0)
            flLatValorReponeEspejoElec = np.round(lsLatMeanEsp[0],2)
            if len(lsLateralEspejoElecElems) >1: flLatValorReponeEspejoElec*=2

        if len(lsLateralEspejoManElems)>0:
            lsLatMeanEsp = fnEspejoLateralMan(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsLatMeanEsp) == 0: lsLatMeanEsp.append(0)
            flLatValorReponeEspejoMan = np.round(lsLatMeanEsp[0],2)
            if len(lsLateralEspejoManElems) >1: flLatValorReponeEspejoMan*=2

        if len(lsLateralManijaElemsDel)>0:
            lsLatMeanManDel = fnManijaLateralDel(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsLatMeanManDel) == 0: lsLatMeanManDel.append(0)
            flLatValorReponeManDel = np.round(lsLatMeanManDel[0],2)
            if len(lsLateralManijaElemsDel) >1: flLatValorReponeManDel*=2

        if len(lsLateralManijaElemsTra)>0:
            lsLatMeanManTra = fnManijaLateralTra(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsLatMeanManTra) == 0: lsLatMeanManTra.append(0)
            flLatValorReponeManTra = np.round(lsLatMeanManTra[0],2)
            if len(lsLateralManijaElemsTra) >1: flLatValorReponeManTra*=2

        if len(lsLateralCristalElemDel)>0:
            lsLatMeanCriDel = fnCristalLateralDel(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsLatMeanCriDel) == 0: lsLatMeanCriDel.append(0)
            flLatValorReponeCriDel = np.round(lsLatMeanCriDel[0],2)
            if len(lsLateralCristalElemDel) >1: flLatValorReponeCriDel*=2

        if len(lsLateralCristalElemTra)>0:
            lsLatMeanCriTra = fnCristalLateralTra(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsLatMeanCriTra) == 0: lsLatMeanCriTra.append(0)
            flLatValorReponeCriTra = np.round(lsLatMeanCriTra[0],2)
            if len(lsLateralCristalElemTra) >1: flLatValorReponeCriTra*=2

        flLateral=np.round(flLatValorReparaAve+flLatValorReponeElem+flLatValorReponePint+flLatValorReponeMoAv+\
                           flLatValorReponeEspejoElec+flLatValorReponeEspejoMan+flLatValorReponeManDel+\
                           flLatValorReponeManTra+flLatValorReponeMolduraDel+flLatValorReponeMolduraTra+\
                           flLatValorReponeCriDel+flLatValorReponeCriTra,2)

        lsValuesResult.append(flLatValorReparaAve)
        lsValuesResult.append(flLatValorReponeElem)
        lsValuesResult.append(flLatValorReponePint)
        lsValuesResult.append(flLatValorReponeMoAv)
        lsValuesResult.append(flLatValorReponeEspejoElec)
        lsValuesResult.append(flLatValorReponeEspejoMan)
        lsValuesResult.append(flLatValorReponeManDel)
        lsValuesResult.append(flLatValorReponeManTra)
        lsValuesResult.append(flLatValorReponeMolduraDel)
        lsValuesResult.append(flLatValorReponeMolduraTra)
        lsValuesResult.append(flLatValorReponeCriDel)
        lsValuesResult.append(flLatValorReponeCriTra)
        lsValuesResult.append(flLateral)
    else:
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)

    logger.info(f"lateral: {lsValuesResult}")

    if '1' in lsTrasero:
        lsTraseroCambiaElems,lsTraseroReparaElems,lsTraseroMolduraElems,\
        lsTraseroFaroExtElems,lsTraseroFaroIntElems= fnGetTraseroElems(CLASE,MARCA,MODELO,lsTrasero)

        if len(lsTraseroReparaElems)>0:
            lsTraReparaAve=fnReparaTrasero(iSEG,iCLASE,lsTraseroReparaElems)
            if len(lsTraReparaAve) == 0: lsTraReparaAve.append(0)
            flTraValorReparaAve = np.round(sum(lsTraReparaAve),2)

        if len(lsTraseroCambiaElems)>0:
            lsTraReponeAve=fnCambiaTrasero(iSEG,iCLASE,iMARCA,iMODELO,lsTraseroCambiaElems,isAlta)
            if len(lsTraReponeAve)  == 0: lsTraReponeAve.append(0)
            flTraValorReponeElem = np.round(sum(lsTraReponeAve),2)

            lsTraReponePintAve,lsTraReponeMoAv = fnCambiaPinturaTrasero(iSEG,iCLASE,lsTraseroCambiaElems)
            if len(lsTraReponePintAve) == 0: lsTraReponePintAve.append(0)
            flTraValorReponePint = np.round(sum(lsTraReponePintAve),2)
            if len(lsTraReponeMoAv)  == 0: lsTraReponeMoAv.append(0)
            flTraValorReponeMoAv = np.round(sum(lsTraReponeMoAv),2)

        if len(lsTraseroCambiaElems) + len(lsTraseroReparaElems) == 1:
            if flTraValorReparaAve != 0:
                flTraValorReparaAve = flTraValorReparaAve + param.bfMObra
            if flTraValorReponeElem != 0:
                flTraValorReponeElem = flTraValorReponeElem + param.bfMObra

        if len(lsTraseroMolduraElems)>0:
            lsTraMeanMold=fnMolduraTrasero(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsTraMeanMold) == 0: lsTraMeanMold.append(0)
            flTraValorReponeMoldura  = np.round(lsTraMeanMold[-1],2)

        if len(lsTraseroFaroExtElems)>0:
            lsTraMeanFExt=fnFaroExtTrasero(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsTraMeanFExt) == 0: lsTraMeanFExt.append(0)
            flTraValorReponeFaroExt  = np.round(lsTraMeanFExt[-1],2)
            if len(lsTraseroFaroExtElems) >1: flTraValorReponeFaroExt*=2

        if len(lsTraseroFaroIntElems)>0:
            lsTraMeanFInt=fnFaroIntTrasero(iCLASE,iMARCA,iMODELO,isAlta)
            if len(lsTraMeanFInt) == 0: lsTraMeanFInt.append(0)
            flTraValorReponeFaroInt  = np.round(lsTraMeanFInt[-1],2)
            if len(lsTraseroFaroIntElems) >1: flTraValorReponeFaroInt*=2

        flTrasero=np.round(flTraValorReparaAve + flTraValorReponeElem + flTraValorReponePint + flTraValorReponeMoAv+\
                           flTraValorReponeMoldura + flTraValorReponeFaroExt + flTraValorReponeFaroInt,2)

        lsValuesResult.append(flTraValorReparaAve)
        lsValuesResult.append(flTraValorReponeElem)
        lsValuesResult.append(flTraValorReponePint)
        lsValuesResult.append(flTraValorReponeMoAv)
        lsValuesResult.append(flTraValorReponeMoldura)
        lsValuesResult.append(flTraValorReponeFaroExt)
        lsValuesResult.append(flTraValorReponeFaroInt)
        lsValuesResult.append(flTrasero)
    else:
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)
        lsValuesResult.append(0)

    logger.info(f"Trasero: {lsValuesResult}")
    
    #ToDo: Seguir codigo
    if len(lsFrenteCambiaElems) + len(lsFrenteReparaElems) +\
       len(lsLateralCambiaElems) + len(lsLateralReparaElems) +\
       len(lsTraseroCambiaElems) + len(lsTraseroReparaElems) == 1:
        # Agregar en lsValuesResult
        if flFrente  != 0: flFrente =  flFrente  + param.bfMObra
        if flLateral != 0: flLateral = flLateral + param.bfMObra
        if flTrasero != 0: flTrasero = flTrasero + param.bfMObra

    bfTmp = resumeDataBrief(CLIENTE,flFrente,flLateral,flTrasero)
    isWrited = fnWriteLog(CLIENTE,CLASE,MARCA,MODELO,SINIESTRO,PERITO,VALORPERITO,FRENTE,LATERAL,TRASERO,lsValuesResult)
    return bfTmp
###########################################################
def decimal(obj):
    is_point = False
    decimals = []
    for get_float in str(obj):
        if is_point:         decimals.append(get_float)
        if get_float == ".": is_point = True
    return len(decimals)

def fnSegmento(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO):
    lsSEG = dfSEGMENTO.loc[(dfSEGMENTO['COD_CLASE']  == inCOD_CLASE) & 
                           (dfSEGMENTO['COD_MARCA']  == inCOD_MARCA) &
                           (dfSEGMENTO['COD_MODELO'] == inCOD_MODELO)]['SEG'].to_numpy()
    if len(lsSEG)==0: return 0
    else: return lsSEG[0]

def fnGetFrentelElems(lsFrenteLc):
    lsFrenteElemsLc = ["CAPOT","FARITO","FARO","FARO_AUXILIAR","FRENTE","GUARDABARRO",
                       "PARABRISA","PARAGOLPE_ALMA","PARAGOLPE_CTRO","PARAGOLPE_REJILLA","REJILLA_RADIADOR"]

    lsFrenteCambiaVal         = []
    lsFrenteReparaVal         = []
    lsFrenteFarito            = []
    lsFrenteFaro              = []
    lsFrenteFaro_Auxiliar     = []
    lsFrenteParabrisas        = []
    lsFrenteParagolpe_Rejilla = []
    lsFrenteRejilla_Radiador  = []

    iPosCAPOT=0
    iPosFARITO=1
    iPosFARO=2
    iPosFARO_AUXILIAR=3
    iPosFRENTE=4
    iPosGUARDABARRO=5
    iPosPARABRISA=6
    iPosPARAGOLPE_ALMA=7
    iPosPARAGOLPE_CTRO=8
    iPosPARAGOLPE_REJILLA=9
    iPosREJILLA_RADIADOR=10

    iPosCAPOTCambiaDer=0
    iPosCAPOTReparaDer=1
    iPosFARITOCambiaDer=2
    iPosFARITOCambiaIzq=3
    iPosFAROCambiaDer=4
    iPosFAROCambiaIzq=5
    iPosFARO_AUXILIARCambiaDer=6
    iPosFARO_AUXILIARCambiaIzq=7
    iPosFRENTECambiaDer=8
    iPosFRENTEReparaDer=9
    iPosGUARDABARROCambiaDer=10
    iPosGUARDABARROReparaDer=11
    iPosGUARDABARROCambiaIzq=12
    iPosGUARDABARROReparaIzq=13
    iPosPARABRISACambiaDer=14
    iPosPARAGOLPE_ALMACambiaDer=15
    iPosPARAGOLPE_ALMAReparaDer=16
    iPosPARAGOLPE_CTROCambiaDer=17
    iPosPARAGOLPE_CTROReparaDer=18
    iPosPARAGOLPE_REJILLACambiaDer=19
    iPosREJILLA_RADIADIRCambiaDer=20

    lsFrenteCambiaVal.append(lsFrenteElemsLc[iPosCAPOT] if lsFrenteLc[iPosCAPOTCambiaDer]=="1" else "")
    lsFrenteReparaVal.append(lsFrenteElemsLc[iPosCAPOT] if lsFrenteLc[iPosCAPOTReparaDer]=="1" else "")
    lsFrenteCambiaVal.append(lsFrenteElemsLc[iPosFRENTE] if lsFrenteLc[iPosFRENTECambiaDer]=="1" else "")
    lsFrenteReparaVal.append(lsFrenteElemsLc[iPosFRENTE] if lsFrenteLc[iPosFRENTEReparaDer]=="1" else "")
    lsFrenteCambiaVal.append(lsFrenteElemsLc[iPosGUARDABARRO] if lsFrenteLc[iPosGUARDABARROCambiaDer]=="1" else "")
    lsFrenteCambiaVal.append(lsFrenteElemsLc[iPosGUARDABARRO] if lsFrenteLc[iPosGUARDABARROCambiaIzq]=="1" else "")
    lsFrenteReparaVal.append(lsFrenteElemsLc[iPosGUARDABARRO] if lsFrenteLc[iPosGUARDABARROReparaDer]=="1" else "")
    lsFrenteReparaVal.append(lsFrenteElemsLc[iPosGUARDABARRO] if lsFrenteLc[iPosGUARDABARROReparaIzq]=="1" else "")
    lsFrenteCambiaVal.append(lsFrenteElemsLc[iPosPARAGOLPE_ALMA] if lsFrenteLc[iPosPARAGOLPE_ALMACambiaDer]=="1" else "")
    lsFrenteReparaVal.append(lsFrenteElemsLc[iPosPARAGOLPE_ALMA] if lsFrenteLc[iPosPARAGOLPE_ALMAReparaDer]=="1" else "")
    lsFrenteCambiaVal.append(lsFrenteElemsLc[iPosPARAGOLPE_CTRO] if lsFrenteLc[iPosPARAGOLPE_CTROCambiaDer]=="1" else "")
    lsFrenteReparaVal.append(lsFrenteElemsLc[iPosPARAGOLPE_CTRO] if lsFrenteLc[iPosPARAGOLPE_CTROReparaDer]=="1" else "")
    lsFrenteFarito.append(lsFrenteElemsLc[iPosFARITO] if lsFrenteLc[iPosFARITOCambiaDer]=="1" else "")
    lsFrenteFarito.append(lsFrenteElemsLc[iPosFARITO] if lsFrenteLc[iPosFARITOCambiaIzq]=="1" else "")
    lsFrenteFaro.append(lsFrenteElemsLc[iPosFARO] if lsFrenteLc[iPosFAROCambiaDer]=="1" else "")
    lsFrenteFaro.append(lsFrenteElemsLc[iPosFARO] if lsFrenteLc[iPosFAROCambiaIzq]=="1" else "")
    lsFrenteFaro_Auxiliar.append(lsFrenteElemsLc[iPosFARO_AUXILIAR] if lsFrenteLc[iPosFARO_AUXILIARCambiaDer]=="1" else "")
    lsFrenteFaro_Auxiliar.append(lsFrenteElemsLc[iPosFARO_AUXILIAR] if lsFrenteLc[iPosFARO_AUXILIARCambiaIzq]=="1" else "")
    lsFrenteParabrisas.append(lsFrenteElemsLc[iPosPARABRISA] if lsFrenteLc[iPosPARABRISACambiaDer]=="1" else "")
    lsFrenteParagolpe_Rejilla.append(lsFrenteElemsLc[iPosPARAGOLPE_REJILLA] if lsFrenteLc[iPosPARAGOLPE_REJILLACambiaDer]=="1" else "")
    lsFrenteRejilla_Radiador.append(lsFrenteElemsLc[iPosREJILLA_RADIADOR] if lsFrenteLc[iPosREJILLA_RADIADIRCambiaDer]=="1" else "")

    lsFrenteCambiaVal         = [i for i in lsFrenteCambiaVal if i != ""]
    lsFrenteReparaVal         = [i for i in lsFrenteReparaVal if i != ""]
    lsFrenteFarito            = [i for i in lsFrenteFarito if i != ""]
    lsFrenteFaro              = [i for i in lsFrenteFaro if i != ""]
    lsFrenteFaro_Auxiliar     = [i for i in lsFrenteFaro_Auxiliar if i != ""]
    lsFrenteParabrisas        = [i for i in lsFrenteParabrisas if i != ""]
    lsFrenteParagolpe_Rejilla = [i for i in lsFrenteParagolpe_Rejilla if i != ""]
    lsFrenteRejilla_Radiador  = [i for i in lsFrenteRejilla_Radiador if i != ""]

    return lsFrenteCambiaVal,lsFrenteReparaVal,lsFrenteFarito,lsFrenteFaro,lsFrenteFaro_Auxiliar,\
           lsFrenteParabrisas,lsFrenteParagolpe_Rejilla,lsFrenteRejilla_Radiador


def fnGetLateralElems(lsLateralLc):
    lsLateralElemsLc = ["CRISTAL_DEL","CRISTAL_TRA","ESPEJOELEC","ESPEJOMAN","MANIJA_DEL","MANIJA_TRA",
                        "MOLDURA_DEL","MOLDURA_TRA","PUERTA_DEL","PUERTA_TRA","PUERTA_DEL_PANEL","PUERTA_TRA_PANEL",
                        "ZOCALO"]

    lsLateralCambiaVal     = []
    lsLateralReparaVal     = []
    lsLateralMolduraDelVal = []
    lsLateralMolduraTraVal = []
    lsLateralEspejoElecVal = []
    lsLateralEspejoManVal  = []
    lsLateralManijaDel     = []
    lsLateralManijaTra     = []
    lsLateralCristalDel    = []
    lsLateralCristalTra    = []

    iPosCRISTAL_DEL=0
    iPosCRISTAL_TRA=1
    iPosESPEJOELEC=2
    iPosESPEJOMAN=3
    iPosMANIJA_DEL=4
    iPosMANIJA_TRA=5
    iPosMOLDURA_DEL=6
    iPosMOLDURA_TRA=7
    iPosPUERTA_DEL=8
    iPosPUERTA_TRA=9
    iPosPUERTA_DEL_PANEL=10
    iPosPUERTA_TRA_PANEL=11
    iPosZOCALO=12

    iPosCRISTAL_DELCambiaDer=0
    iPosCRISTAL_DELCambiaIzq=1
    iPosCRISTAL_TRACambiaDer=2
    iPosCRISTAL_TRACambiaIzq=3
    iPosESPEJOELECCambiaDer=4
    iPosESPEJOELECCambiaIzq=5
    iPosESPEJOMANCambiaDer=6
    iPosESPEJOMANCambiaIzq=7
    iPosMANIJA_DELCambiaDer=8
    iPosMANIJA_DELCambiaIzq=9
    iPosMANIJA_TRACambiaDer=10
    iPosMANIJA_TRACambiaIzq=11
    iPosMOLDURA_DELCambiaDer=12
    iPosMOLDURA_DELCambiaIzq=13
    iPosMOLDURA_TRACambiaDer=14
    iPosMOLDURA_TRACambiaIzq=15
    iPosPUERTA_DELCambiaDer=16
    iPosPUERTA_DELCambiaIzq=17
    iPosPUERTA_TRACambiaDer=18
    iPosPUERTA_TRACambiaIzq=19
    iPosPUERTA_DEL_PANELReparaDer=20
    iPosPUERTA_DEL_PANELReparaIzq=21
    iPosPUERTA_TRA_PANELReparaDer=22
    iPosPUERTA_TRA_PANELReparaIzq=23
    iPosZOCALOCambiaDer=24
    iPosZOCALOReparaDer=25
    iPosZOCALOCambiaIzq=26
    iPosZOCALOReparaIzq=27

    lsLateralCristalDel.append(lsLateralElemsLc[iPosCRISTAL_DEL] if lsLateralLc[iPosCRISTAL_DELCambiaDer]=="1" else "")
    lsLateralCristalDel.append(lsLateralElemsLc[iPosCRISTAL_DEL] if lsLateralLc[iPosCRISTAL_DELCambiaIzq]=="1" else "")
    lsLateralCristalTra.append(lsLateralElemsLc[iPosCRISTAL_TRA] if lsLateralLc[iPosCRISTAL_TRACambiaDer]=="1" else "")
    lsLateralCristalTra.append(lsLateralElemsLc[iPosCRISTAL_TRA] if lsLateralLc[iPosCRISTAL_TRACambiaIzq]=="1" else "")
    lsLateralEspejoElecVal.append(lsLateralElemsLc[iPosESPEJOELEC] if lsLateralLc[iPosESPEJOELECCambiaDer]== "1"else "")
    lsLateralEspejoElecVal.append(lsLateralElemsLc[iPosESPEJOELEC] if lsLateralLc[iPosESPEJOELECCambiaIzq]== "1"else "")
    lsLateralEspejoManVal.append(lsLateralElemsLc[iPosESPEJOMAN] if lsLateralLc[iPosESPEJOMANCambiaDer]== "1"else "")
    lsLateralEspejoManVal.append(lsLateralElemsLc[iPosESPEJOMAN] if lsLateralLc[iPosESPEJOMANCambiaIzq]== "1"else "")
    lsLateralManijaDel.append(lsLateralElemsLc[iPosMANIJA_DEL] if lsLateralLc[iPosMANIJA_DELCambiaDer]== "1"else "")
    lsLateralManijaDel.append(lsLateralElemsLc[iPosMANIJA_DEL] if lsLateralLc[iPosMANIJA_DELCambiaIzq]== "1"else "")
    lsLateralManijaTra.append(lsLateralElemsLc[iPosMANIJA_TRA] if lsLateralLc[iPosMANIJA_TRACambiaDer]== "1"else "")
    lsLateralManijaTra.append(lsLateralElemsLc[iPosMANIJA_TRA] if lsLateralLc[iPosMANIJA_TRACambiaIzq]== "1"else "")
    lsLateralMolduraDelVal.append(lsLateralElemsLc[iPosMOLDURA_DEL] if lsLateralLc[iPosMOLDURA_DELCambiaDer]== "1"else "")
    lsLateralMolduraDelVal.append(lsLateralElemsLc[iPosMOLDURA_DEL] if lsLateralLc[iPosMOLDURA_DELCambiaIzq]== "1"else "")
    lsLateralMolduraTraVal.append(lsLateralElemsLc[iPosMOLDURA_TRA] if lsLateralLc[iPosMOLDURA_TRACambiaDer]== "1"else "")
    lsLateralMolduraTraVal.append(lsLateralElemsLc[iPosMOLDURA_TRA] if lsLateralLc[iPosMOLDURA_TRACambiaIzq]== "1"else "")
    lsLateralCambiaVal.append(lsLateralElemsLc[iPosPUERTA_DEL] if lsLateralLc[iPosPUERTA_DELCambiaDer]=="1" else "")
    lsLateralCambiaVal.append(lsLateralElemsLc[iPosPUERTA_DEL] if lsLateralLc[iPosPUERTA_DELCambiaIzq]=="1" else "")
    lsLateralCambiaVal.append(lsLateralElemsLc[iPosPUERTA_TRA] if lsLateralLc[iPosPUERTA_TRACambiaDer]=="1" else "")
    lsLateralCambiaVal.append(lsLateralElemsLc[iPosPUERTA_TRA] if lsLateralLc[iPosPUERTA_TRACambiaIzq]=="1" else "")
    lsLateralReparaVal.append(lsLateralElemsLc[iPosPUERTA_DEL_PANEL] if lsLateralLc[iPosPUERTA_DEL_PANELReparaDer]=="1" else "")
    lsLateralReparaVal.append(lsLateralElemsLc[iPosPUERTA_DEL_PANEL] if lsLateralLc[iPosPUERTA_DEL_PANELReparaIzq]=="1" else "")
    lsLateralReparaVal.append(lsLateralElemsLc[iPosPUERTA_TRA_PANEL] if lsLateralLc[iPosPUERTA_TRA_PANELReparaDer]=="1" else "")
    lsLateralReparaVal.append(lsLateralElemsLc[iPosPUERTA_TRA_PANEL] if lsLateralLc[iPosPUERTA_TRA_PANELReparaIzq]=="1" else "")
    lsLateralCambiaVal.append(lsLateralElemsLc[iPosZOCALO] if lsLateralLc[iPosZOCALOCambiaDer]=="1" else "")
    lsLateralReparaVal.append(lsLateralElemsLc[iPosZOCALO] if lsLateralLc[iPosZOCALOReparaDer]=="1" else "")
    lsLateralCambiaVal.append(lsLateralElemsLc[iPosZOCALO] if lsLateralLc[iPosZOCALOCambiaIzq]=="1" else "")
    lsLateralReparaVal.append(lsLateralElemsLc[iPosZOCALO] if lsLateralLc[iPosZOCALOReparaIzq]=="1" else "")

    lsLateralCambiaVal     = [i for i in lsLateralCambiaVal if i != ""]
    lsLateralReparaVal     = [i for i in lsLateralReparaVal if i != ""]
    lsLateralMolduraDelVal = [i for i in lsLateralMolduraDelVal if i != ""]
    lsLateralMolduraTraVal = [i for i in lsLateralMolduraTraVal if i != ""]
    lsLateralEspejoElecVal = [i for i in lsLateralEspejoElecVal if i != ""]
    lsLateralEspejoManVal  = [i for i in lsLateralEspejoManVal if i != ""]
    lsLateralManijaDel     = [i for i in lsLateralManijaDel if i != ""]
    lsLateralManijaTra     = [i for i in lsLateralManijaTra if i != ""]
    lsLateralCristalDel    = [i for i in lsLateralCristalDel if i != ""]
    lsLateralCristalTra    = [i for i in lsLateralCristalTra if i != ""]

    return lsLateralCambiaVal,lsLateralReparaVal,\
           lsLateralMolduraDelVal,lsLateralMolduraTraVal,\
           lsLateralEspejoElecVal,lsLateralEspejoManVal,\
           lsLateralManijaDel,lsLateralManijaTra,\
           lsLateralCristalDel,lsLateralCristalTra

def fnGetTraseroElems(iClaseLc, iMarcaLc, iModeloLc, lsTraseroLc):
    lsTraseroElemsLc = ['BAULPORTON','FAROEXT','FAROINT','GUARDABARRO','LUNETA','MOLDURA','PANELCOLACOMP','PARAGOLPE','PANELCOLASUP']

    lsTraseroCambiaVal  = []
    lsTraseroReparaVal  = []
    lsTraseroMolduraVal = []
    lsTraseroFaroExtVal = []
    lsTraseroFaroIntVal = []

    iPosBAULPORTON=0
    iPosFAROEXT=1
    iPosFAROINT=2
    iPosGUARDABARRO=3
    iPosLUNETA=4
    iPosMOLDURA=5
    iPosPANELCOLACOMP=6
    iPosPARAGOLPE=7
    iPosPANELCOLASUP=8

    iPosBAULPORTONCambiaDer=0
    iPosBAULPORTONReparaDer=1
    iPosFAROEXTCambiaDer=2
    iPosFAROEXTCambiaIzq=3
    iPosFAROINTCambiaDer=4
    iPosFAROINTCambiaIzq=5
    iPosGUARDABARROCambiaDer=6
    iPosGUARDABARROReparaDer=7
    iPosGUARDABARROCambiaIzq=8
    iPosGUARDABARROReparaIzq=9
    iPosLUNETACambiaDer=10
    iPosMOLDURACambiaDer=11
    iPosPANELCOLACOMPCambiaDer=12
    iPosPANELCOLACOMPReparaDer=13
    iPosPARAGOLPECambiaDer=14
    iPosPARAGOLPEReparaDer=15

    lsTraseroCambiaVal.append(lsTraseroElemsLc[iPosBAULPORTON] if lsTraseroLc[iPosBAULPORTONCambiaDer] == "1" else "")
    lsTraseroReparaVal.append(lsTraseroElemsLc[iPosBAULPORTON] if lsTraseroLc[iPosBAULPORTONReparaDer] == "1" else "")
    lsTraseroFaroExtVal.append(lsTraseroElemsLc[iPosFAROEXT] if lsTraseroLc[iPosFAROEXTCambiaDer] == "1" else "")
    lsTraseroFaroExtVal.append(lsTraseroElemsLc[iPosFAROEXT] if lsTraseroLc[iPosFAROEXTCambiaIzq] == "1" else "")
    lsTraseroFaroIntVal.append(lsTraseroElemsLc[iPosFAROINT] if lsTraseroLc[iPosFAROINTCambiaDer] == "1" else "")
    lsTraseroFaroIntVal.append(lsTraseroElemsLc[iPosFAROINT] if lsTraseroLc[iPosFAROINTCambiaIzq] == "1" else "")
    lsTraseroCambiaVal.append(lsTraseroElemsLc[iPosGUARDABARRO] if lsTraseroLc[iPosGUARDABARROCambiaDer] == "1" else "")
    lsTraseroReparaVal.append(lsTraseroElemsLc[iPosGUARDABARRO] if lsTraseroLc[iPosGUARDABARROReparaDer] == "1" else "")
    lsTraseroCambiaVal.append(lsTraseroElemsLc[iPosGUARDABARRO] if lsTraseroLc[iPosGUARDABARROCambiaIzq] == "1" else "")
    lsTraseroReparaVal.append(lsTraseroElemsLc[iPosGUARDABARRO] if lsTraseroLc[iPosGUARDABARROReparaIzq] == "1" else "")
    lsTraseroCambiaVal.append(lsTraseroElemsLc[iPosLUNETA] if lsTraseroLc[iPosLUNETACambiaDer] == "1" else "")
    lsTraseroMolduraVal.append(lsTraseroElemsLc[iPosMOLDURA] if lsTraseroLc[iPosMOLDURACambiaDer] == "1" else "")
    lsTraseroCambiaVal.append(lsTraseroElemsLc[iPosPANELCOLACOMP] if lsTraseroLc[iPosPANELCOLACOMPCambiaDer] == "1" else "")
    lsTraseroReparaVal.append(lsTraseroElemsLc[iPosPANELCOLASUP] if lsTraseroLc[iPosPANELCOLACOMPReparaDer] == "1" else "")
    lsTraseroCambiaVal.append(lsTraseroElemsLc[iPosPARAGOLPE] if lsTraseroLc[iPosPARAGOLPECambiaDer] == "1" else "")
    lsTraseroReparaVal.append(lsTraseroElemsLc[iPosPARAGOLPE] if lsTraseroLc[iPosPARAGOLPEReparaDer] == "1" else "")

    blPorton = fnHasPorton(iClaseLc, iMarcaLc, iModeloLc)
    if lsTraseroCambiaVal[iPosBAULPORTON]=="BAULPORTON":
        if blPorton==True: lsTraseroCambiaVal[iPosBAULPORTON]="PORTON"
        else: lsTraseroCambiaVal[iPosBAULPORTON]="BAUL"
    if lsTraseroReparaVal[iPosBAULPORTON]=="BAULPORTON":
        if blPorton==True: lsTraseroReparaVal[iPosBAULPORTON]="PORTON"
        else: lsTraseroReparaVal[iPosBAULPORTON]="BAUL"

    lsTraseroCambiaVal  = [i for i in lsTraseroCambiaVal if i != ""]
    lsTraseroReparaVal  = [i for i in lsTraseroReparaVal if i != ""]
    lsTraseroMolduraVal = [i for i in lsTraseroMolduraVal if i != ""]
    lsTraseroFaroExtVal = [i for i in lsTraseroFaroExtVal if i != ""]
    lsTraseroFaroIntVal = [i for i in lsTraseroFaroIntVal if i != ""]

    return lsTraseroCambiaVal,lsTraseroReparaVal,lsTraseroMolduraVal,lsTraseroFaroExtVal,lsTraseroFaroIntVal

def fnHasPorton(iClaseLc, iMarcaLc, iModeloLc):
    blPorton = False
    if len(dfPorton.loc[(dfPorton['COD_CLASE']==int(iClaseLc))&(dfPorton['COD_MARCA']==int(iMarcaLc))&(dfPorton['COD_MODELO']==int(iModeloLc))])!=0:
        blPorton = True
    return blPorton

def fnIsOld(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,dfData):
    blOld = False
    dfOld = dfData.loc[(dfData['COD_CLASE'] == inCOD_CLASE) & (dfData['COD_MARCA'] == inCOD_MARCA) & (dfData['COD_MODELO'] == inCOD_MODELO)]['VIEJO']

    if len(dfOld) == 0:
        blOld = False
    else:
        blOld = dfData.loc[(dfData['COD_CLASE'] == inCOD_CLASE) & (dfData['COD_MARCA'] == inCOD_MARCA) & (dfData['COD_MODELO'] == inCOD_MODELO)]['VIEJO'].iloc[0]

    if blOld!=True and blOld!=False: blOld = False

    return blOld

###TRASERO##########################################################################################
def fnReparaTrasero(inSEG,inCOD_CLASE,lsRepara):
    ###ToDo:Se necesita separar en gama alta y media? 
    inCOD_PARTE = 2
    lsReparaAve = []
    flAverage = 0

    for index, item in enumerate(lsRepara):
        bfID_ELEM = dfVALOR_MO_UNIF_TRASERO.loc[(dfVALOR_MO_UNIF_TRASERO['COD_CLASE'] == inCOD_CLASE) &
                                                (dfVALOR_MO_UNIF_TRASERO['COD_PARTE'] == inCOD_PARTE) &
                        (dfVALOR_MO_UNIF_TRASERO['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                       [['VALOR_MO_MEAN','CANT_HS_PINT_MEAN','VALOR_MAT_PINT_MEAN']]

        flVALOR_MO_MEAN     = bfID_ELEM['VALOR_MO_MEAN']
        flCANT_HS_PINT_MEAN = bfID_ELEM['CANT_HS_PINT_MEAN']

        ###Todo:Sacar############################################################################
        flVALOR_MO_MEAN     = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2)       
        flCANT_HS_PINT_MEAN = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfPintura),2) 
        ###Todo:Sacar############################################################################

        flAverage=np.round((flVALOR_MO_MEAN + flCANT_HS_PINT_MEAN + bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        lsReparaAve.append(flAverage)

    for index, item in enumerate(lsReparaAve): lsReparaAve[index] = list(set(item))[0]

    return lsReparaAve

def fnCambiaTrasero(inSEG,inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,lsRepone,isAlta):
    inCOD_PARTE = 2
    lsReponeAve = []
    flAverage   = 0
    flAverageMD = 0 #BORRAR

    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['COD_CLASE']  == inCOD_CLASE)  &
                                                 (dfVALOR_REPUESTO_MO_Unif['COD_MARCA']  == inCOD_MARCA)  & 
                                                 (dfVALOR_REPUESTO_MO_Unif['COD_MODELO'] == inCOD_MODELO) &
                                                 (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']  == inCOD_PARTE)  & 
                    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))][['PRECIO_MEAN']]

        flMean = np.round(bfID_ELEM['PRECIO_MEAN'].mean(),2)
        flAverage = pd.Series([flMean])
        
        #BORRAR
        if   item=="BAUL"         :flAverageMD = paramal.bfBaul_Porton if isAlta else param.bfBaul_Porton
        elif item=="PORTON"       :flAverageMD = paramal.bfBaul_Porton if isAlta else param.bfBaul_Porton
        elif item=="GUARDABARRO"  :flAverageMD = paramal.bfGuardabarro if isAlta else param.bfGuardabarro
        elif item=="LUNETA"       :flAverageMD = paramal.bfLuneta      if isAlta else param.bfLuneta
        elif item=="PANELCOLACOMP":flAverageMD = paramal.bfPanel_Cola  if isAlta else param.bfPanel_Cola
        elif item=="PANELCOLASUP" :flAverageMD = paramal.bfPanel_Sup   if isAlta else param.bfPanel_Sup
        elif item=="PARAGOLPE"    :flAverageMD = paramal.bfParagolpe   if isAlta else param.bfParagolpe

    for index, item in enumerate(lsReponeAve): lsReponeAve[index] = list(set(item))[0]

    return lsReponeAve

def fnCambiaPinturaTrasero(inSEG,inCOD_CLASE,lsRepone):
    inCOD_PARTE = 2
    lsReponePintAve=[]
    lsReponeMoAv=[]
    flAverage=0
    flMoAv=0

    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_VALOR_MAT_TRASERO.loc[(dfVALOR_REPUESTO_VALOR_MAT_TRASERO['COD_CLASE']==inCOD_CLASE) & 
                                                           (dfVALOR_REPUESTO_VALOR_MAT_TRASERO['COD_PARTE']==inCOD_PARTE) &
                    (dfVALOR_REPUESTO_VALOR_MAT_TRASERO['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                              [['VALOR_MO_MEAN','CANT_HS_PINT_MEAN','VALOR_MAT_PINT_MEAN']]

        flVALOR_MO_MEAN     = bfID_ELEM['VALOR_MO_MEAN']
        flCANT_HS_PINT_MEAN = bfID_ELEM['CANT_HS_PINT_MEAN']

        ###Todo:Sacar############################################################################
        flVALOR_MO_MEAN     = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2)
        flCANT_HS_PINT_MEAN = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfPintura),2)
        ###Todo:Sacar############################################################################

        flAverage = np.round((flCANT_HS_PINT_MEAN + bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        flMoAv    = np.round(flVALOR_MO_MEAN,2)

        if len(flAverage)==0:flAverage=[0]
        if len(flMoAv)==0:flMoAv=[0]

        lsReponePintAve.append(flAverage)
        lsReponeMoAv.append(flMoAv)

    for index, item in enumerate(lsReponePintAve): lsReponePintAve[index]=list(set(item))[0]
    for index, item in enumerate(lsReponeMoAv)   : lsReponeMoAv[index]=list(set(item))[0]

    return lsReponePintAve,lsReponeMoAv

def fnMolduraTrasero(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 2
    moldCtro    = ['PARAGOLPE EMBELLEC / MOLD']
    lsVersion   = ['1','2','3']
    lsMoldCtro  = []

    dfMOLD_CTRO = dfMOLDURA.loc[(dfMOLDURA['COD_CLASE']  == inCOD_CLASE)  & 
                                (dfMOLDURA['COD_MARCA']  == inCOD_MARCA)  &
                                (dfMOLDURA['COD_MODELO'] == inCOD_MODELO) & 
                                (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, moldCtro))))].sort_values(['VALOR'], ascending=[False])

    dfTmp = dfMOLD_CTRO.loc[~dfMOLD_CTRO['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]

    if len(dfTmp)!=0:
        flValue = dfTmp['VALOR'].mean() 
    else:
        if isAlta: flValue = paramal.bfMoldura
        else:      flValue = param.bfMoldura
    lsMoldCtro.append(round(flValue  + param.bfMOMinimo,2))
    
    return lsMoldCtro

def fnFaroExtTrasero(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 2
    faroDer = ['FARO DER']
    lsVersion = ['1','2','3','4','5','6']
    lsFaroExt = []

    dfFARO_EXT = dfFARO.loc[(dfFARO['COD_CLASE']  == inCOD_CLASE)  & 
                            (dfFARO['COD_MARCA']  == inCOD_MARCA)  &
                            (dfFARO['COD_MODELO'] == inCOD_MODELO) & 
                            (dfFARO['COD_PARTE']  == inCOD_PARTE)  &
                            (dfFARO['DESC_ELEM'].str.contains('|'.join(map(re.escape, faroDer))))].sort_values(['VALOR'], ascending=[False])

    dfTmp = dfFARO_EXT.loc[~dfFARO_EXT['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]

    if len(dfTmp)!=0:
        flValue = dfTmp['VALOR'].mean()
    else:
        if isAlta: flValue = paramal.bfFaro_Ext
        else:      flValue = param.bfFaro_Ext
    lsFaroExt.append(round(flValue + param.bfMOMinimo,2))
        
    return lsFaroExt

def fnFaroIntTrasero(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 2
    faroDer = ['FARO DER 1']
    lsFaroInt = []

    dfFARO_INT = dfFARO.loc[(dfFARO['COD_CLASE']  == inCOD_CLASE)  & 
                            (dfFARO['COD_MARCA']  == inCOD_MARCA)  &
                            (dfFARO['COD_MODELO'] == inCOD_MODELO) & 
                            (dfFARO['COD_PARTE']  == inCOD_PARTE)  & 
                            (dfFARO['DESC_ELEM'].str.contains('|'.join(map(re.escape, faroDer))))].sort_values(['VALOR'], ascending=[False])

    if len(dfFARO_INT)!=0:
        flValue = dfFARO_INT['VALOR'].mean()
    else:
        if isAlta: flValue = paramal.bfFaro_Int
        else:      flValue = param.bfFaro_Int 
    lsFaroInt.append(round(flValue + param.bfMOMinimo,2))

    return lsFaroInt
######################################################################################################
###FRENTE#############################################################################################
def fnReparaFrente(inSEG,inCOD_CLASE,lsRepara):
    ###ToDo:Se necesita separar en gama alta y media?     
    inCOD_PARTE = 1
    lsReparaAve = []
    flAverage = 0
    for index, item in enumerate(lsRepara):
        bfID_ELEM = dfVALOR_MO_UNIF_FRENTE.loc[(dfVALOR_MO_UNIF_FRENTE['COD_CLASE']==inCOD_CLASE) &
                                               (dfVALOR_MO_UNIF_FRENTE['COD_PARTE']==inCOD_PARTE) &
                                (dfVALOR_MO_UNIF_FRENTE['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                              [['VALOR_MO_MEAN','CANT_HS_PINT_MEAN','VALOR_MAT_PINT_MEAN']]

        flVALOR_MO_MEAN      = bfID_ELEM['VALOR_MO_MEAN']
        flCANT_HS_PINT_MEAN  = bfID_ELEM['CANT_HS_PINT_MEAN']

        ###Todo:Sacar############################################################################
        flVALOR_MO_MEAN       = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2) 
        flCANT_HS_PINT_MEAN   = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfMObra),2) 
        ###Todo:Sacar############################################################################

        flAverage = np.round((flVALOR_MO_MEAN + flCANT_HS_PINT_MEAN + bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        lsReparaAve.append(flAverage)

    for index, item in enumerate(lsReparaAve):
        lsReparaAve[index]=list(set(item))[0]

    return lsReparaAve

def fnCambiaFrente(inSEG,inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,lsRepone,isAlta):
    inCOD_PARTE = 1
    lsReponeAve = []
    flAverage   = 0
    flAverageMD = 0 #BORRAR

    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['COD_CLASE'] == inCOD_CLASE)   &
                                                 (dfVALOR_REPUESTO_MO_Unif['COD_MARCA'] == inCOD_MARCA)   & 
                                                 (dfVALOR_REPUESTO_MO_Unif['COD_MODELO'] == inCOD_MODELO) &
                                                 (dfVALOR_REPUESTO_MO_Unif['COD_PARTE'] == inCOD_PARTE)   & 
                    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))][['PRECIO_MEAN']]

        flMean = np.round(bfID_ELEM['PRECIO_MEAN'].mean(),2)
        flAverage = pd.Series([flMean])

        #BORRAR
        if item  =="CAPOT"         :flAverageMD = paramal.bfFrt_GA_Del_Capot if isAlta          else param.bfFrt_GM_Del_Capot
        elif item=="FRENTE"        :flAverageMD = paramal.bfFrt_GA_Del_Frente if isAlta         else param.bfFrt_GM_Del_Frente
        elif item=="GUARDABARRO"   :flAverageMD = paramal.bfFrt_GA_Del_Guardabarro if isAlta    else param.bfFrt_GM_Del_Guardabarro
        elif item=="PARAGOLPE_ALMA":flAverageMD = paramal.bfFrt_GA_Del_Paragolpe_Alma if isAlta else param.bfFrt_GM_Del_Paragolpe_Alma
        elif item=="PARAGOLPE_CTRO":flAverageMD = paramal.bfFrt_GA_Del_Paragolpe_Ctro if isAlta else param.bfFrt_GM_Del_Paragolpe_Ctro

    for index, item in enumerate(lsReponeAve): lsReponeAve[index] = list(set(item))[0]

    return lsReponeAve

def fnCambiaPinturaFrente(inSEG,inCOD_CLASE,lsRepone):
    inCOD_PARTE = 1
    lsReponePintAve = []
    lsReponeMoAv    = []

    flAverage = 0
    flMoAv    = 0

    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_VALOR_MAT_FRENTE.loc[(dfVALOR_REPUESTO_VALOR_MAT_FRENTE['COD_CLASE']==inCOD_CLASE) &
                                                          (dfVALOR_REPUESTO_VALOR_MAT_FRENTE['COD_PARTE']==inCOD_PARTE) &
                        (dfVALOR_REPUESTO_VALOR_MAT_FRENTE['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                                 [['VALOR_MO_MEAN','CANT_HS_PINT_MEAN','VALOR_MAT_PINT_MEAN']]

        flVALOR_MO_MEAN = bfID_ELEM['VALOR_MO_MEAN']
        flCANT_HS_PINT_MEAN = bfID_ELEM['CANT_HS_PINT_MEAN']
        
         ###Todo:Sacar############################################################################
        flVALOR_MO_MEAN = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2) 
        flCANT_HS_PINT_MEAN = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfPintura),2) 
         ###Todo:Sacar############################################################################

        flAverage = np.round((flCANT_HS_PINT_MEAN+bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        flMoAv  = np.round(flVALOR_MO_MEAN,2)

        if len(flAverage) == 0: flAverage = [0]
        if len(flMoAv) == 0: flMoAv = [0]
                
        lsReponePintAve.append(flAverage)
        lsReponeMoAv.append(flMoAv)

    for index, item in enumerate(lsReponePintAve): lsReponePintAve[index] = list(set(item))[0]
    for index, item in enumerate(lsReponeMoAv)   : lsReponeMoAv[index] = list(set(item))[0]

    return lsReponePintAve,lsReponeMoAv

def fnParabrisas(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 1
    espPara = ['PARABRISAS']
    lsMeanPara = []

    dfMOLD_LATERAL = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['COD_CLASE']  == inCOD_CLASE)  &
                                                  (dfVALOR_REPUESTO_MO_Unif['COD_MARCA']  == inCOD_MARCA)  &
                                                  (dfVALOR_REPUESTO_MO_Unif['COD_MODELO'] == inCOD_MODELO) &
                                                  (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']  == inCOD_PARTE)  &
                    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].str.contains('|'.join(map(re.escape, espPara))))].sort_values(['PRECIO_MEAN'], ascending=[False])

    if len(dfMOLD_LATERAL)!=0:
        flValue = dfMOLD_LATERAL['PRECIO_MEAN'].mean() 
    else:
        if isAlta: flValue = paramal.bfFrt_GA_Del_Parabrisas
        else:      flValue = param.bfFrt_GM_Del_Parabrisas
    lsMeanPara.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanPara

def fnParagolpe_Rejilla(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 1
    espPara = ['PARAGOLPE_REJILLA']
    lsMeanPara = []

    dfPARAGOLPE_REJILLA = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['COD_CLASE']  == inCOD_CLASE)  &
                                                       (dfVALOR_REPUESTO_MO_Unif['COD_MARCA']  == inCOD_MARCA)  &
                                                       (dfVALOR_REPUESTO_MO_Unif['COD_MODELO'] == inCOD_MODELO) &
                                                       (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']  == inCOD_PARTE)  &
                        (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].str.contains('|'.join(map(re.escape, espPara))))].sort_values(['PRECIO_MEAN'], ascending=[False])

    if len(dfPARAGOLPE_REJILLA)!=0:
        flValue = dfPARAGOLPE_REJILLA['PRECIO_MEAN'].mean() 
    else:
        if isAlta: flValue = paramal.bfFrt_GA_Del_Paragolpe_Rejilla
        else:      flValue = param.bfFrt_GM_Del_Paragolpe_Rejilla
    lsMeanPara.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanPara

def fnRejilla_Radiador(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 1
    espPara = ['REJILLA_RADIADOR']
    lsMeanPara = []

    dfREJILLA_RADIADOR = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['COD_CLASE']  == inCOD_CLASE)  &
                                                      (dfVALOR_REPUESTO_MO_Unif['COD_MARCA']  == inCOD_MARCA)  &
                                                      (dfVALOR_REPUESTO_MO_Unif['COD_MODELO'] == inCOD_MODELO) &
                                                      (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']  == inCOD_PARTE)  &
    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].str.contains('|'.join(map(re.escape, espPara))))].sort_values(['PRECIO_MEAN'], ascending=[False])

    if len(dfREJILLA_RADIADOR)!=0:
        flValue = dfREJILLA_RADIADOR['PRECIO_MEAN'].mean() 
    else:
        if isAlta: flValue = paramal.bfFrt_GA_Del_Rejilla_Radiador
        else:      flValue = param.bfFrt_GM_Del_Rejilla_Radiador
    lsMeanPara.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanPara

def fnFaroFrente(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 1
    faroDer = ['FARO DER']
    lsVersion = ['1','2','3','4']
    lsMeanFaro = []

    dfFARO_FRENTE = dfFARO.loc[(dfFARO['COD_CLASE']  == inCOD_CLASE)  &
                               (dfFARO['COD_MARCA']  == inCOD_MARCA)  &
                               (dfFARO['COD_MODELO'] == inCOD_MODELO) &
                               (dfFARO['COD_PARTE']  == inCOD_PARTE)  &
                               (dfFARO['DESC_ELEM'].str.contains('|'.join(map(re.escape, faroDer))))].sort_values(['VALOR'], ascending=[False])

    dfTmp = dfFARO_FRENTE.loc[~dfFARO_FRENTE['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]

    if len(dfTmp)!=0:
        flValue = dfTmp['VALOR'].mean() 
    else:
        if isAlta: flValue = paramal.bfFrt_GA_Del_Faro
        else:      flValue = param.bfFrt_GM_Del_Faro  
    lsMeanFaro.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanFaro

def fnFaritoFrente(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 1
    faroDer = ['FARITO DER']
    lsVersion = ['1','2','3','4']
    lsMeanFaro = []

    dfFARITO_FRENTE = dfFARO.loc[(dfFARO['COD_CLASE']  == inCOD_CLASE)  &
                               (dfFARO['COD_MARCA']  == inCOD_MARCA)  &
                               (dfFARO['COD_MODELO'] == inCOD_MODELO) &
                               (dfFARO['COD_PARTE']  == inCOD_PARTE)  &
                               (dfFARO['DESC_ELEM'].str.contains('|'.join(map(re.escape, faroDer))))].sort_values(['VALOR'], ascending=[False])

    dfTmp = dfFARITO_FRENTE.loc[~dfFARITO_FRENTE['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]

    if len(dfTmp)!=0:
        flValue = dfTmp['VALOR'].mean() 
    else:
        if isAlta: flValue = paramal.bfFrt_GA_Del_Farito
        else:      flValue = param.bfFrt_GM_Del_Farito  
    lsMeanFaro.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanFaro


######################################################################################################
###LATERAL############################################################################################
def fnReparaLateral(inSEG,inCOD_CLASE,lsRepara):
    ###ToDo:Se necesita separar en gama alta y media?     
    inCOD_PARTE = 3
    lsReparaAve = []
    flAverage = 0
    for index, item in enumerate(lsRepara):
        bfID_ELEM = dfVALOR_MO_UNIF_LATERAL.loc[(dfVALOR_MO_UNIF_LATERAL['COD_CLASE']==inCOD_CLASE)&
                                                (dfVALOR_MO_UNIF_LATERAL['COD_PARTE']==inCOD_PARTE)&
                                (dfVALOR_MO_UNIF_LATERAL['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                               [['VALOR_MO_MEAN','CANT_HS_PINT_MEAN','VALOR_MAT_PINT_MEAN']]

        flVALOR_MO_MEAN      = bfID_ELEM['VALOR_MO_MEAN']
        flCANT_HS_PINT_MEAN  = bfID_ELEM['CANT_HS_PINT_MEAN']

        ###Todo:Sacar############################################################################
        flVALOR_MO_MEAN       = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2) 
        flCANT_HS_PINT_MEAN   = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfMObra),2)
        ###Todo:Sacar############################################################################

        flAverage = np.round((flVALOR_MO_MEAN + flCANT_HS_PINT_MEAN + bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        lsReparaAve.append(flAverage)

    for index, item in enumerate(lsReparaAve): lsReparaAve[index]=list(set(item))[0]

    return lsReparaAve

def fnCambiaLateral(inSEG,inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,lsRepone,isAlta):
    inCOD_PARTE = 3
    lsReponeAve = []
    flAverage   = 0
    flAverageMD = 0 #BORRAR

    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['COD_CLASE']  == inCOD_CLASE)  &
                                                 (dfVALOR_REPUESTO_MO_Unif['COD_MARCA']  == inCOD_MARCA)  &
                                                 (dfVALOR_REPUESTO_MO_Unif['COD_MODELO'] == inCOD_MODELO) &
                                                 (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']  == inCOD_PARTE)  &
                    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))][['PRECIO_MEAN']]

        flMean = np.round(bfID_ELEM['PRECIO_MEAN'].mean(),2)
        flAverage = pd.Series([flMean])

        #BORRAR
        if   item=="PUERTA_DEL"      :flAverageMD = paramal.bfLat_Puerta_Delantera if isAlta  else param.bfLat_Puerta_Delantera
        elif item=="PUERTA_TRA"      :flAverageMD = paramal.bfLat_Puerta_Trasera if isAlta    else param.bfLat_Puerta_Trasera
        elif item=="PUERTA_DEL_PANEL":flAverageMD = paramal.bfLat_Puerta_Panel_Del  if isAlta else param.bfLat_Puerta_Panel_Del
        elif item=="PUERTA_TRA_PANEL":flAverageMD = paramal.bfLat_Puerta_Panel_Tras if isAlta else param.bfLat_Puerta_Panel_Tras
        elif item=="ZOCALO"          :flAverageMD = paramal.bfLat_Zocalo if isAlta            else param.bfLat_Zocalo

    for index, item in enumerate(lsReponeAve): lsReponeAve[index] = list(set(item))[0]

    return lsReponeAve

def fnCambiaPinturaLateral(inSEG,inCOD_CLASE,lsRepone):
    inCOD_PARTE = 3
    lsReponePintAve = []
    lsReponeMoAv    = []

    flAverage = 0
    flMoAv    = 0

    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_VALOR_MAT_LATERAL.loc[(dfVALOR_REPUESTO_VALOR_MAT_LATERAL['SEG']==inSEG) &
                                             (dfVALOR_REPUESTO_VALOR_MAT_LATERAL['COD_CLASE']==inCOD_CLASE) &
                                             (dfVALOR_REPUESTO_VALOR_MAT_LATERAL['COD_PARTE']==inCOD_PARTE) &
                        (dfVALOR_REPUESTO_VALOR_MAT_LATERAL['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                                  [['VALOR_MO_MEAN','CANT_HS_PINT_MEAN','VALOR_MAT_PINT_MEAN']]

        flVALOR_MO_MEAN = bfID_ELEM['VALOR_MO_MEAN']
        flCANT_HS_PINT_MEAN = bfID_ELEM['CANT_HS_PINT_MEAN']
        
        ###Todo:Sacar############################################################################
        flVALOR_MO_MEAN = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2)
        flCANT_HS_PINT_MEAN = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfPintura),2)
        ###Todo:Sacar############################################################################

        flAverage = np.round((flCANT_HS_PINT_MEAN+bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        flMoAv  = np.round(flVALOR_MO_MEAN,2)

        if len(flAverage) == 0: flAverage = [0]
        if len(flMoAv) == 0: flMoAv = [0]
                
        lsReponePintAve.append(flAverage)
        lsReponeMoAv.append(flMoAv)

    for index, item in enumerate(lsReponePintAve): lsReponePintAve[index] = list(set(item))[0]
    for index, item in enumerate(lsReponeMoAv): lsReponeMoAv[index] = list(set(item))[0]

    return lsReponePintAve,lsReponeMoAv

def fnEspejoLateralElec(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    espElec = ['ESPEJO ELECTRICO']
    lsVersion = ['1','2','3','4','5']
    lsMeanEsp = []

    dfESPEJO_ELEC = dfESPEJO.loc[(dfESPEJO['COD_CLASE']  == inCOD_CLASE)  &
                                 (dfESPEJO['COD_MARCA']  == inCOD_MARCA)  &
                                 (dfESPEJO['COD_MODELO'] == inCOD_MODELO) &
                                 (dfESPEJO['COD_PARTE']  == inCOD_PARTE)  &
                                 (dfESPEJO['DESC_ELEM'].str.contains('|'.join(map(re.escape, espElec))))].sort_values(['VALOR'], ascending=[False])

    dfTmp = dfESPEJO_ELEC.loc[~dfESPEJO_ELEC['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]

    if len(dfTmp)!=0:
        flValue = dfTmp['VALOR'].mean() 
    else:
        if isAlta: flValue = paramal.bfLat_Espejo_Electrico 
        else:      flValue = param.bfLat_Espejo_Electrico 
    lsMeanEsp.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanEsp

def fnEspejoLateralMan(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    espMan = ['ESPEJO MANUAL']
    lsVersion = ['1','2','3','4','5']
    lsMeanEsp = []

    dfESPEJO_MAN = dfESPEJO.loc[(dfESPEJO['COD_MARCA'] == inCOD_MARCA)   &
                                (dfESPEJO['COD_MODELO'] == inCOD_MODELO) &
                                (dfESPEJO['COD_PARTE']  == inCOD_PARTE)  &
                                (dfESPEJO['COD_PARTE']  == inCOD_PARTE)  &
                                (dfESPEJO['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMan))))].sort_values(['VALOR'], ascending=[False])

    dfTmp = dfESPEJO_MAN.loc[~dfESPEJO_MAN['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]

    if len(dfTmp)!=0:
        flValue = dfTmp['VALOR'].mean() 
    else:
        if isAlta: flValue = paramal.bfLat_Espejo_Manual 
        else:      flValue = param.bfLat_Espejo_Manual
    lsMeanEsp.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanEsp

def fnManijaLateralDel(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    lsManija = ['DEL MANIJA']
    lsVersion = ['1','2','3','4','5']
    lsMeanMan = []

    dfMANIJA_RST  = dfMANIJA.loc[(dfMANIJA['COD_CLASE']  == inCOD_CLASE)  &
                                 (dfMANIJA['COD_MARCA']  == inCOD_MARCA)  &
                                 (dfMANIJA['COD_MODELO'] == inCOD_MODELO) &
                                 (dfMANIJA['COD_PARTE']  == inCOD_PARTE)  &
                                 (dfMANIJA['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsManija))))].sort_values(['VALOR'], ascending=[False])

    dfTmp = dfMANIJA_RST.loc[~dfMANIJA_RST['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]

    if len(dfTmp)!=0:
        flValue = dfTmp['VALOR'].mean() 
    else:
        if isAlta: flValue = paramal.bfLat_Manija_Pta_Del
        else:      flValue = param.bfLat_Manija_Pta_Del
    lsMeanMan.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanMan

def fnManijaLateralTra(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    lsManija = ['TRAS MANIJA']
    lsVersion = ['1','2','3','4','5']
    lsMeanMan = []

    dfMANIJA_RST  = dfMANIJA.loc[(dfMANIJA['COD_CLASE']  == inCOD_CLASE)  &
                                 (dfMANIJA['COD_MARCA']  == inCOD_MARCA)  &
                                 (dfMANIJA['COD_MODELO'] == inCOD_MODELO) &
                                 (dfMANIJA['COD_PARTE']  == inCOD_PARTE)  &
                                 (dfMANIJA['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsManija))))].sort_values(['VALOR'], ascending=[False])

    dfTmp = dfMANIJA_RST.loc[~dfMANIJA_RST['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]

    if len(dfTmp)!=0:
        flValue = dfTmp['VALOR'].mean()
    else:
        if isAlta: flValue = paramal.bfLat_Manija_Pta_Tras
        else:      flValue = param.bfLat_Manija_Pta_Tras
    lsMeanMan.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanMan

def fnMolduraLateralDel(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    espMold = ['DEL MOLD']
    lsMeanMold = []

    dfMOLD_LATERAL = dfMOLDURA.loc[(dfMOLDURA['COD_CLASE']  == inCOD_CLASE)  & 
                                   (dfMOLDURA['COD_MARCA']  == inCOD_MARCA)  &
                                   (dfMOLDURA['COD_MODELO'] == inCOD_MODELO) & 
                                   (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                   (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))].sort_values(['VALOR'], ascending=[False])

    if len(dfMOLD_LATERAL)!=0:
        flValue = dfMOLD_LATERAL['VALOR'].mean() 
    else:
        if isAlta: flValue = paramal.bfLat_Moldura_Pta_Del
        else:      flValue = param.bfLat_Moldura_Pta_Del
    lsMeanMold.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanMold

def fnMolduraLateralTra(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    espMold = ['TRAS MOLD']
    lsMeanMold = []

    dfMOLD_LATERAL = dfMOLDURA.loc[(dfMOLDURA['COD_CLASE']  == inCOD_CLASE)  &
                                   (dfMOLDURA['COD_MARCA']  == inCOD_MARCA)  &
                                   (dfMOLDURA['COD_MODELO'] == inCOD_MODELO) &
                                   (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                   (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))].sort_values(['VALOR'], ascending=[False])

    if len(dfMOLD_LATERAL)!=0:
        flValue = dfMOLD_LATERAL['VALOR'].mean() 
    else:
        if isAlta: flValue = paramal.bfLat_Moldura_Pta_Tras
        else:      flValue = param.bfLat_Moldura_Pta_Tras
    lsMeanMold.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanMold

def fnCristalLateralDel(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    espMold = ['DEL CRISTAL']
    lsMeanMold = []

    dfMOLD_LATERAL = dfCRISTAL.loc[(dfCRISTAL['COD_CLASE']  == inCOD_CLASE)  & 
                                   (dfCRISTAL['COD_MARCA']  == inCOD_MARCA)  &
                                   (dfCRISTAL['COD_MODELO'] == inCOD_MODELO) &
                                   (dfCRISTAL['COD_PARTE']  == inCOD_PARTE)  &
                                   (dfCRISTAL['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))].sort_values(['VALOR'], ascending=[False])

    if len(dfMOLD_LATERAL)!=0:
        flValue = dfMOLD_LATERAL['VALOR'].mean()
    else:
        if isAlta: flValue = paramal.bfLat_Cristal_Delantero
        else:      flValue = param.bfLat_Cristal_Delantero
    lsMeanMold.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanMold

def fnCristalLateralTra(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    espMold = ['TRAS CRISTAL']
    lsMeanMold = []

    dfMOLD_LATERAL = dfCRISTAL.loc[(dfCRISTAL['COD_CLASE']  == inCOD_CLASE)  & 
                                   (dfCRISTAL['COD_MARCA']  == inCOD_MARCA)  &
                                   (dfCRISTAL['COD_MODELO'] == inCOD_MODELO) &
                                   (dfCRISTAL['COD_PARTE']  == inCOD_PARTE)  &
                                   (dfCRISTAL['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))].sort_values(['VALOR'], ascending=[False])

    if len(dfMOLD_LATERAL)!=0:
        flValue = dfMOLD_LATERAL['VALOR'].mean()
    else:
        if isAlta: flValue = paramal.bfLat_Cristal_Trasero
        else:      flValue = param.bfLat_Cristal_Trasero
    lsMeanMold.append(round(flValue + param.bfMOMinimo,2))

    return lsMeanMold
####################################################################################
####################################################################################
def resumeDataBrief(intCLIENTE,fltFrente,fltLateral,fltTrasero):
    intClientType = 2
    if intCLIENTE.isnumeric(): intClientType = int(intCLIENTE)

    ftSum = (fltFrente + fltLateral + fltTrasero) * float(param.bfAjuste)

    if intClientType == 1: ftSum *= float(param.bfAsegurado)
    else                 : ftSum *= float(param.bfTercero)

    txtValorTotal = "<span id=\"CostBrief\" class=\"pure-form-message-inline\" style=\"text-align:left;font-family:'helvetica neue';font-size:100%;color:rgb(170,27,23);\">Sugerido&nbsp$&nbsp{0:0.2f}".format(ftSum)+"</span>"
    return txtValorTotal

def fnWriteLog(CLIENTE,CLASE,MARCA,MODELO,SINIESTRO,PERITO,VALORPERITO,FRENTE,LATERAL,TRASERO,lsValuesResultWrite):
    logger.info (f"lsValuesResultWrite: {lsValuesResultWrite}")
    bfWrite =True
    ts = datetime.datetime.now().timestamp()

    bfValues = str(ts)+","+str(CLIENTE)+","+str(CLASE)+","+str(MARCA)+","+str(MODELO)+",'"+SINIESTRO+"','"+PERITO.replace(',','')+"','"+VALORPERITO+"','"+FRENTE+"','"+LATERAL+"','"+TRASERO+"',"

    bfValues += str(lsValuesResultWrite[0])+","+ str(lsValuesResultWrite[1])+","+ str(lsValuesResultWrite[2])+","+ str(lsValuesResultWrite[3])+","\
             +  str(lsValuesResultWrite[4])+","+ str(lsValuesResultWrite[5])+","+ str(lsValuesResultWrite[6])+","+ str(lsValuesResultWrite[7])+","\
             +  str(lsValuesResultWrite[8])+","+ str(lsValuesResultWrite[9])+","+ str(lsValuesResultWrite[10])+","+str(lsValuesResultWrite[11])+","\
             +  str(lsValuesResultWrite[12])+","+str(lsValuesResultWrite[13])+","+str(lsValuesResultWrite[14])+","+str(lsValuesResultWrite[15])+","\
             +  str(lsValuesResultWrite[16])+","+str(lsValuesResultWrite[17])+","+str(lsValuesResultWrite[18])+","+str(lsValuesResultWrite[19])+","\
             +  str(lsValuesResultWrite[20])+","+str(lsValuesResultWrite[21])+","+str(lsValuesResultWrite[22])+","+str(lsValuesResultWrite[23])+","\
             +  str(lsValuesResultWrite[24])+","+str(lsValuesResultWrite[25])+","+str(lsValuesResultWrite[26])+","+str(lsValuesResultWrite[27])+","\
             +  str(lsValuesResultWrite[28])+","+str(lsValuesResultWrite[29])+","+str(lsValuesResultWrite[30])+","+str(lsValuesResultWrite[31])+","
             
    bfValues += str(param.bfAsegurado)+","+str(param.bfTercero)+","+str(param.bfMObra)+","+str(param.bfPintura)+","+str(param.bfAjuste)

    bfClause = '''INSERT INTO logpresupuestosV1 (timestamp,cliente,clase,marca,modelo,siniestro,Perito,ValorPerito,frente,lateralr,trasero,
                                                 frReparaPintura,frReponeElemento,frReponePintura,frReponeManoObra,frReponeFarito,frReponeFaro,
                                                 frReponeFaro_Auxiliar,frReponeParabrisas,frReponeParagolpe_Rejilla,frReponeRejilla_Radiador,frTotal,
                                                 ltReparaPintura,ltReponeElemento,ltReponePintura,ltReponeManoObra,ltReponeEspejoEle,
                                                 ltReponeEspejoMan,ltReponeManijaDel,ltReponeManijaTra,ltReponeMolduraDel,ltReponeMolduraTra,
                                                 ltReponeCristalDel,ltReponeCristalTra,ltTotal,
                                                 trReparaPintura,trReponeElemento,trReponePintura,trReponeManoObra,
                                                 trReponeMoldura,trReponeFaroExt,trReponeFaroInt,trTotal,
                                                 Asegurado,Tercero,MObra,Pintura,Ajuste) VALUES (''' + bfValues + ');'
    logger.info (f"bfClause: {bfClause}")
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text(bfClause))
        if conn.in_transaction(): conn.commit()
        conn.close()
        engine.dispose()
    except Exception as e:
        bfWrite =False
        logger.error(f"Error: "+str(e))
    return bfWrite

def fnWriteLogBrief(CLIENTE,CLASE,MARCA,MODELO,SINIESTRO,PERITO,VALORPERITO):    
    bfWrite =True
    ts = datetime.datetime.now().timestamp()

    bfValues = str(ts)+","+str(CLIENTE)+","+str(CLASE)+","+str(MARCA)+","+str(MODELO)+",'"+SINIESTRO+"','"+PERITO.replace(',','')+"','"+VALORPERITO+"'"
    print(bfValues)
    bfClause = '''INSERT INTO logpresupuestosV1 (timestamp,cliente,clase,marca,modelo,siniestro,Perito,ValorPerito) VALUES (''' + bfValues + ');'
    try:
        engine = db.create_engine(cDBConnValue)
        conn = engine.connect()
        result = conn.execute(text(bfClause))
        if conn.in_transaction(): conn.commit()
        conn.close()
        engine.dispose()
    except Exception as e:
        bfWrite =False
        logger.error(f"Error: "+str(e))
    return bfWrite

def fnAltaGama(CLASE,MARCA,MODELO):
    bAltaGama = False
    
    engine = db.create_engine(cDBConnValue)
    conn = engine.connect()
    result = conn.execute(text("SELECT al FROM marcamodelo where clase=" + str(CLASE) + " and marca=" + str(MARCA) + " and modelo=" + str(MODELO) +";"))
    for row in result:
        if row[0] == 1: bAltaGama = True
    conn.close()
    engine.dispose()
    return bAltaGama

def leer_ultimas_lineas_log(num_lineas=1):
    try:
        with open(LOG_FILE_NAME, 'r') as f:
            lines = f.readlines()
            ultimas_lineas = lines[-num_lineas:]
            return [line.strip() for line in ultimas_lineas] 
    except Exception as e:
        logger.error(f"Error: LOG_FILE_NAME {e}", exc_info=True)
        return []