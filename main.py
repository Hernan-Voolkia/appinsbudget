from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import warnings
import datetime
import re
import pandas as pd
import numpy as np
import sqlalchemy as db
from sqlalchemy import text, exc

import param
import paramal
import search
import marca
import index
import admvalue
import dbstatus

warnings.filterwarnings("ignore")
np.set_printoptions(suppress=True)

df = pd.read_csv('./data/dfBaseCleanSumV1.csv',sep=';',encoding='utf-8',decimal='.',
                 dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                          'COD_PARTE':'int8','NRO_PRESU':'int32','ID_ELEM':'int32','VALOR_MO':'float64',
                          'VALOR_REPUESTO':'float64','CANT_HS_PINT':'float64','VALOR_MAT_PINT':'float64',})
#MARCA-MODELO
dfModelo = pd.read_csv('./data/ClaseMarcaModelo.csv',sep=';',encoding='latin-1',decimal='.',
                       dtype={'CLASE':'int16','MARCA':'int16','MODELO':'int16','DMARCA':'object','DMODELO':'object'})
#MARCA-MODELO-NUEVO
dfModeloNuevo = pd.read_csv('./data/ClaseMarcaModeloNuevosRed.csv',sep=';',encoding='latin-1',decimal='.',
                           dtype={'CLASE':'int16','MARCA':'int16','MODELO':'int16'})
#PORTON
dfPorton = pd.read_csv('./data/dfPortonV2.csv',sep=';',encoding='utf-8',decimal='.',
                       dtype = {'COD_CLASE':'int16','COD_MARCA':'int8','COD_MODELO':'int8'})
#SEGMENTOS
dfSEGMENTO = pd.read_csv('./data/_dfSEGMENTACION_V1.csv',sep=';',encoding='utf-8',decimal='.',
                         dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16','SEG':'int8'})
#VALOR-REPUESTO
dfVALOR_REPUESTO_MO_Unif = pd.read_csv('./data/_dfVALOR_REPUESTO_ALL_V7.csv',sep=';',encoding='utf-8',decimal='.',parse_dates = ['FECHA'],
                        dtype = {'SEG':'int8','COD_CLASE':'int16','COD_MARCA':'int8','COD_MODELO':'int8', 
                                 'COD_PARTE':'int8','DESC_ELEM':'str','PRECIO_MEAN':'float64','VIEJO':'bool'})
#VALOR-MO-FRENTE
dfVALOR_MO_UNIF_FRENTE = pd.read_csv('./data/_dfVALOR_REPARA_MO&PINT_FRENTEV7.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                 'VALOR_MO_MEAN':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                 'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                 'RATIO_HS_PINT_STD':'float64','CANT_HS_PINT_STD':'float64',
                                 'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_ST':'float64',
                                 'ORIG_MAT_PINT_MEAN':'float64','ORIG_MAT_PINT_STD':'float64'})
#VALOR-MO-TRASERO
dfVALOR_MO_UNIF_TRASERO = pd.read_csv('./data/_dfVALOR_REPARA_MO&PINT_TRASEROV7.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                 'VALOR_MO_MEAN':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                 'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                 'RATIO_HS_PINT_STD':'float64','CANT_HS_PINT_STD':'float64',
                                 'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_ST':'float64',
                                 'ORIG_MAT_PINT_MEAN':'float64','ORIG_MAT_PINT_STD':'float64'})
#VALOR-MO-LATERAL
dfVALOR_MO_UNIF_LATERAL = pd.read_csv('./data/_dfVALOR_REPARA_MO&PINT_LATERALV7.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                 'VALOR_MO_MEAN':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                 'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                 'RATIO_HS_PINT_STD':'float64','CANT_HS_PINT_STD':'float64',
                                 'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_ST':'float64',
                                 'ORIG_MAT_PINT_MEAN':'float64','ORIG_MAT_PINT_STD':'float64'})
#VALRO-MO-PINT-FRENTE
dfVALOR_REPUESTO_VALOR_MAT_FRENTE = pd.read_csv('./data/_dfVALOR_REPUESTO_MO&PINT_FRENTEV7.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                 'VALOR_MO':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                 'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                 'RATIO_HS_PINT_MEAN':'float64','RATIO_HS_PINT_STD':'float64',
                                 'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_STD':'float64'})
#VALRO-MO-PINT-TRASERO
dfVALOR_REPUESTO_VALOR_MAT_TRASERO = pd.read_csv('./data/_dfVALOR_REPUESTO_MO&PINT_TRASEROV7.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                 'VALOR_MO':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                 'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                 'RATIO_HS_PINT_MEAN':'float64','RATIO_HS_PINT_STD':'float64',
                                 'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_STD':'float64'})
#VALRO-MO-PINT-LATERAL
dfVALOR_REPUESTO_VALOR_MAT_LATERAL = pd.read_csv('./data/_dfVALOR_REPUESTO_MO&PINT_LATERALV7.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'SEG':'int8','COD_CLASE':'int16','COD_PARTE':'int8','DESC_ELEM':'str',
                                 'VALOR_MO':'float64','VALOR_MO_STD':'float64','RATIO_MO_MEAN':'float64',
                                 'RATIO_MO_STD':'float64','CANT_HS_PINT_MEAN':'float64','CANT_HS_PINT_STD':'float64',
                                 'RATIO_HS_PINT_MEAN':'float64','RATIO_HS_PINT_STD':'float64',
                                 'VALOR_MAT_PINT_MEAN':'float64','VALOR_MAT_PINT_STD':'float64'})
#MOLDURAS
dfMOLDURA = pd.read_csv('./data/MolduraSedanValueMin.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                                 'COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                                 'COD_ELEM':'int64','VALOR':'float64','VIEJO':'bool'})
#ESPEJO
dfESPEJO = pd.read_csv('./data/PuertaEspejoSedanValueMin.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                                 'COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                                 'COD_ELEM':'int64','VALOR': 'float64','VIEJO':'bool'})
#FARO
dfFARO = pd.read_csv('./data/FaroOnlySedanValueMin.csv',sep=';',encoding='utf-8',decimal='.',
                     dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                              'COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                              'COD_ELEM':'int64','VALOR': 'float64','VIEJO':'bool'})
#CRISTAL
dfCRISTAL = pd.read_csv('./data/PuertaCristalSedanValueMin.csv',sep=';',encoding='utf-8',decimal='.',
                        dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                                 'COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                                 'COD_ELEM':'int64','VALOR': 'float64','VIEJO':'bool'})
#MANIJA
dfMANIJA = pd.read_csv('./data/PuertaManijaSedanValueMin.csv',sep=';',encoding='utf-8',decimal='.',
                       dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                                'COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                                'COD_ELEM':'int64','VALOR': 'float64','VIEJO':'bool'})
#MOTOS
dfMOTO = pd.read_csv('./data/motos.csv',sep=';',encoding='utf-8',na_values=['NA', '?'], on_bad_lines='warn',
                     dtype={'CLASE':int,'MARCA':int,'MODELO':int,'DMARCA':str,'DMODELO':str}) 
#DBVALUES
#engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
conn = engine.connect()
result = conn.execute(text('SELECT stname,flvalue FROM admvalue;'))
for row in result:
    if row[0] == 'Tercero': param.bfTercero = float(row[1])
    if row[0] == 'MObra': param.bfMObra = float(row[1])
    if row[0] == 'MOMinimo': param.bfMOMinimo = float(row[1])
    if row[0] == 'Pintura': param.bfPintura = float(row[1])
    if row[0] == 'Ajuste': param.bfAjuste = float(row[1])
    if row[0] == 'Asegurado': param.bfAsegurado = float(row[1])
conn.close()
engine.dispose()

app = FastAPI()
app.mount("/img", StaticFiles(directory="img"), name='img')
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return index.bfHTML

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
    #DBVALUES
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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

    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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
    
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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
    
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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

    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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

    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
    conn = engine.connect()
    result = conn.execute(text('SELECT * FROM admvaluestra;'))
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

    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
    conn = engine.connect()
    result = conn.execute(text('SELECT * FROM admvaluestraal;'))
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
        
    return search.bfHTML

@app.get("/admvalue", response_class=HTMLResponse)
async def adminValues():
    #DBVALUES
    try:
        #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
        engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
        conn = engine.connect()
        result = conn.execute(text('SELECT stname,flvalue FROM admvalue;'))
        for row in result:
            if row[0] == 'Tercero': param.bfTercero = float(row[1])
            if row[0] == 'MObra': param.bfMObra = float(row[1])
            if row[0] == 'MOMinimo': param.bfMOMinimo = float(row[1])
            if row[0] == 'Pintura': param.bfPintura = float(row[1])
            if row[0] == 'Ajuste': param.bfAjuste = float(row[1])
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
    
    bfAdminValues = admvalue.bfHTML
    bfAdminValues = bfAdminValues.replace('rplBfAsegurado',str(param.bfAsegurado))
    bfAdminValues = bfAdminValues.replace('rplBfTercero',str(param.bfTercero))
    bfAdminValues = bfAdminValues.replace('rplBfMObra',str(param.bfMObra))
    bfAdminValues = bfAdminValues.replace('rplBfMOMinimo',str(param.bfMOMinimo))
    bfAdminValues = bfAdminValues.replace('rplBfPintura',str(param.bfPintura))
    bfAdminValues = bfAdminValues.replace('rplBfAjuste',str(param.bfAjuste))
    return bfAdminValues

@app.post("/admvaluesave", response_class=PlainTextResponse)
async def adminValuesSave(ASEGURADO:str="",TERCERO:str="",MOBRA:str="",MOMINIMO:str="",PINTURA:str="",AJUSTE:str=""):
    #DBVALUES
    bfMsg = "Valores grabados satisfactoriamente" 
    try:
       #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
       engine = db.create_engine('sqlite:///appinsbudget.sqlite3');
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
    return bfMsg

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
        #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
        engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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
    
    return templates.TemplateResponse("admreplat.html", context)

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
        #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
        engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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
    
    return templates.TemplateResponse("admreplatag.html", context)

@app.post("/admvalueslat", response_class=PlainTextResponse)
async def admvalueslat(request: Request, Lat_Cristal_Delantero:str="",Lat_Cristal_Trasero:str="",\
                       Lat_Espejo_Electrico:str="",Lat_Espejo_Manual:str="",Lat_Manija_Pta_Del:str="",\
                       Lat_Manija_Pta_Tras:str="",Lat_Moldura_Pta_Del:str="",Lat_Moldura_Pta_Tras:str="",\
                       Lat_Puerta_Delantera:str="",Lat_Puerta_Trasera:str="",Lat_Zocalo:str=""):
    
    bfMsg = "Valores grabados satisfactoriamente"
    try:
       #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
       engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
       conn = engine.connect()

       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Cristal_Delantero).replace(',','.') + ' WHERE stName="Lat_Cristal_Delantero"'))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Cristal_Trasero).replace(',','.') + ' WHERE stName="Lat_Cristal_Trasero"'))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Espejo_Electrico).replace(',','.') + ' WHERE stName="Lat_Espejo_Electrico"'))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Espejo_Manual).replace(',','.') + ' WHERE stName="Lat_Espejo_Manual"'))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Manija_Pta_Del).replace(',','.') + ' WHERE stName="Lat_Manija_Pta_Del"'))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Manija_Pta_Tras).replace(',','.') + ' WHERE stName="Lat_Manija_Pta_Tras"'))       
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Moldura_Pta_Del).replace(',','.') + ' WHERE stName="Lat_Moldura_Pta_Del"'))       
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Moldura_Pta_Tras).replace(',','.') + ' WHERE stName="Lat_Moldura_Pta_Tras"'))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Puerta_Delantera).replace(',','.') + ' WHERE stName="Lat_Puerta_Delantera"'))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Puerta_Trasera).replace(',','.') + ' WHERE stName="Lat_Puerta_Trasera"'))
       result = conn.execute(text('UPDATE admvalueslat SET flValue =' + str(Lat_Zocalo).replace(',','.') + ' WHERE stName="Lat_Zocalo"'))

       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar, comuniquese con el administrador " + str(e)    
       
    return bfMsg         

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
        #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
        engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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
            
    return templates.TemplateResponse("admreptra.html", context)

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
        #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
        engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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
            
    return templates.TemplateResponse("admreptraag.html", context)

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
        #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
        engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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
    return templates.TemplateResponse("admrepdel.html", context)

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
        #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
        engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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
    return templates.TemplateResponse("admrepdelag.html", context)

@app.post("/admvaluestra", response_class=PlainTextResponse)
async def admvaluestra(Baul_Porton:str="",Faro_Ext:str="",Faro_Int:str="",Guardabarro:str="",Luneta:str="",\
                      Moldura:str="",Panel_Cola:str="",Paragolpe:str=""):
    bfMsg = "Valores grabados satisfactoriamente" 
    try:
       #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
       engine = db.create_engine('sqlite:///appinsbudget.sqlite3');
       conn = engine.connect()
       
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Baul_Porton).replace(',','.') + ' WHERE stName="Baul_Porton"'))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Faro_Ext).replace(',','.') + ' WHERE stName="Faro_Ext"'))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Faro_Int).replace(',','.') + ' WHERE stName="Faro_Int"'))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Guardabarro).replace(',','.') + ' WHERE stName="Guardabarro"'))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Luneta).replace(',','.') + ' WHERE stName="Luneta"'))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Moldura).replace(',','.') + ' WHERE stName="Moldura"'))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Panel_Cola).replace(',','.') + ' WHERE stName="Panel_Cola"'))
       result = conn.execute(text('UPDATE admvaluestra SET flValue =' + str(Paragolpe).replace(',','.') + ' WHERE stName="Paragolpe"'))
       
       if conn.in_transaction(): conn.commit()
       conn.close()
       engine.dispose()
    except Exception as e:
       bfMsg = "Se produjo un error al grabar: "+str(e)     
    
    return bfMsg

@app.get("/dbCreateLog", response_class=HTMLResponse)
async def dbCreateLog():
    bfValue = "bfHTMLdbCreateLog finalizado satisfactoriamente"
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
    conn = engine.connect()
    try:
        conn.execute(text('''CREATE TABLE  IF NOT EXISTS 'logpresupuestosV1' (
                            'id'	             INTEGER NOT NULL UNIQUE,
                            'timestamp'	         TEXT DEFAULT ' ',
                            'user'	             TEXT NOT NULL DEFAULT ' ',
                            'cliente'	         INTEGER NOT NULL,
                            'clase'	             INTEGER NOT NULL,
                            'marca'	             INTEGER NOT NULL,
                            'modelo'	         INTEGER NOT NULL,
                            'siniestro'	         TEXT DEFAULT ' ',
                            'lateralr'	         TEXT DEFAULT ' ',
                            'trasero'	         TEXT DEFAULT ' ',
                            'ltReparaPintura'	 REAL DEFAULT 0,
                            'ltReponeElemento'	 REAL DEFAULT 0,
                            'ltReponePintura'	 REAL DEFAULT 0,
                            'ltReponeManoObra'	 REAL DEFAULT 0,
                            'ltReponeEspejoEle'	 REAL DEFAULT 0,
                            'ltReponeEspejoMan'	 REAL DEFAULT 0,
                            'ltReponeManijaDel'	 REAL DEFAULT 0,
                            'ltReponeManijaTra'	 REAL DEFAULT 0,
                            'ltReponeMolduraDel' REAL DEFAULT 0,
                            'ltReponeMolduraTra' REAL DEFAULT 0,
                            'ltReponeCristalDel' REAL DEFAULT 0,
                            'ltReponeCristalTra' REAL DEFAULT 0,
                            'ltTotal'	         REAL DEFAULT 0,
                            'trReparaPintura'	 REAL DEFAULT 0,
                            'trReponeElemento'	 REAL DEFAULT 0,
                            'trReponePintura'	 REAL DEFAULT 0,
                            'trReponeManoObra'	 REAL DEFAULT 0,
                            'trReponeMoldura'	 REAL DEFAULT 0,
                            'trReponeFaroExt'	 REAL DEFAULT 0,
                            'trReponeFaroInt'	 REAL DEFAULT 0,
                            'trTotal'	         REAL DEFAULT 0,
                            'Asegurado'	         REAL DEFAULT 0,
                            'Tercero'	         REAL DEFAULT 0,
                            'MObra'	             REAL DEFAULT 0,
                            'Pintura'	         REAL DEFAULT 0,
                            'Ajuste'	         REAL DEFAULT 0,
                            PRIMARY KEY('id' AUTOINCREMENT)
                        ) '''))
        if conn.in_transaction(): conn.commit()
    except exc.SQLAlchemyError as e:
        bfValue = "dbCreateAdminValue Error: "+str(e)     
    conn.close()
    engine.dispose()
    return dbstatus.bfHTMLdbCreateLog.replace('<<value>>',bfValue)

@app.get("/dbCreateAdminValue", response_class=HTMLResponse)
async def dbcreateAdminValue():
    bfValue = "dbCreateAdminValue finalizado satisfactoriamente"
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
    conn = engine.connect()
    try:
        conn.execute(text('''CREATE TABLE IF NOT EXISTS 'admvalue' (
                              'stName'  TEXT NOT NULL UNIQUE,
                              'flValue' REAL DEFAULT 0,
                               PRIMARY KEY('stName')
                          ) '''))
        #CREATE TABLE admvalue (id SERIAL PRIMARY KEY,
        #               stname TEXT DEFAULT ' ',
        #               flvalue REAL DEFAULT 0);
        if conn.in_transaction(): conn.commit()
    except exc.SQLAlchemyError as e:
        bfValue = "dbCreateAdminValue Error: "+str(e)          
    conn.close()
    engine.dispose()
    return dbstatus.bfHTMLdbCreateAdminValue.replace('<<value>>',bfValue)

@app.get("/dbDropAdminValue", response_class=HTMLResponse)
async def dbDropAdminValue():
    bfValue = "dbDropAdminValue finalizado satisfactoriamente"
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
    conn = engine.connect()
    try:
        conn.execute(text('''DROP TABLE admvalue;'''))
        if conn.in_transaction(): conn.commit()
    except exc.SQLAlchemyError as e:
        bfValue = "dbDropAdminValue Error: "+str(e)          
    conn.close()
    engine.dispose()
    return dbstatus.bfHTMLdbCreateAdminValue.replace('<<value>>',bfValue)

@app.get("/dbInsertAdminValue", response_class=HTMLResponse)
async def dbInsertAdminValue():
    bfValue = "dbInsertAdminValue finalizado satisfactoriamente"
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
    conn = engine.connect()
    try:
        result = conn.execute(text('''INSERT INTO admvalue (stname, flvalue) VALUES ('Asegurado',1);'''))
        result = conn.execute(text('''INSERT INTO admvalue (stname, flvalue) VALUES ('Tercero',0.8);'''))
        result = conn.execute(text('''INSERT INTO admvalue (stname, flvalue) VALUES ('MObra',18250);'''))
        result = conn.execute(text('''INSERT INTO admvalue (stname, flvalue) VALUES ('MOMinimo',9250);'''))
        result = conn.execute(text('''INSERT INTO admvalue (stname, flvalue) VALUES ('Pintura',22500);'''))
        result = conn.execute(text('''INSERT INTO admvalue (stname, flvalue) VALUES ('Ajuste',1);'''))
        if conn.in_transaction(): conn.commit()
    except exc.SQLAlchemyError as e:
        bfValue = "dbInsertAdminValue Error: "+str(e)          
    conn.close()
    engine.dispose()
    return dbstatus.bfHTMLdbCreateAdminValue.replace('<<value>>',bfValue)

@app.get("/dbreadAdmin", response_class=PlainTextResponse)
async def dbreadAdmin():
    lsResult = []
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
    conn = engine.connect()
    try:
        result = conn.execute(text('''SELECT stname,flvalue FROM admvalue;'''))
    except exc.SQLAlchemyError as e:
        bfValue = "dbInsertAdminValue Error: "+str(e)       
             
    for row in result:
        lsResult.append(row)    
    conn.close()
    engine.dispose()
    
    return ";".join(str(x) for x in lsResult) 

@app.get("/dbread", response_class=HTMLResponse)
async def dbRead(request: Request):
    lsResult = []
    lsTimeStamp = []
    lsReparaTrasero = []
    lsCambiaTrasero = []
    lsReparaLateral = []
    lsCambiaLateral = []
    context = {"request": request,"result":'',"timestamp":'',
               "reparatrasero":'',"cambiatrasero":'',
               "reparalateral":'',"cambialateral":''}
    
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
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

    except exc.SQLAlchemyError as e:
        bfValue = 'dbInsertAdminValue Error: '+str(e)
    conn.close()
    engine.dispose()    
    context["result"] = lsResult
    context["restimestamp"] = lsTimeStamp    
    context["reparatrasero"] = lsReparaTrasero
    context["cambiatrasero"] = lsCambiaTrasero   
    context["reparalateral"] = lsReparaLateral
    context["cambialateral"] = lsCambiaLateral   

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
        isWrited = fnWriteLogBrief(CLIENTE,CLASE,MARCA,MODELO,SINIESTRO,PERITO,VALORPERITO,'','','')
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

    if '1' in lsFrente:
        lsFrenteCambiaElems,lsFrenteReparaElems,\
        lsFrenteFaritoElemsDel,lsFrenteFaroElemsDel,\
        lsFrenteFaro_AuxiliarElemsDel,lsFrenteParabrisasElemsDel,\
        lsFrenteParagolpe_RejillaElemsDel,lsFrenteRejilla_RadiadorElemsDel=fnGetFrentelElems(lsFrente)  
        
        #ACA SE SEIGUE
        if len(lsFrenteReparaElems)>0:        
            lsLatReparaAve=fnReparaFrente(iSEG,iCLASE,lsFrenteReparaElems)
            if len(lsLatReparaAve) == 0: lsLatReparaAve.append(0)
            flFrtValorReparaAve = np.round(sum(lsLatReparaAve),2)

        if len(lsFrenteCambiaElems)>0:    
            lsLatReponeAve=fnCambiaFrente(iSEG,iCLASE,iMARCA,iMODELO,lsFrenteCambiaElems,isAlta)
            if len(lsLatReponeAve) == 0: lsLatReponeAve.append(0)
            flFrtValorReponeElem = np.round(sum(lsLatReponeAve),2)
            
            lsLatReponePintAve,lsLatReponeMoAv=fnCambiaPinturaFrente(iSEG,iCLASE,lsFrenteCambiaElems) 
            if len(lsLatReponePintAve) == 0: lsLatReponePintAve.append(0)
            flFrtValorReponePint = np.round(sum(lsLatReponePintAve),2)
            
            if len(lsLatReponeMoAv)  == 0: lsLatReponeMoAv.append(0)        
            flFrtValorReponeMoAv = np.round(sum(lsLatReponeMoAv),2)
        
        if len(lsFrenteFaritoElemsDel)>0:      
            if isAlta: flFrtValorReponeFarito = paramal.bfFrt_GA_Del_Farito   
            else:      flFrtValorReponeFarito = param.bfFrt_GM_Del_Farito

        if len(lsFrenteFaroElemsDel)>0:        
            if isAlta: flFrtValorReponeFaro = paramal.bfFrt_GA_Del_Faro   
            else:      flFrtValorReponeFaro = param.bfFrt_GM_Del_Faro

        if len(lsFrenteFaro_AuxiliarElemsDel)>0:        
            if isAlta: flFrtValorReponeFaro_Auxiliar = paramal.bfFrt_GA_Del_Faro_Auxiliar   
            else:      flFrtValorReponeFaro_Auxiliar = param.bfFrt_GM_Del_Faro_Auxiliar

        if len(lsFrenteParabrisasElemsDel)>0:        
            if isAlta: flFrtValorReponeParabrisas = paramal.bfFrt_GA_Del_Parabrisas   
            else:      flFrtValorReponeParabrisas = param.bfFrt_GM_Del_Parabrisas

        if len(lsFrenteParagolpe_RejillaElemsDel)>0:        
            if isAlta: flFrtValorReponeParagolpe_Rejilla = paramal.bfFrt_GA_Del_Paragolpe_Rejilla  
            else:      flFrtValorReponeParagolpe_Rejilla = param.bfFrt_GM_Del_Paragolpe_Rejilla

        if len(lsFrenteRejilla_RadiadorElemsDel)>0:        
            if isAlta: flFrtValorReponeRejilla_Radiador = paramal.bfFrt_GA_Del_Rejilla_Radiador   
            else:      flFrtValorReponeRejilla_Radiador = param.bfFrt_GM_Del_Rejilla_Radiador
        
        flFrente=np.round(flFrtValorReparaAve+flFrtValorReponeElem+flFrtValorReponePint+flFrtValorReponeMoAv+\
                          flFrtValorReponeFarito+flFrtValorReponeFaro+flFrtValorReponeFaro_Auxiliar+flFrtValorReponeParabrisas+\
                          flFrtValorReponeParagolpe_Rejilla+flFrtValorReponeRejilla_Radiador,2)        
        
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
        lsValuesResult.append(0)
        lsValuesResult.append(0)

    if '1' in lsLateral:
        lsLateralCambiaElems,lsLateralReparaElems,\
        lsLateralMolduraElemsDel,lsLateralMolduraElemsTra,\
        lsLateralEspejoElecElems,lsLateralEspejoManElems,\
        lsLateralManijaElemsDel,lsLateralManijaElemsTra,\
        lsLateralCristalElemDel,lsLateralCristalElemTra =fnGetLateralElems(lsLateral)

        if len(lsLateralReparaElems)>0:
            lsLatReparaAve=fnReparaLateral(iSEG,iCLASE,lsLateralReparaElems)
            if len(lsLatReparaAve) == 0: lsLatReparaAve.append(0)
            flLatValorReparaAve = np.round(sum(lsLatReparaAve),2)

        if len(lsLateralCambiaElems)>0:
            lsLatReponeAve=fnCambiaLateral(iSEG,iCLASE,iMARCA,iMODELO,lsLateralCambiaElems,isAlta)
            if len(lsLatReponeAve) == 0: lsLatReponeAve.append(0)
            flLatValorReponeElem = np.round(sum(lsLatReponeAve),2)

            lsLatReponePintAve,lsLatReponeMoAv=fnCambiaPinturaLateral(iSEG,iCLASE,lsLateralCambiaElems) 
            if len(lsLatReponePintAve) == 0: lsLatReponePintAve.append(0)
            flLatValorReponePint = np.round(sum(lsLatReponePintAve),2)
            if len(lsLatReponeMoAv)  == 0: lsLatReponeMoAv.append(0)        
            flLatValorReponeMoAv = np.round(sum(lsLatReponeMoAv),2)

        if len(lsLateralMolduraElemsDel)>0:
            lsLatMeanMod = fnMolduraLateralDel(iMARCA,iMODELO,isAlta)
            if len(lsLatMeanMod) == 0: lsLatMeanMod.append(0)   
            flLatValorReponeMolduraDel = np.round(lsLatMeanMod[0],2)
            if len(lsLateralMolduraElemsDel)== 2: flLatValorReponeMolduraDel*=2

        if len(lsLateralMolduraElemsTra)>0:
            lsLatMeanMod = fnMolduraLateralTra(iMARCA,iMODELO,isAlta)
            if len(lsLatMeanMod) == 0: lsLatMeanMod.append(0) 
            flLatValorReponeMolduraTra = np.round(lsLatMeanMod[0],2) 
            if len(lsLateralMolduraElemsTra)== 2: flLatValorReponeMolduraTra*=2
        
        if len(lsLateralEspejoElecElems)>0:
            lsLatMeanEsp = fnEspejoLateralElec(iMARCA,iMODELO,isAlta)
            if len(lsLatMeanEsp) == 0: lsLatMeanEsp.append(0)    
            flLatValorReponeEspejoElec = np.round(lsLatMeanEsp[0],2)
            if len(lsLateralEspejoElecElems) >1: flLatValorReponeEspejoElec*=2

        if len(lsLateralEspejoManElems)>0:
            lsLatMeanEsp = fnEspejoLateralMan(iMARCA,iMODELO,isAlta)
            if len(lsLatMeanEsp) == 0: lsLatMeanEsp.append(0)    
            flLatValorReponeEspejoMan = np.round(lsLatMeanEsp[0],2)
            if len(lsLateralEspejoManElems) >1: flLatValorReponeEspejoMan*=2

        if len(lsLateralManijaElemsDel)>0:
            lsLatMeanManDel = fnManijaLateralDel(iMARCA,iMODELO,isAlta)
            if len(lsLatMeanManDel) == 0: lsLatMeanManDel.append(0)    
            flLatValorReponeManDel = np.round(lsLatMeanManDel[0],2)
            if len(lsLateralManijaElemsDel) >1: flLatValorReponeManDel*=2

        if len(lsLateralManijaElemsTra)>0:
            lsLatMeanManTra = fnManijaLateralTra(iMARCA,iMODELO,isAlta)
            if len(lsLatMeanManTra) == 0: lsLatMeanManTra.append(0)    
            flLatValorReponeManTra = np.round(lsLatMeanManTra[0],2)
            if len(lsLateralManijaElemsTra) >1: flLatValorReponeManTra*=2

        if len(lsLateralCristalElemDel)>0:
            lsLatMeanCriDel = fnCristalLateralDel(iMARCA,iMODELO,isAlta)
            if len(lsLatMeanCriDel) == 0: lsLatMeanCriDel.append(0)    
            flLatValorReponeCriDel = np.round(lsLatMeanCriDel[0],2)
            if len(lsLateralCristalElemDel) >1: flLatValorReponeCriDel*=2

        if len(lsLateralCristalElemTra)>0:
            lsLatMeanCriTra = fnCristalLateralTra(iMARCA,iMODELO,isAlta)
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
            
            lsTraReponePintAve,lsTraReponeMoAv=fnCambiaPinturaTrasero(iSEG,iCLASE,lsTraseroCambiaElems)                                                                 
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
            lsTraMeanMold=fnMolduraTrasero(iMARCA,iMODELO,isAlta)      
            if len(lsTraMeanMold) == 0: lsTraMeanMold.append(0)
            flTraValorReponeMoldura  = np.round(lsTraMeanMold[-1],2)

        if len(lsTraseroFaroExtElems)>0:
            lsTraMeanFExt=fnFaroExtTrasero(iMARCA,iMODELO,isAlta)    
            if len(lsTraMeanFExt) == 0: lsTraMeanFExt.append(0)
            flTraValorReponeFaroExt  = np.round(lsTraMeanFExt[-1],2)
            if len(lsTraseroFaroExtElems) >1: flTraValorReponeFaroExt*=2 

        if len(lsTraseroFaroIntElems)>0:
            lsTraMeanFInt=fnFaroIntTrasero(iMARCA,iMODELO,isAlta)    
            if len(lsTraMeanFInt) == 0: lsTraMeanFInt.append(0)
            flTraValorReponeFaroInt  = np.round(lsTraMeanFInt[-1],2)
            if len(lsTraseroFaroIntElems) >1: flTraValorReponeFaroInt*=2
    
        flTrasero=np.round(flTraValorReparaAve+flTraValorReponeElem+flTraValorReponePint+\
                           flTraValorReponeMoAv+flTraValorReponeMoldura+\
                           flTraValorReponeFaroExt+flTraValorReponeFaroInt,2)

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
    
    #ToDo: Seguir codigo
    if len(lsFrenteCambiaElems) + len(lsFrenteReparaElems) +\
       len(lsLateralCambiaElems) + len(lsLateralReparaElems) +\
       len(lsTraseroCambiaElems) + len(lsTraseroReparaElems) == 1:
        # Agregar en lsValuesResult   
        if flFrente  != 0: flFrente =  flFrente  + param.bfMObra
        if flLateral != 0: flLateral = flLateral + param.bfMObra            
        if flTrasero != 0: flTrasero = flTrasero + param.bfMObra

    bfTmp = resumeDataBrief(CLIENTE,flFrente,flLateral,flTrasero)
    #Todo: Agregar el Log Frente
    isWrited = fnWriteLog(CLIENTE,CLASE,MARCA,MODELO,SINIESTRO,PERITO,VALORPERITO,LATERAL,TRASERO,lsValuesResult)
    
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
    lsSEG = dfSEGMENTO.loc[(dfSEGMENTO['COD_CLASE'] == inCOD_CLASE) & (dfSEGMENTO['COD_MARCA'] == inCOD_MARCA) & 
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

def fnIsOld(inCOD_MARCA,inCOD_MODELO,dfData):
    blOld = False
    dfOld = dfData.loc[(dfData['COD_MARCA'] == inCOD_MARCA) & (dfData['COD_MODELO'] == inCOD_MODELO)]['VIEJO']
  
    if len(dfOld) == 0: 
        blOld = False
    else:
        blOld = dfData.loc[(dfData['COD_MARCA'] == inCOD_MARCA) & (dfData['COD_MODELO'] == inCOD_MODELO)]['VIEJO'].iloc[0]
    
    if blOld!=True and blOld!=False: blOld = False
    
    return blOld

def fnReparaTrasero(inSEG,inCOD_CLASE,lsRepara):
    inCOD_PARTE = 2
    lsReparaAve = []
    flAverage = 0
   
    for index, item in enumerate(lsRepara):
        bfID_ELEM = dfVALOR_MO_UNIF_TRASERO.loc[(dfVALOR_MO_UNIF_TRASERO['SEG'] == inSEG) & 
                                                (dfVALOR_MO_UNIF_TRASERO['COD_CLASE'] == inCOD_CLASE) & 
                                                (dfVALOR_MO_UNIF_TRASERO['COD_PARTE'] == inCOD_PARTE) &
                        (dfVALOR_MO_UNIF_TRASERO['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                [['VALOR_MO_MEAN','CANT_HS_PINT_MEAN','VALOR_MAT_PINT_MEAN']] 

        flVALOR_MO_MEAN     = bfID_ELEM['VALOR_MO_MEAN']
        flCANT_HS_PINT_MEAN = bfID_ELEM['CANT_HS_PINT_MEAN'] 

        flVALOR_MO_MEAN     = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2)       #Todo: Sacar
        flCANT_HS_PINT_MEAN = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfPintura),2) #Todo: Sacar

        flAverage=np.round((flVALOR_MO_MEAN + flCANT_HS_PINT_MEAN + bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        lsReparaAve.append(flAverage) 
    
    for index, item in enumerate(lsReparaAve): lsReparaAve[index] = list(set(item))[0]     

    return lsReparaAve

def fnCambiaTrasero(inSEG,inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,lsRepone,isAlta):
    inCOD_PARTE = 2
    lsReponeAve = []
    flAverage = 0
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfVALOR_REPUESTO_MO_Unif)
      
    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['SEG'] == inSEG)        & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_CLASE']    == inCOD_CLASE)  & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_MARCA']    == inCOD_MARCA)  &
                                        (dfVALOR_REPUESTO_MO_Unif['COD_MODELO']   == inCOD_MODELO) &
                                        (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']    == inCOD_PARTE)  &
                                        (dfVALOR_REPUESTO_MO_Unif['VIEJO']        == isOld)        & 
                    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))][['PRECIO_MEAN']] 
        
        flAverage = np.round(bfID_ELEM['PRECIO_MEAN'],2)

        if len(flAverage) == 0:
            bfID_ELEM = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['SEG'] == inSEG)        & 
                                            (dfVALOR_REPUESTO_MO_Unif['COD_CLASE']    == inCOD_CLASE)  & 
                                            (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']    == inCOD_PARTE)  &
                                            (dfVALOR_REPUESTO_MO_Unif['VIEJO']        == isOld)        &
                    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))][['PRECIO_MEAN']] 
            
            flMean = np.round(bfID_ELEM['PRECIO_MEAN'].mean(),2)   
            flAverage = pd.Series([flMean])
            
            #Alta Gama
            if pd.isna(flAverage.iloc[0]):
                if isAlta:
                    if item=="BAULPORTON"     :flAverage.iloc[0]=paramal.bfBaul_Porton
                    elif item=="FAROEXT"      :flAverage.iloc[0]=paramal.bfFaro_Ext
                    elif item=="FAROINT"      :flAverage.iloc[0]=paramal.bfFaro_Int
                    elif item=="LUNETA"       :flAverage.iloc[0]=paramal.bfLuneta
                    elif item=="MOLDURA"      :flAverage.iloc[0]=paramal.bfMoldura
                    elif item=="PANELCOLACOMP":flAverage.iloc[0]=paramal.bfPanel_Cola
                    elif item=="PANELCOLASUP" :flAverage.iloc[0]=paramal.bfPanel_Sup
                    elif item=="PARAGOLPE"    :flAverage.iloc[0]=paramal.bfParagolpe
                    else: flAverage.iloc[0] = 0
                else:    
                    if item=="BAULPORTON"     :flAverage.iloc[0]=param.bfBaul_Porton
                    elif item=="FAROEXT"      :flAverage.iloc[0]=param.bfFaro_Ext
                    elif item=="FAROINT"      :flAverage.iloc[0]=param.bfFaro_Int
                    elif item=="LUNETA"       :flAverage.iloc[0]=param.bfLuneta
                    elif item=="MOLDURA"      :flAverage.iloc[0]=param.bfMoldura
                    elif item=="PANELCOLACOMP":flAverage.iloc[0]=param.bfPanel_Cola
                    elif item=="PANELCOLASUP" :flAverage.iloc[0]=param.bfPanel_Sup
                    elif item=="PARAGOLPE"    :flAverage.iloc[0]=param.bfParagolpe
                    else: flAverage.iloc[0] = 0
        
        if len(flAverage) == 0: flAverage = [0]

        lsReponeAve.append(flAverage)
    
    for index, item in enumerate(lsReponeAve): lsReponeAve[index] = list(set(item))[0]     
    
    return lsReponeAve 

def fnCambiaPinturaTrasero(inSEG,inCOD_CLASE,lsRepone):
    inCOD_PARTE = 2
    lsReponePintAve=[]
    lsReponeMoAv=[]
    flAverage=0
    flMoAv=0
    
    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_VALOR_MAT_TRASERO.loc[(dfVALOR_REPUESTO_VALOR_MAT_TRASERO['SEG']==inSEG)& 
                    (dfVALOR_REPUESTO_VALOR_MAT_TRASERO['COD_CLASE']==inCOD_CLASE)&
                    (dfVALOR_REPUESTO_VALOR_MAT_TRASERO['COD_PARTE']==inCOD_PARTE)&
                    (dfVALOR_REPUESTO_VALOR_MAT_TRASERO['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                        [['VALOR_MO_MEAN','CANT_HS_PINT_MEAN','VALOR_MAT_PINT_MEAN']] 

        flVALOR_MO_MEAN     = bfID_ELEM['VALOR_MO_MEAN']
        flCANT_HS_PINT_MEAN = bfID_ELEM['CANT_HS_PINT_MEAN'] 

        flVALOR_MO_MEAN     = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2)  #Todo: Sacar
        flCANT_HS_PINT_MEAN = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfPintura),2) #Todo: Sacar

        flAverage = np.round((flCANT_HS_PINT_MEAN + bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        flMoAv    = np.round(flVALOR_MO_MEAN,2) 
        
        if len(flAverage)==0:flAverage=[0]
        if len(flMoAv)==0:flMoAv=[0]
                                  
        lsReponePintAve.append(flAverage) 
        lsReponeMoAv.append(flMoAv) 

    for index, item in enumerate(lsReponePintAve): lsReponePintAve[index]=list(set(item))[0]     
    for index, item in enumerate(lsReponeMoAv)   : lsReponeMoAv[index]=list(set(item))[0]      
    
    return lsReponePintAve,lsReponeMoAv 

def fnMolduraTrasero(inCOD_MARCA,inCOD_MODELO,isAlta):    
    inCOD_PARTE = 2
    moldCtro = ['PARAGOLPE EMBELLEC / MOLD']
    lsVersion = ['1','2','3'] 
    lsMoldCtro = []
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfMOLDURA)

    dfMOLD_CTRO = dfMOLDURA.loc[(dfMOLDURA['COD_MARCA']  == inCOD_MARCA)  & 
                                (dfMOLDURA['COD_MODELO'] == inCOD_MODELO) &
                                (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                (dfMOLDURA['VIEJO']      == isOld)        & 
                                (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, moldCtro))))]\
                                .sort_values(['VALOR'], ascending=[False])
    if len(dfMOLD_CTRO)==0:
        dfMOLD_CTRO = dfMOLDURA.loc[(dfMOLDURA['COD_MARCA'] == inCOD_MARCA) & 
                                    (dfMOLDURA['COD_PARTE'] == inCOD_PARTE) &
                                    (dfMOLDURA['VIEJO']      == isOld)      & 
                                    (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, moldCtro))))]\
                                    .sort_values(['VALOR'], ascending=[False])

    dfTmp = dfMOLD_CTRO.loc[~dfMOLD_CTRO['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]
        
    if len(dfTmp)!=0: 
        flValue = dfTmp['VALOR'].mean() + param.bfMOMinimo
        lsMoldCtro.append(round(flValue,2))
    else:
        if isAlta: flValue = paramal.bfMoldura + param.bfMOMinimo
        else:      flValue = param.bfMoldura   + param.bfMOMinimo
        lsMoldCtro.append(round(flValue,2))   

    return lsMoldCtro

def fnFaroExtTrasero(inCOD_MARCA,inCOD_MODELO,isAlta):    
    inCOD_PARTE = 2
    faroDer = ['FARO DER']
    lsVersion = ['1','2','3','4','5','6'] 
    lsFaroExt = []
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfFARO)
    
    dfFARO_EXT = dfFARO.loc[(dfFARO['COD_MARCA']  == inCOD_MARCA)  & 
                            (dfFARO['COD_MODELO'] == inCOD_MODELO) &
                            (dfFARO['COD_PARTE']  == inCOD_PARTE)  &
                            (dfFARO['VIEJO']      == isOld)        &
                            (dfFARO['DESC_ELEM'].str.contains('|'.join(map(re.escape, faroDer))))]\
                            .sort_values(['VALOR'], ascending=[False])
    if len(dfFARO_EXT)==0:
            dfFARO_EXT = dfFARO.loc[(dfFARO['COD_MARCA'] == inCOD_MARCA) & 
                                    (dfFARO['COD_PARTE'] == inCOD_PARTE) &
                                    (dfFARO['VIEJO']      == isOld)      &
                                    (dfFARO['DESC_ELEM'].str.contains('|'.join(map(re.escape, faroDer))))]\
                                    .sort_values(['VALOR'], ascending=[False])

    dfTmp = dfFARO_EXT.loc[~dfFARO_EXT['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]
    
    if len(dfTmp)!=0: 
        flValue = dfTmp['VALOR'].mean() + param.bfMOMinimo
        lsFaroExt.append(round(flValue,2))
    else:
        if isAlta: flValue = paramal.bfFaro_Ext + param.bfMOMinimo
        else:      flValue = param.bfFaro_Ext   + param.bfMOMinimo
        lsFaroExt.append(round(flValue,2))
    return lsFaroExt

def fnFaroIntTrasero(inCOD_MARCA,inCOD_MODELO,isAlta):    
    inCOD_PARTE = 2
    faroDer = ['FARO DER 1']
    lsFaroInt = []
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfFARO)
    
    dfFARO_INT = dfFARO.loc[(dfFARO['COD_MARCA']  == inCOD_MARCA)  & 
                            (dfFARO['COD_MODELO'] == inCOD_MODELO) &
                            (dfFARO['COD_PARTE']  == inCOD_PARTE)  &
                            (dfFARO['VIEJO']      == isOld)        &
                            (dfFARO['DESC_ELEM'].str.contains('|'.join(map(re.escape, faroDer))))]\
                            .sort_values(['VALOR'], ascending=[False])
    if len(dfFARO_INT)==0:
            dfFARO_INT = dfFARO.loc[(dfFARO['COD_MARCA'] == inCOD_MARCA) & 
                                    (dfFARO['COD_PARTE'] == inCOD_PARTE) &
                                    (dfFARO['VIEJO']     == isOld)       &
                                    (dfFARO['DESC_ELEM'].str.contains('|'.join(map(re.escape, faroDer))))]\
                                    .sort_values(['VALOR'], ascending=[False])
    
    if len(dfFARO_INT)!=0: 
        flValue = dfFARO_INT['VALOR'].mean() + param.bfMOMinimo
        lsFaroInt.append(round(flValue,2))
    else:
        if isAlta: flValue = paramal.bfFaro_Int + param.bfMOMinimo
        else:      flValue = param.bfFaro_Int + param.bfMOMinimo
        lsFaroInt.append(round(flValue,2))   
    
    return lsFaroInt
#FRENTE#
def fnReparaFrente(inSEG,inCOD_CLASE,lsRepara):
    inCOD_PARTE = 1
    lsReparaAve = []
    flAverage = 0
    for index, item in enumerate(lsRepara):
        bfID_ELEM = dfVALOR_MO_UNIF_FRENTE.loc[(dfVALOR_MO_UNIF_FRENTE['SEG']==inSEG)&
                                               (dfVALOR_MO_UNIF_FRENTE['COD_CLASE']==inCOD_CLASE)& 
                                               (dfVALOR_MO_UNIF_FRENTE['COD_PARTE']==inCOD_PARTE)&
                                (dfVALOR_MO_UNIF_FRENTE['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                        [['VALOR_MO_MEAN','CANT_HS_PINT_MEAN','VALOR_MAT_PINT_MEAN']] 
                                                                      
        flVALOR_MO_MEAN      = bfID_ELEM['VALOR_MO_MEAN']
        flCANT_HS_PINT_MEAN  = bfID_ELEM['CANT_HS_PINT_MEAN'] 

        flVALOR_MO_MEAN       = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2) #Todo: sacar 6350
        flCANT_HS_PINT_MEAN   = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfMObra),2) #Todo: sacar 6350
        
        flAverage = np.round((flVALOR_MO_MEAN + flCANT_HS_PINT_MEAN + bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        lsReparaAve.append(flAverage) 
        
    for index, item in enumerate(lsReparaAve): 
        lsReparaAve[index]=list(set(item))[0]     
    
    return lsReparaAve           

def fnCambiaFrente(inSEG,inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,lsRepone,isAlta):
    inCOD_PARTE = 1
    lsReponeAve = []
    flAverage = 0
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfVALOR_REPUESTO_MO_Unif)

    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['SEG'] == inSEG)        & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_CLASE']    == inCOD_CLASE)  & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_MARCA']    == inCOD_MARCA)  & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_MODELO']   == inCOD_MODELO) &          
                                        (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']    == inCOD_PARTE)  &
                                        (dfVALOR_REPUESTO_MO_Unif['VIEJO']        == isOld)        & 
                    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))][['PRECIO_MEAN']] 

        flAverage = np.round(bfID_ELEM['PRECIO_MEAN'],2)
        
        if len(flAverage) == 0:
            bfID_ELEM = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['SEG'] == inSEG)        & 
                                            (dfVALOR_REPUESTO_MO_Unif['COD_CLASE']    == inCOD_CLASE)  & 
                                            (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']    == inCOD_PARTE)  &
                                            (dfVALOR_REPUESTO_MO_Unif['VIEJO']        == isOld)        &
                    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))][['PRECIO_MEAN']] 
            
            flMean = np.round(bfID_ELEM['PRECIO_MEAN'].mean(),2)   
            flAverage = pd.Series([flMean])

            if pd.isna(flAverage.iloc[0]):
                if isAlta:
                    if item  =="CAPOT"          :flAverage.iloc[0]=paramal.bfFrt_GA_Del_Capot
                    elif item=="FRENTE"         :flAverage.iloc[0]=paramal.bfFrt_GA_Del_Frente
                    elif item=="GUARDABARRO"    :flAverage.iloc[0]=paramal.bfFrt_GA_Del_Guardabarro
                    elif item=="PARAGOLPE_ALMA" :flAverage.iloc[0]=paramal.bfFrt_GA_Del_Paragolpe_Alma
                    elif item=="PARAGOLPE_CTRO" :flAverage.iloc[0]=paramal.bfFrt_GA_Del_Paragolpe_Ctro
                    else: flAverage.iloc[0] = 0
                else:    
                    if item  =="CAPOT"          :flAverage.iloc[0]=param.bfFrt_GM_Del_Capot
                    elif item=="FRENTE"         :flAverage.iloc[0]=param.bfFrt_GM_Del_Frente
                    elif item=="GUARDABARRO"    :flAverage.iloc[0]=param.bfFrt_GM_Del_Guardabarro
                    elif item=="PARAGOLPE_ALMA" :flAverage.iloc[0]=param.bfFrt_GM_Del_Paragolpe_Alma
                    elif item=="PARAGOLPE_CTRO" :flAverage.iloc[0]=param.bfFrt_GM_Del_Paragolpe_Ctro
                    else: flAverage.iloc[0] = 0
        
        if len(flAverage) == 0: flAverage = [0]

        lsReponeAve.append(flAverage)
        
    for index, item in enumerate(lsReponeAve): 
        lsReponeAve[index] = list(set(item))[0]     
    
    return lsReponeAve

def fnCambiaPinturaFrente(inSEG,inCOD_CLASE,lsRepone):
    inCOD_PARTE = 1
    lsReponePintAve = []
    lsReponeMoAv    = []
    
    flAverage = 0
    flMoAv    = 0
    
    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_VALOR_MAT_FRENTE.loc[(dfVALOR_REPUESTO_VALOR_MAT_FRENTE['SEG']==inSEG) & 
                                             (dfVALOR_REPUESTO_VALOR_MAT_FRENTE['COD_CLASE']==inCOD_CLASE) & 
                                             (dfVALOR_REPUESTO_VALOR_MAT_FRENTE['COD_PARTE']==inCOD_PARTE) &
                        (dfVALOR_REPUESTO_VALOR_MAT_FRENTE['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                             [['VALOR_MO_MEAN','CANT_HS_PINT_MEAN','VALOR_MAT_PINT_MEAN']] 
        
        flVALOR_MO_MEAN = bfID_ELEM['VALOR_MO_MEAN']
        flVALOR_MO_MEAN = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2) #Todo: Para simplificar y no procesar todo
        
        flCANT_HS_PINT_MEAN = bfID_ELEM['CANT_HS_PINT_MEAN']
        flCANT_HS_PINT_MEAN = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfPintura),2) #Todo: Para simplificar y no procesar todo

        flAverage = np.round((flCANT_HS_PINT_MEAN+bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        
        flMoAv  = np.round(flVALOR_MO_MEAN,2) 

        if len(flAverage) == 0: flAverage = [0]
        lsReponePintAve.append(flAverage) 
        if len(flMoAv) == 0: flMoAv = [0]
        lsReponeMoAv.append(flMoAv) 
        
    for index, item in enumerate(lsReponePintAve): lsReponePintAve[index] = list(set(item))[0]     
    
    for index, item in enumerate(lsReponeMoAv): lsReponeMoAv[index] = list(set(item))[0]      

    return lsReponePintAve,lsReponeMoAv

#LATERAL#
def fnEspejoLateralElec(inCOD_MARCA,inCOD_MODELO,isAlta):
    espElec = ['ESPEJO ELECTRICO']
    lsVersion = ['1','2','3','4','5'] 
    lsMeanEsp = []
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfESPEJO)
    
    dfESPEJO_ELEC = dfESPEJO.loc[(dfESPEJO['COD_MARCA'] == inCOD_MARCA)   & 
                                 (dfESPEJO['COD_MODELO'] == inCOD_MODELO) &
                                 (dfESPEJO['VIEJO']     == isOld)         &
                                 (dfESPEJO['DESC_ELEM'].str.contains('|'.join(map(re.escape, espElec))))]\
                                 .sort_values(['VALOR'], ascending=[False])
        
    if len(dfESPEJO_ELEC)==0:
        dfESPEJO_ELEC = dfESPEJO.loc[(dfESPEJO['COD_MARCA'] == inCOD_MARCA) & 
                                     (dfESPEJO['VIEJO']     == isOld)       &
                                     (dfESPEJO['DESC_ELEM'].str.contains('|'.join(map(re.escape, espElec))))]\
                                     .sort_values(['VALOR'], ascending=[False])
    
    dfTmp = dfESPEJO_ELEC.loc[~dfESPEJO_ELEC['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]
    
    if len(dfTmp)!=0: 
        flValue = dfTmp['VALOR'].mean() + param.bfMOMinimo
        lsMeanEsp.append(round(flValue,2))   
    else:
        if isAlta: flValue = paramal.bfLat_Espejo_Electrico + param.bfMOMinimo
        else:      flValue = param.bfLat_Espejo_Electrico   + param.bfMOMinimo
        lsMeanEsp.append(round(flValue,2))   
    
    return lsMeanEsp 

def fnEspejoLateralMan(inCOD_MARCA,inCOD_MODELO,isAlta):
    espMan = ['ESPEJO MANUAL']
    lsVersion = ['1','2','3','4','5'] 
    lsMeanEsp = []
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfESPEJO)
    
    dfESPEJO_MAN = dfESPEJO.loc[(dfESPEJO['COD_MARCA'] == inCOD_MARCA)   & 
                                (dfESPEJO['COD_MODELO'] == inCOD_MODELO) &
                                (dfESPEJO['VIEJO']     == isOld)         &
                                (dfESPEJO['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMan))))]\
                                .sort_values(['VALOR'], ascending=[False])
        
    if len(dfESPEJO_MAN)==0:
        dfESPEJO_MAN = dfESPEJO.loc[(dfESPEJO['COD_MARCA'] == inCOD_MARCA) & 
                                    (dfESPEJO['VIEJO']     == isOld)       &
                                    (dfESPEJO['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMan))))]\
                                    .sort_values(['VALOR'], ascending=[False])
    
    dfTmp = dfESPEJO_MAN.loc[~dfESPEJO_MAN['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]
    
    if len(dfTmp)!=0: 
        flValue = dfTmp['VALOR'].mean() + param.bfMOMinimo
        lsMeanEsp.append(round(flValue,2))   
    else:
        if isAlta: flValue = paramal.bfLat_Espejo_Manual + param.bfMOMinimo
        else:      flValue = param.bfLat_Espejo_Manual + param.bfMOMinimo
        lsMeanEsp.append(round(flValue,2))   
    
    return lsMeanEsp 

def fnManijaLateralDel(inCOD_MARCA,inCOD_MODELO,isAlta):
    lsManija = ['DEL MANIJA']
    lsVersion = ['1','2','3','4','5'] 
    lsMeanMan = []
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfMANIJA)
    
    dfMANIJA_RST  = dfMANIJA.loc[(dfMANIJA['COD_MARCA'] == inCOD_MARCA)   & 
                                 (dfMANIJA['COD_MODELO'] == inCOD_MODELO) &
                                 (dfMANIJA['VIEJO']     == isOld)         &
                                 (dfMANIJA['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsManija))))]\
                                 .sort_values(['VALOR'], ascending=[False])
        
    if len(dfMANIJA_RST)==0:
        dfMANIJA_RST = dfMANIJA.loc[(dfMANIJA['COD_MARCA'] == inCOD_MARCA) & 
                                    (dfMANIJA['VIEJO']     == isOld)       &
                                    (dfMANIJA['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsManija))))]\
                                    .sort_values(['VALOR'], ascending=[False])
   
    dfTmp = dfMANIJA_RST.loc[~dfMANIJA_RST['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]
    
    if len(dfTmp)!=0: 
        flValue = dfTmp['VALOR'].mean() + param.bfMOMinimo
        lsMeanMan.append(round(flValue,2))   
    else:
        if isAlta: flValue = paramal.bfLat_Manija_Pta_Del + param.bfMOMinimo
        else:      flValue = param.bfLat_Manija_Pta_Del   + param.bfMOMinimo
        lsMeanMan.append(round(flValue,2))   

    return lsMeanMan 

def fnManijaLateralTra(inCOD_MARCA,inCOD_MODELO,isAlta):
    lsManija = ['TRAS MANIJA']
    lsVersion = ['1','2','3','4','5'] 
    lsMeanMan = []
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfMANIJA)
    
    dfMANIJA_RST  = dfMANIJA.loc[(dfMANIJA['COD_MARCA']  == inCOD_MARCA)  & 
                                 (dfMANIJA['COD_MODELO'] == inCOD_MODELO) &
                                 (dfMANIJA['VIEJO']      == isOld)        &
                                 (dfMANIJA['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsManija))))]\
                                 .sort_values(['VALOR'], ascending=[False])
        
    if len(dfMANIJA_RST)==0:
        dfMANIJA_RST = dfMANIJA.loc[(dfMANIJA['COD_MARCA'] == inCOD_MARCA) & 
                                    (dfMANIJA['VIEJO']      == isOld)      &
                                    (dfMANIJA['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsManija))))]\
                                    .sort_values(['VALOR'], ascending=[False])
   
    dfTmp = dfMANIJA_RST.loc[~dfMANIJA_RST['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]
    
    if len(dfTmp)!=0: 
        flValue = dfTmp['VALOR'].mean() + param.bfMOMinimo
        lsMeanMan.append(round(flValue,2))   
    else:
        if isAlta: flValue = paramal.bfLat_Manija_Pta_Tras + param.bfMOMinimo
        else:      flValue = param.bfLat_Manija_Pta_Tras   + param.bfMOMinimo
        lsMeanMan.append(round(flValue,2))   

    return lsMeanMan 

def fnMolduraLateralDel(inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    espMold = ['DEL MOLD']
    lsMeanMold = []
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfMOLDURA)
    
    dfMOLD_LATERAL = dfMOLDURA.loc[(dfMOLDURA['COD_MARCA']  == inCOD_MARCA)  & 
                                   (dfMOLDURA['COD_MODELO'] == inCOD_MODELO) &
                                   (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                   (dfMOLDURA['VIEJO']      == isOld)        &
                                   (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                   .sort_values(['VALOR'], ascending=[False])
    
    if len(dfMOLD_LATERAL)==0:
            dfMOLD_LATERAL = dfMOLDURA.loc[(dfMOLDURA['COD_MARCA'] == inCOD_MARCA)   & 
                                           (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                           (dfMOLDURA['VIEJO']      == isOld)        &
                                           (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                           .sort_values(['VALOR'], ascending=[False])

    if len(dfMOLD_LATERAL)!=0: 
        flValue = dfMOLD_LATERAL['VALOR'].mean() + param.bfMOMinimo
        lsMeanMold.append(round(flValue,2))   
    else:
        if isAlta: flValue = paramal.bfLat_Moldura_Pta_Del + param.bfMOMinimo
        else:      flValue = param.bfLat_Moldura_Pta_Del   + param.bfMOMinimo
        lsMeanMold.append(round(flValue,2))   
        
    return lsMeanMold

def fnMolduraLateralTra(inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    espMold = ['TRAS MOLD']
    lsMeanMold = []
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfMOLDURA)
    
    dfMOLD_LATERAL = dfMOLDURA.loc[(dfMOLDURA['COD_MARCA']  == inCOD_MARCA)  & 
                                   (dfMOLDURA['COD_MODELO'] == inCOD_MODELO) &
                                   (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                   (dfMOLDURA['VIEJO']      == isOld)        &
                                   (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                   .sort_values(['VALOR'], ascending=[False])
    
    if len(dfMOLD_LATERAL)==0:
            dfMOLD_LATERAL = dfMOLDURA.loc[(dfMOLDURA['COD_MARCA'] == inCOD_MARCA)   & 
                                           (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                           (dfMOLDURA['VIEJO']      == isOld)        &
                                           (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                           .sort_values(['VALOR'], ascending=[False])
                                           
    if len(dfMOLD_LATERAL)!=0: 
        flValue = dfMOLD_LATERAL['VALOR'].mean() + param.bfMOMinimo
        lsMeanMold.append(round(flValue,2)) 
    else:
        if isAlta: flValue = paramal.bfLat_Moldura_Pta_Tras + param.bfMOMinimo
        else:      flValue = param.bfLat_Moldura_Pta_Tras + param.bfMOMinimo
        lsMeanMold.append(round(flValue,2))   
    
    return lsMeanMold

def fnCristalLateralDel(inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    espMold = ['DEL CRISTAL']
    lsMeanMold = []
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfCRISTAL)
    
    dfMOLD_LATERAL = dfCRISTAL.loc[(dfCRISTAL['COD_MARCA']  == inCOD_MARCA)  & 
                                   (dfCRISTAL['COD_MODELO'] == inCOD_MODELO) &
                                   (dfCRISTAL['COD_PARTE']  == inCOD_PARTE)  &
                                   (dfCRISTAL['VIEJO']      == isOld)        &
                                   (dfCRISTAL['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                   .sort_values(['VALOR'], ascending=[False])
    
    if len(dfMOLD_LATERAL)==0:
            dfMOLD_LATERAL = dfCRISTAL.loc[(dfCRISTAL['COD_MARCA'] == inCOD_MARCA)   & 
                                           (dfCRISTAL['COD_PARTE']  == inCOD_PARTE)  &
                                           (dfCRISTAL['VIEJO']      == isOld)        &
                                           (dfCRISTAL['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                           .sort_values(['VALOR'], ascending=[False])

    if len(dfMOLD_LATERAL)!=0: 
        flValue = dfMOLD_LATERAL['VALOR'].mean() + param.bfMOMinimo
        lsMeanMold.append(round(flValue,2))   
    else:
        if isAlta: flValue = paramal.bfLat_Cristal_Delantero + param.bfMOMinimo
        else:      flValue = param.bfLat_Cristal_Delantero + param.bfMOMinimo
        lsMeanMold.append(round(flValue,2))   
        
    return lsMeanMold

def fnCristalLateralTra(inCOD_MARCA,inCOD_MODELO,isAlta):
    inCOD_PARTE = 3
    espMold = ['TRAS CRISTAL']
    lsMeanMold = []
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfCRISTAL)
    
    dfMOLD_LATERAL = dfCRISTAL.loc[(dfCRISTAL['COD_MARCA']  == inCOD_MARCA)  & 
                                   (dfCRISTAL['COD_MODELO'] == inCOD_MODELO) &
                                   (dfCRISTAL['COD_PARTE']  == inCOD_PARTE)  &
                                   (dfCRISTAL['VIEJO']      == isOld)        &
                                   (dfCRISTAL['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                   .sort_values(['VALOR'], ascending=[False])
    
    if len(dfMOLD_LATERAL)==0:
            dfMOLD_LATERAL = dfCRISTAL.loc[(dfCRISTAL['COD_MARCA'] == inCOD_MARCA)   & 
                                           (dfCRISTAL['COD_PARTE']  == inCOD_PARTE)  &
                                           (dfCRISTAL['VIEJO']      == isOld)        &
                                           (dfCRISTAL['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                           .sort_values(['VALOR'], ascending=[False])
                                           
    if len(dfMOLD_LATERAL)!=0: 
        flValue = dfMOLD_LATERAL['VALOR'].mean() + param.bfMOMinimo
        lsMeanMold.append(round(flValue,2)) 
    else:
        if isAlta: flValue = paramal.bfLat_Cristal_Trasero + param.bfMOMinimo
        else:      flValue = param.bfLat_Cristal_Trasero + param.bfMOMinimo
        lsMeanMold.append(round(flValue,2))   
        
    return lsMeanMold
 
def fnReparaLateral(inSEG,inCOD_CLASE,lsRepara):
    inCOD_PARTE = 3
    lsReparaAve = []
    flAverage = 0
    for index, item in enumerate(lsRepara):
        bfID_ELEM = dfVALOR_MO_UNIF_LATERAL.loc[(dfVALOR_MO_UNIF_LATERAL['SEG']==inSEG)&
                                                (dfVALOR_MO_UNIF_LATERAL['COD_CLASE']==inCOD_CLASE)& 
                                                (dfVALOR_MO_UNIF_LATERAL['COD_PARTE']==inCOD_PARTE)&
                                (dfVALOR_MO_UNIF_LATERAL['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                        [['VALOR_MO_MEAN','CANT_HS_PINT_MEAN','VALOR_MAT_PINT_MEAN']] 
                                                                      
        flVALOR_MO_MEAN      = bfID_ELEM['VALOR_MO_MEAN']
        flCANT_HS_PINT_MEAN  = bfID_ELEM['CANT_HS_PINT_MEAN'] 

        flVALOR_MO_MEAN       = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2) #Todo: sacar 6350
        flCANT_HS_PINT_MEAN   = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfMObra),2) #Todo: sacar 6350
        
        flAverage = np.round((flVALOR_MO_MEAN + flCANT_HS_PINT_MEAN + bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        lsReparaAve.append(flAverage) 
        
    for index, item in enumerate(lsReparaAve): lsReparaAve[index]=list(set(item))[0]     
    
    return lsReparaAve           

def fnCambiaLateral(inSEG,inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,lsRepone,isAlta):
    inCOD_PARTE = 3
    lsReponeAve = []
    flAverage = 0
    
    isOld = fnIsOld(inCOD_MARCA,inCOD_MODELO,dfVALOR_REPUESTO_MO_Unif)

    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['SEG'] == inSEG)        & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_CLASE']    == inCOD_CLASE)  & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_MARCA']    == inCOD_MARCA)  & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_MODELO']   == inCOD_MODELO) &          
                                        (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']    == inCOD_PARTE)  &
                                        (dfVALOR_REPUESTO_MO_Unif['VIEJO']        == isOld)        & 
                    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))][['PRECIO_MEAN']] 

        flAverage = np.round(bfID_ELEM['PRECIO_MEAN'],2)
        
        if len(flAverage) == 0:
            bfID_ELEM = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['SEG'] == inSEG)        & 
                                            (dfVALOR_REPUESTO_MO_Unif['COD_CLASE']    == inCOD_CLASE)  & 
                                            (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']    == inCOD_PARTE)  &
                                            (dfVALOR_REPUESTO_MO_Unif['VIEJO']        == isOld)        &
                    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))][['PRECIO_MEAN']] 
            
            flMean = np.round(bfID_ELEM['PRECIO_MEAN'].mean(),2)   
            flAverage = pd.Series([flMean])

            if pd.isna(flAverage.iloc[0]):
                if isAlta:
                    if item=="CRISTAL_DEL"       :flAverage.iloc[0]=paramal.bfLat_Cristal_Delantero
                    elif item=="CRISTAL_TRA"     :flAverage.iloc[0]=paramal.bfLat_Cristal_Trasero
                    elif item=="ESPEJOELEC"      :flAverage.iloc[0]=paramal.bfLat_Espejo_Electrico
                    elif item=="ESPEJOMAN"       :flAverage.iloc[0]=paramal.bfLat_Espejo_Manual
                    elif item=="MANIJA_DEL"      :flAverage.iloc[0]=paramal.bfLat_Manija_Pta_Del
                    elif item=="MANIJA_TRA"      :flAverage.iloc[0]=paramal.bfLat_Manija_Pta_Tras
                    elif item=="MOLDURA_DEL"     :flAverage.iloc[0]=paramal.bfLat_Moldura_Pta_Del
                    elif item=="MOLDURA_TRA"     :flAverage.iloc[0]=paramal.bfLat_Moldura_Pta_Tras
                    elif item=="PUERTA_DEL"      :flAverage.iloc[0]=paramal.bfLat_Puerta_Delantera
                    elif item=="PUERTA_TRA"      :flAverage.iloc[0]=paramal.bfLat_Puerta_Trasera
                    elif item=="PUERTA_DEL_PANEL":flAverage.iloc[0]=paramal.bfLat_Puerta_Panel_Del
                    elif item=="PUERTA_TRA_PANEL":flAverage.iloc[0]=paramal.bfLat_Puerta_Panel_Tras
                    elif item=="ZOCALO"          :flAverage.iloc[0]=paramal.bfLat_Zocalo
                    else: flAverage.iloc[0] = 0
                else:
                    if item=="CRISTAL_DEL"       :flAverage.iloc[0]=param.bfLat_Cristal_Delantero
                    elif item=="CRISTAL_TRA"     :flAverage.iloc[0]=param.bfLat_Cristal_Trasero
                    elif item=="ESPEJOELEC"      :flAverage.iloc[0]=param.bfLat_Espejo_Electrico
                    elif item=="ESPEJOMAN"       :flAverage.iloc[0]=param.bfLat_Espejo_Manual
                    elif item=="MANIJA_DEL"      :flAverage.iloc[0]=param.bfLat_Manija_Pta_Del
                    elif item=="MANIJA_TRA"      :flAverage.iloc[0]=param.bfLat_Manija_Pta_Tras
                    elif item=="MOLDURA_DEL"     :flAverage.iloc[0]=param.bfLat_Moldura_Pta_Del
                    elif item=="MOLDURA_TRA"     :flAverage.iloc[0]=param.bfLat_Moldura_Pta_Tras
                    elif item=="PUERTA_DEL"      :flAverage.iloc[0]=param.bfLat_Puerta_Delantera
                    elif item=="PUERTA_TRA"      :flAverage.iloc[0]=param.bfLat_Puerta_Trasera
                    elif item=="PUERTA_DEL_PANEL":flAverage.iloc[0]=param.bfLat_Puerta_Panel_Del
                    elif item=="PUERTA_TRA_PANEL":flAverage.iloc[0]=param.bfLat_Puerta_Panel_Tras
                    elif item=="ZOCALO"          :flAverage.iloc[0]=param.bfLat_Zocalo
        
        if len(flAverage) == 0: flAverage = [0]

        lsReponeAve.append(flAverage)
        
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
        flVALOR_MO_MEAN = np.round((flVALOR_MO_MEAN / 6350) * float(param.bfMObra),2) #Todo: Para simplificar y no procesar todo
        
        flCANT_HS_PINT_MEAN = bfID_ELEM['CANT_HS_PINT_MEAN']
        flCANT_HS_PINT_MEAN = np.round((flCANT_HS_PINT_MEAN / 6350) * float(param.bfPintura),2) #Todo: Para simplificar y no procesar todo

        flAverage = np.round((flCANT_HS_PINT_MEAN+bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        
        flMoAv  = np.round(flVALOR_MO_MEAN,2) 

        if len(flAverage) == 0: flAverage = [0]
        lsReponePintAve.append(flAverage) 
        if len(flMoAv) == 0: flMoAv = [0]
        lsReponeMoAv.append(flMoAv) 
        
    for index, item in enumerate(lsReponePintAve): lsReponePintAve[index] = list(set(item))[0]     
    
    for index, item in enumerate(lsReponeMoAv): lsReponeMoAv[index] = list(set(item))[0]      

    return lsReponePintAve,lsReponeMoAv

##################################################
def resumeDataBrief(intCLIENTE,fltFrente,fltLateral,fltTrasero):
    intClientType = 2
    if intCLIENTE.isnumeric(): intClientType = int(intCLIENTE)
    
    ftSum = (fltFrente + fltLateral + fltTrasero) * float(param.bfAjuste)
    
    if intClientType == 1: ftSum *= float(param.bfAsegurado)
    else                 : ftSum *= float(param.bfTercero)
    
    txtValorTotal = "<span id=\"CostBrief\" class=\"pure-form-message-inline\" style=\"text-align:left;font-family:'helvetica neue';font-size:100%;color:rgb(170,27,23);\">Sugerido&nbsp$&nbsp{0:0.2f}".format(ftSum)+"</span>"
    return txtValorTotal

def getMarcaDesc(bfCLASE,bfMARCA):
    bfTmp = ''
    idf = dfModelo.loc[(dfModelo['CLASE']==bfCLASE)  & (dfModelo['MARCA']==bfMARCA)]
    bfTmp = idf.iloc[0]['DMARCA'] 
    return bfTmp

def getModeloDesc(bfCLASE,bfMARCA,bfMODELO):    
    bfTmp = ''
    idf = dfModelo.loc[(dfModelo['CLASE']==bfCLASE) & (dfModelo['MARCA']==bfMARCA) & (dfModelo['MODELO']==bfMODELO)]
    bfTmp = idf.iloc[0]['DMODELO']  
    return bfTmp


def fnWriteLog(CLIENTE,CLASE,MARCA,MODELO,SINIESTRO,PERITO,VALORPERITO,LATERAL,TRASERO,lsValuesResultWrite):
    bfWrite =True
    ts = datetime.datetime.now().timestamp()
  
    bfValues = str(ts)+","+str(CLIENTE)+","+str(CLASE)+","+str(MARCA)+","+str(MODELO)+",'"+SINIESTRO+"','"+PERITO.replace(',','')+"','"+VALORPERITO+"','"+LATERAL+"','"+TRASERO+"',"
    
    bfValues += str(lsValuesResultWrite[0])+","+str(lsValuesResultWrite[1])+","+str(lsValuesResultWrite[2])+","+str(lsValuesResultWrite[3])+","\
            +str(lsValuesResultWrite[4])+","+str(lsValuesResultWrite[5])+","+str(lsValuesResultWrite[6])+","+str(lsValuesResultWrite[7])+","\
            +str(lsValuesResultWrite[8])+","+str(lsValuesResultWrite[9])+","+str(lsValuesResultWrite[10])+","+str(lsValuesResultWrite[11])+","\
            +str(lsValuesResultWrite[12])+","+str(lsValuesResultWrite[13])+","+str(lsValuesResultWrite[14])+","+str(lsValuesResultWrite[15])+","\
            +str(lsValuesResultWrite[16])+","+str(lsValuesResultWrite[17])+","+str(lsValuesResultWrite[18])+","+str(lsValuesResultWrite[19])+","+str(lsValuesResultWrite[20])+","
    bfValues += str(param.bfAsegurado)+","+str(param.bfTercero)+","+str(param.bfMObra)+","+str(param.bfPintura)+","+str(param.bfAjuste)

    bfClause = '''INSERT INTO logpresupuestosV1 (timestamp,cliente,clase,marca,modelo,siniestro,Perito,ValorPerito,lateralr,trasero,
                                                 ltReparaPintura,ltReponeElemento,ltReponePintura,ltReponeManoObra,
                                                 ltReponeEspejoEle,ltReponeEspejoMan,ltReponeManijaDel,ltReponeManijaTra,
                                                 ltReponeMolduraDel,ltReponeMolduraTra,ltReponeCristalDel,ltReponeCristalTra,
                                                 ltTotal,trReparaPintura,trReponeElemento,trReponePintura,trReponeManoObra,
                                                 trReponeMoldura,trReponeFaroExt,trReponeFaroInt,trTotal,Asegurado,
                                                 Tercero,MObra,Pintura,Ajuste) VALUES (''' + bfValues + ');'
    #try:
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
    conn = engine.connect()
    result = conn.execute(text(bfClause))
    if conn.in_transaction(): conn.commit()
    conn.close()
    engine.dispose()
    #except Exception as e:
    #    bfWrite =False
    return bfWrite

def fnWriteLogBrief(CLIENTE,CLASE,MARCA,MODELO,SINIESTRO,PERITO,VALORPERITO,LATERAL,TRASERO,lsValuesResultWrite):
    bfWrite =True
    ts = datetime.datetime.now().timestamp()
  
    bfValues = str(ts)+","+str(CLIENTE)+","+str(CLASE)+","+str(MARCA)+","+str(MODELO)+",'"+SINIESTRO+"','"+PERITO.replace(',','')+"','"+VALORPERITO+"'"
    print(bfValues)
    bfClause = '''INSERT INTO logpresupuestosV1 (timestamp,cliente,clase,marca,modelo,siniestro,Perito,ValorPerito) VALUES (''' + bfValues + ');'
    #try:
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
    conn = engine.connect()
    result = conn.execute(text(bfClause))
    if conn.in_transaction(): conn.commit()
    conn.close()
    engine.dispose()
    #except Exception as e:
    #    bfWrite =False
    return bfWrite

def fnAltaGama(CLASE,MARCA,MODELO):
    bAltaGama = False
    #engine = db.create_engine('postgresql://appinsbudgetuser:oGcfNsvSvdQsdmZGK6PnfsTGASpEg2da@dpg-cq3b65qju9rs739bbnb0-a/appinsbudgetdb')
    engine = db.create_engine('sqlite:///appinsbudget.sqlite3')
    conn = engine.connect()
    result = conn.execute(text("SELECT al FROM marcamodelo where clase=" + str(CLASE) + " and marca=" + str(MARCA) + " and modelo=" + str(MODELO) +";"))
    for row in result: 
        if row[0] == 1: bAltaGama = True
    conn.close()
    engine.dispose()
    return bAltaGama