from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

import warnings
warnings.filterwarnings("ignore")
import math
import re
import pandas as pd
import numpy as np
np.set_printoptions(suppress=True)

import param
import search
import marca
import index

df = pd.read_csv('./data/dfBaseCleanSumV1.csv',sep=';',encoding='utf-8',decimal='.',
                 dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16',
                          'COD_PARTE':'int8','NRO_PRESU':'int32','ID_ELEM':'int32','VALOR_MO':'float64',
                          'VALOR_REPUESTO':'float64','CANT_HS_PINT':'float64','VALOR_MAT_PINT':'float64',})
#MARCA-MODELO
dfModelo = pd.read_csv('./data/ClaseMarcaModelo.csv',sep=';',encoding='latin-1',decimal='.',
                       dtype={'CLASE':'int16','MARCA':'int16','MODELO':'int16','DMARCA':'object','DMODELO':'object'})
#PORTON
dfPorton = pd.read_csv('./data/dfPortonV2.csv',sep=';',encoding='utf-8',decimal='.',
                       dtype = {'COD_CLASE':'int16','COD_MARCA':'int8','COD_MODELO':'int8'})
#SEGMENTOS
dfSEGMENTO = pd.read_csv('./data/_dfSEGMENTACION_V1.csv',sep=';',encoding='utf-8',decimal='.',
                         dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','COD_MODELO':'int16','SEG':'int8'})
#VALOR-REPUESTO
dfVALOR_REPUESTO_MO_Unif = pd.read_csv('./data/_dfVALOR_REPUESTO_ALL_V7.csv',sep=';',encoding='utf-8',decimal='.',parse_dates = ['FECHA'],
                        dtype = {'SEG':'int8','COD_CLASE':'int16','COD_MARCA':'int8','COD_MODELO':'int8', 
                                 'COD_PARTE':'int8','COD_TAREA':'int8','DESC_ELEM':'str','ELEM_MOD':'int64',
                                 'TOTAL_ELEM':'int64','PRECIO_MEAN':'float64','PRECIO_STD':'float64'})
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
dfMOLDURA = pd.read_csv('./data/_dfVALOR_REPUESTO_MOLDURAS_V7.csv',sep=';',encoding='utf-8',decimal='.',parse_dates=['FECHA'],
                        dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','DESC_MARC':'str','COD_MODELO':'int16',
                                 'DESC_MODE':'str','COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                                 'COD_ELEM':'int64','NRO_PIEZA':'str','VALOR':'float64'})
#ESPEJO
dfESPEJO = pd.read_csv('./data/_dfVALOR_REPUESTO_ESPEJOS_V7.csv',sep=';',encoding='utf-8',decimal='.',parse_dates=['FECHA'],
                        dtype = {'COD_CLASE':'int16','COD_MARCA':'int16','DESC_MARC':'str','COD_MODELO':'int16',
                                 'DESC_MODE':'str','COD_PARTE':'int8','ID_ELEM':'int64','DESC_ELEM':'str',
                                 'COD_ELEM':'int64','NRO_PIEZA':'str','VALOR': 'float64'})
app = FastAPI()
app.mount("/img", StaticFiles(directory="img"), name='img')

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return index.bfHTML

@app.post("/vh", response_class=PlainTextResponse)
async def modelo(CLASE  : int = 0):
    bfVH = ''
    if CLASE == 901:   bfVH = marca.bfMarca901
    elif CLASE == 907: bfVH = marca.bfMarca907
    return bfVH

@app.post("/modelo", response_class=PlainTextResponse)
async def modelo(CLASE:int=901, MARCA:int=0):
    bfOptions = '<option id=0></option>'
    dfModeloSearch = dfModelo.loc[(dfModelo['CLASE']==CLASE) & (dfModelo['MARCA']==MARCA)]
    dfModeloSearch = dfModeloSearch.sort_values(['MODELO'], ascending=[False])
    for index, row in dfModeloSearch.iterrows():
        bfOptions += "<option id=" + str(row['MODELO']) + ">" + str(row['DMODELO']) + "</option>" 
    return bfOptions

@app.get("/consulta", response_class=HTMLResponse)
async def consulta():
    return search.bfHTML

@app.post("/searchV1", response_class=PlainTextResponse)
async def searchV1(CLIENTE:str="",CLASE:str="",MARCA:str="",MODELO:str="",SINIESTRO:str="",LATERAL:str="",TRASERO:str=""):
    bfTmp = CLIENTE+";"+CLASE+";"+MARCA+";"+MODELO+";"+SINIESTRO+";"+LATERAL+";"+TRASERO+";";
    return bfTmp

@app.post("/search", response_class=PlainTextResponse)
async def search_Data(CLIENTE:str="",CLASE:str="",MARCA:str="",MODELO:str="",SINIESTRO:str="",LATERAL:str="",TRASERO:str=""):
    #Segmenta Input
    lsLateral = LATERAL.split('-')
    lsTrasero = TRASERO.split('-')
    #Lateral
    lsLateralCambiaElems = []
    lsLateralReparaElems = []
    lsLateralMolduraElems= []
    lsLateralEspejoElems= []
    flLatValorReparaAve=0
    flLatValorReponeElem=0
    flLatValorReponePint=0
    flLatValorReponeMoAv=0
    flLatValorReponeEspejo=0 
    flLatValorReponeMoldura=0 
    #Trasero
    lsTraseroCambiaElems = []
    lsTraseroReparaElems = []
    lsTraseroMolduraElems= []
    flTraValorReparaAve=0
    flTraValorReponeElem=0
    flTraValorReponePint=0
    flTraValorReponeMoAv=0
    flTraValorReponeMoldura=0
    #ToDo: Agregar si no es numerico mensaje de error    
    if CLASE.isdigit(): iCLASE = int(CLASE)
    if MARCA.isdigit(): iMARCA = int(MARCA)
    if MODELO.isdigit():iMODELO= int(MODELO)
    #Deteccion de Segmento 
    iSEG = fnSegmento(iCLASE,iMARCA,iMODELO)
    #Output
    flLateral=0
    flTrasero=0

    if '1' in lsLateral:
        lsLateralCambiaElems,lsLateralReparaElems,lsLateralMolduraElems,lsLateralEspejoElems=fnGetLateralElems(lsLateral)
        
        if len(lsLateralReparaElems)>0:
            
            lsLatReparaAve,lsLatReparaMin,lsLatReparaMax = fnReparaLateral(iSEG,iCLASE,lsLateralReparaElems)
            
            if len(lsLatReparaAve) == 0: lsLatReparaAve.append(0)
            flLatValorReparaAve = np.round(sum(lsLatReparaAve),2)
            
            if len(lsLatReparaMin) == 0: lsLatReparaMin.append(0)  
            flLatValorReparaMin = np.round(sum(lsLatReparaMin),2)
              
            if len(lsLatReparaMax) == 0: lsLatReparaMax.append(0)   
            flLatValorReparaMax = np.round(sum(lsLatReparaMax),2)
            
        if len(lsLateralCambiaElems)>0:
            
            lsLatReponeAve,lsLatReponeMin,lsLatReponeMax=fnCambiaLateral(iSEG,iCLASE,iMARCA,iMODELO,lsLateralCambiaElems)
            
            if len(lsLatReponeAve) == 0: lsLatReponeAve.append(0)
            flLatValorReponeElem = np.round(sum(lsLatReponeAve),2)
            
            if len(lsLatReponeMin) == 0: lsLatReponeMin.append(0) 
            flLatValorReponeElemMin = np.round(sum(lsLatReponeMin),2)
               
            if len(lsLatReponeMax) == 0: lsLatReponeMax.append(0) 
            flLatValorReponeElemMax = np.round(sum(lsLatReponeMax),2)
            
            lsLatReponePintAve,lsLatReponePintMin,lsLatReponePintMax,lsLatReponeMoAv,lsLatReponeMoMin,lsLatReponeMoMax=\
                                                               fnCambiaPinturaLateral(iSEG,iCLASE,lsLateralCambiaElems) 

            if len(lsLatReponePintAve) == 0: lsLatReponePintAve.append(0)
            flLatValorReponePint = np.round(sum(lsLatReponePintAve),2)
            
            if len(lsLatReponePintMin) == 0: lsLatReponePintMin.append(0)
            flLatValorReponePintMin = np.round(sum(lsLatReponePintMin),2)
                
            if len(lsLatReponePintMax) == 0: lsLatReponePintMax.append(0)
            flLatValorReponePintMax = np.round(sum(lsLatReponePintMax),2)           
    
            if len(lsLatReponeMoAv)  == 0: lsLatReponeMoAv.append(0)        
            flLatValorReponeMoAv = np.round(sum(lsLatReponeMoAv),2)
                 
            if len(lsLatReponeMoMin) == 0: lsLatReponeMoMin.append(0)
            flLatValorReponeMoMin   = np.round(sum(lsLatReponeMoMin),2)
              
            if len(lsLatReponeMoMax) == 0: lsLatReponeMoMax.append(0)
            flLatValorReponeMoMax   = np.round(sum(lsLatReponeMoMax),2)

        if len(lsLateralMolduraElems)>0:
            flLatValorReponeMoldura = fnMolduraLateral(iMARCA,iMODELO)
            if len(lsLateralEspejoElems)>1: flLatValorReponeMoldura*=2
        
        if len(lsLateralEspejoElems)>0:
            lsLatMeanEsp = fnEspejoLateral(iMARCA,iMODELO)
            
            if len(lsLatMeanEsp) == 0: lsLatMeanEsp.append(0)    
            flLatValorReponeEspejo = np.round(lsLatMeanEsp[0],2)
            if len(lsLateralEspejoElems) >1: flLatValorReponeEspejo*=2

        #print("_Lateral Valores Promedio_______________")
        #print(f"Repara y Pintura = {flLatValorReparaAve}")
        #print(f"Repone Elem      = {flLatValorReponeElem}")
        #print(f"Repone Pint      = {flLatValorReponePint}")
        #print(f"Repone MO        = {flLatValorReponeMoAv}")
        #print(f"Repone Espejo    = {flLatValorReponeEspejo}")
        #print(f"Repone Moldura   = {flLatValorReponeMoldura}")
        flLateral=np.round(flLatValorReparaAve+flLatValorReponeElem+flLatValorReponePint+flLatValorReponeMoAv+flLatValorReponeEspejo+flLatValorReponeMoldura,2)
        #print(f"Total            = {flLateral}")
     
    if '1' in lsTrasero:
        lsTraseroCambiaElems,lsTraseroReparaElems,lsTraseroMolduraElems = fnGetTraseroElems(CLASE,MARCA,MODELO,lsTrasero)
        
        if len(lsTraseroReparaElems)>0:
            lsTraReparaAve,lsTraReparaMin,lsTraReparaMax=fnReparaTrasero(iSEG,iCLASE,lsTraseroReparaElems)
            
            if len(lsTraReparaAve) == 0: lsTraReparaAve.append(0)
            flTraValorReparaAve = np.round(sum(lsTraReparaAve),2)
            
            if len(lsTraReparaMin) == 0: lsTraReparaMin.append(0)    
            flTraValorReparaMin = np.round(sum(lsTraReparaMin),2)
            
            if len(lsTraReparaMax) == 0: lsTraReparaMax.append(0)     
            flTraValorReparaMax = np.round(sum(lsTraReparaMax),2)
            
        if len(lsTraseroCambiaElems)>0:
            lsTraReponeAve,lsTraReponeMin,lsTraReponeMax=fnCambiaTrasero(iSEG,iCLASE,iMARCA,iMODELO,lsTraseroCambiaElems)    

            if len(lsTraReponeAve)  == 0: lsTraReponeAve.append(0)
            flTraValorReponeElem = np.round(sum(lsTraReponeAve),2)
            
            if len(lsTraReponeMin)  == 0: lsTraReponeMin.append(0)    
            flTraValorReponeElemMin = np.round(sum(lsTraReponeMin),2)
            
            if len(lsTraReponeMax)  == 0: lsTraReponeMax.append(0) 
            flTraValorReponeElemMax = np.round(sum(lsTraReponeMax),2)
 
            lsTraReponePintAve,lsTraReponePintMin,lsTraReponePintMax,lsTraReponeMoAv,lsTraReponeMoMin,lsTraReponeMoMax=\
                                                                fnCambiaPinturaTrasero(iSEG,iCLASE,lsTraseroCambiaElems) 

            if len(lsTraReponePintAve) == 0: lsTraReponePintAve.append(0)
            flTraValorReponePint = np.round(sum(lsTraReponePintAve),2) 
            
            if len(lsTraReponePintMin) == 0: lsTraReponePintMin.append(0)    
            flTraValorReponePintMin = np.round(sum(lsTraReponePintMin),2)
            
            if len(lsTraReponePintMax) == 0: lsTraReponePintMax.append(0)       
            flTraValorReponePintMax = np.round(sum(lsTraReponePintMax),2)
    
            if len(lsTraReponeMoAv)  == 0: lsTraReponeMoAv.append(0)             
            flTraValorReponeMoAv = np.round(sum(lsTraReponeMoAv),2)
            
            if len(lsTraReponeMoMin) == 0: lsTraReponeMoMin.append(0)  
            flTraValorReponeMoMin   = np.round(sum(lsTraReponeMoMin),2)
            
            if len(lsTraReponeMoMax) == 0: lsTraReponeMoMax.append(0)     
            flTraValorReponeMoMax   = np.round(sum(lsTraReponeMoMax),2)
            
        if len(lsTraseroMolduraElems)>0:
            lsTraMeanMold=fnMolduraTrasero(iMARCA,iMODELO)      

            if len(lsTraMeanMold) == 0: lsTraMeanMold.append(0)
            flTraValorReponeMoldura  = np.round(lsTraMeanMold[-1],2)

        #print("_Trasero Valores Promedio_______________")
        #print(f"Repara y Pintura = {flTraValorReparaAve}")
        #print(f"Repone Elem    = {flTraValorReponeElem}")
        #print(f"Repone Pint    = {flTraValorReponePint}")
        #print(f"Repone MO      = {flTraValorReponeMoAv}")
        #print(f"Repone Moldura = {flTraValorReponeMoldura}")
        flTrasero=np.round(flTraValorReparaAve+flTraValorReponeElem+flTraValorReponePint+flTraValorReponeMoAv+flTraValorReponeMoldura,2)
        #print(f"Total          = {flTrasero}")

    bfTmp = resumeDataBrief(CLIENTE,flLateral,flTrasero)

    return bfTmp

###########################################################
def decimal(obj):
    is_point = False
    decimals = []
    for get_float in str(obj):
        if is_point:
            decimals.append(get_float)
        if get_float == ".":
            is_point = True
    return len(decimals)

def fnSegmento(inCOD_CLASE,inCOD_MARCA,inCOD_MODELO):
    lsSEG = dfSEGMENTO.loc[(dfSEGMENTO['COD_CLASE'] == inCOD_CLASE) & (dfSEGMENTO['COD_MARCA'] == inCOD_MARCA) & 
                           (dfSEGMENTO['COD_MODELO'] == inCOD_MODELO)]['SEG'].to_numpy() 
    if len(lsSEG)==0: return 0
    else: return lsSEG[0]
    
def fnGetLateralElems(lsLateralLc):
    lsLateralElemsLc = ["CRISTAL_DEL","CRISTAL_TRA","ESPEJO","MOLDURA","PUERTA_DEL","PUERTA_TRA","PUERTA_DEL_PANEL","PUERTA_TRA_PANEL","ZOCALO"]
    #Array lsLateralElemsLc
    iPosCRISTAL_DEL=0
    iPosCRISTAL_TRA=1
    iPosESPEJO=2
    iPosMOLDURA=3
    iPosPUERTA_DEL=4
    iPosPUERTA_TRA=5
    iPosPUERTA_DEL_PANEL=6
    iPosPUERTA_TRA_PANEL=7
    iPosZOCALO=8
    
    lsLateralCambiaVal  = []
    lsLateralReparaVal  = []
    lsLateralMolduraVal = []
    lsLateralEspejoVal  = []

    #Array lsLateralLc
    iPosCRISTAL_DELCambiaDer=0
    iPosCRISTAL_DELCambiaIzq=1
    iPosCRISTAL_TRACambiaDer=2
    iPosCRISTAL_TRACambiaIzq=3
    iPosESPEJOCambiaDer=4
    iPosESPEJOCambiaIzq=5
    iPosMOLDURACambiaDer=6
    iPosMOLDURACambiaIzq=7
    iPosPUERTA_DELCambiaDer=8
    iPosPUERTA_DELCambiaIzq=9
    iPosPUERTA_TRACambiaDer=10
    iPosPUERTA_TRACambiaIzq=11
    iPosPUERTA_DEL_PANELReparaDer=12
    iPosPUERTA_DEL_PANELReparaIzq=13
    iPosPUERTA_TRA_PANELReparaDer=14
    iPosPUERTA_TRA_PANELReparaIzq=15
    iPosZOCALOCambiaDer=16
    iPosZOCALOReparaDer=17
    iPosZOCALOCambiaIzq=18
    iPosZOCALOReparaIzq=19
    
    lsLateralCambiaVal.append(lsLateralElemsLc[iPosCRISTAL_DEL] if lsLateralLc[iPosCRISTAL_DELCambiaDer]=="1" else "")
    lsLateralCambiaVal.append(lsLateralElemsLc[iPosCRISTAL_DEL] if lsLateralLc[iPosCRISTAL_DELCambiaIzq]=="1" else "")
    lsLateralCambiaVal.append(lsLateralElemsLc[iPosCRISTAL_TRA] if lsLateralLc[iPosCRISTAL_TRACambiaDer]=="1" else "")
    lsLateralCambiaVal.append(lsLateralElemsLc[iPosCRISTAL_TRA] if lsLateralLc[iPosCRISTAL_TRACambiaIzq]=="1" else "")
    lsLateralEspejoVal.append(lsLateralElemsLc[iPosESPEJO] if lsLateralLc[iPosESPEJOCambiaDer]== "1"else "")
    lsLateralEspejoVal.append(lsLateralElemsLc[iPosESPEJO] if lsLateralLc[iPosESPEJOCambiaIzq]== "1"else "")
    lsLateralMolduraVal.append(lsLateralElemsLc[iPosMOLDURA] if lsLateralLc[iPosMOLDURACambiaDer]== "1"else "")
    lsLateralMolduraVal.append(lsLateralElemsLc[iPosMOLDURA] if lsLateralLc[iPosMOLDURACambiaIzq]== "1"else "")
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
    
    lsLateralCambiaVal = [i for i in lsLateralCambiaVal if i != ""]
    lsLateralReparaVal = [i for i in lsLateralReparaVal if i != ""]
    lsLateralMolduraVal = [i for i in lsLateralMolduraVal if i != ""]
    lsLateralEspejoVal = [i for i in lsLateralEspejoVal if i != ""]
    
    return lsLateralCambiaVal,lsLateralReparaVal,lsLateralMolduraVal,lsLateralEspejoVal 

def fnGetTraseroElems(iClaseLc, iMarcaLc, iModeloLc, lsTraseroLc):    
    lsTraseroElemsLc = ['BAULPORTON','FARO','GUARDABARRO','LUNETA','MOLDURA','PANELCOLACOMP','PARAGOLPE','PANELCOLASUP']
    #Array lsTraseroElemsLc
    iPosBAULPORTON=0
    iPosFARO=1
    iPosGUARDABARRO=2
    iPosLUNETA=3
    iPosMOLDURA=4
    iPosPANELCOLACOMP=5
    iPosPARAGOLPE=6
    iPosPANELCOLASUP=7
       
    lsTraseroCambiaVal  = []
    lsTraseroReparaVal  = []
    lsTraseroMolduraVal = []
    
    #Array lsTraseroLc
    iPosBAULPORTONCambiaDer=0
    iPosFAROCambiaDer=1
    iPosFAROCambiaIzq=2
    iPosGUARDABARROCambiaDer=3
    iPosGUARDABARROReparaDer=4
    iPosGUARDABARROCambiaIzq=5
    iPosGUARDABARROReparaIzq=6
    iPosLUNETACambiaDer=7
    iPosMOLDURACambiaDer=8
    iPosPANELCOLACOMPCambiaDer=9
    iPosPANELCOLACOMPReparaDer=10
    iPosPARAGOLPECambiaDer=11
    iPosPARAGOLPEReparaDer=12
    
    lsTraseroCambiaVal.append(lsTraseroElemsLc[iPosBAULPORTON] if lsTraseroLc[iPosBAULPORTONCambiaDer] == "1" else "")
    lsTraseroCambiaVal.append(lsTraseroElemsLc[iPosFARO] if lsTraseroLc[iPosFAROCambiaDer] == "1" else "")
    lsTraseroCambiaVal.append(lsTraseroElemsLc[iPosFARO] if lsTraseroLc[iPosFAROCambiaIzq] == "1" else "")
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
    
    lsTraseroCambiaVal = [i for i in lsTraseroCambiaVal if i != ""]
    lsTraseroReparaVal = [i for i in lsTraseroReparaVal if i != ""]
    lsTraseroMolduraVal = [i for i in lsTraseroMolduraVal if i != ""]
     
    return lsTraseroCambiaVal,lsTraseroReparaVal,lsTraseroMolduraVal 
    
def fnHasPorton(iClaseLc, iMarcaLc, iModeloLc):
    blPorton = False
    if len(dfPorton.loc[(dfPorton['COD_CLASE']==int(iClaseLc))&(dfPorton['COD_MARCA']==int(iMarcaLc))&(dfPorton['COD_MODELO']==int(iModeloLc))])!=0:
        blPorton = True
    return blPorton    

def fnReparaTrasero(inSEG,inCOD_CLASE,lsRepara):
    inCOD_PARTE  =   2
    lsReparaAve = []
    lsReparaMin = []
    lsReparaMax = []
    flAverage = 0
    flMin     = 0
    flMax     = 0
        
    for index, item in enumerate(lsRepara):
        bfID_ELEM = dfVALOR_MO_UNIF_TRASERO.loc[(dfVALOR_MO_UNIF_TRASERO['SEG'] == inSEG) & 
                    (dfVALOR_MO_UNIF_TRASERO['COD_CLASE'] == inCOD_CLASE) & (dfVALOR_MO_UNIF_TRASERO['COD_PARTE'] == inCOD_PARTE) &
                    (dfVALOR_MO_UNIF_TRASERO['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                    [['VALOR_MO_MEAN','VALOR_MO_STD','CANT_HS_PINT_MEAN','CANT_HS_PINT_STD','VALOR_MAT_PINT_MEAN','VALOR_MAT_PINT_STD']] 
        
        flAverage=np.round((bfID_ELEM['VALOR_MO_MEAN']+bfID_ELEM['CANT_HS_PINT_MEAN']+bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
            
        flMin=np.round((bfID_ELEM['VALOR_MO_MEAN'] - bfID_ELEM['VALOR_MO_STD'])+ \
                       (bfID_ELEM['CANT_HS_PINT_MEAN'] - bfID_ELEM['CANT_HS_PINT_STD']) + \
                       (bfID_ELEM['VALOR_MAT_PINT_MEAN'] - bfID_ELEM['VALOR_MAT_PINT_STD']),2) 
            
        flMax=np.round((bfID_ELEM['VALOR_MO_MEAN'] + bfID_ELEM['VALOR_MO_STD']) + \
                       (bfID_ELEM['CANT_HS_PINT_MEAN']   + bfID_ELEM['CANT_HS_PINT_STD']) + \
                       (bfID_ELEM['VALOR_MAT_PINT_MEAN'] + bfID_ELEM['VALOR_MAT_PINT_STD']),2)  
            
        lsReparaAve.append(flAverage) 
        lsReparaMin.append(flMin) 
        lsReparaMax.append(flMax) 
   
    for index, item in enumerate(lsReparaAve): lsReparaAve[index] = list(set(item))[0]     
    for index, item in enumerate(lsReparaMin): lsReparaMin[index] = list(set(item))[0]     
    for index, item in enumerate(lsReparaMax): lsReparaMax[index] = list(set(item))[0]             
    
    return lsReparaAve,lsReparaMin,lsReparaMax

def fnCambiaTrasero(inSEG,inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,lsRepone):
    inCOD_PARTE = 2
    lsReponeAve = []
    lsReponeMin = []
    lsReponeMax = []
    flAverage = 0
    flMin     = 0
    flMax     = 0
    
    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['SEG'] == inSEG)        & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_CLASE']    == inCOD_CLASE)  & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_MARCA']    == inCOD_MARCA)  & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_MODELO']   == inCOD_MODELO) &          
                                        (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']    == inCOD_PARTE)  &
                    (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                                                    [['PRECIO_MEAN','PRECIO_STD']] 
        flAverage = np.round(bfID_ELEM['PRECIO_MEAN'],2)
        flMin     = np.round((bfID_ELEM['PRECIO_MEAN'] - bfID_ELEM['PRECIO_STD']),2) 
        flMax     = np.round((bfID_ELEM['PRECIO_MEAN'] + bfID_ELEM['PRECIO_STD']),2)  
        
        if len(flMin) == 0: flMin = [0]
        lsReponeMin.append(flMin) 
        if len(flAverage) == 0: flAverage = [0]
        if  item.upper().count('FARO') > 0:   
            lsReponeAve.append(flMin) 
        else:
            lsReponeAve.append(flAverage)
        if len(flMax) == 0: flMax = [0]
        lsReponeMax.append(flMax) 
    
    for index, item in enumerate(lsReponeMin): lsReponeMin[index] = list(set(item))[0]     
    for index, item in enumerate(lsReponeAve): lsReponeAve[index] = list(set(item))[0]     
    for index, item in enumerate(lsReponeMax): lsReponeMax[index] = list(set(item))[0]    
    
    return lsReponeAve,lsReponeMin,lsReponeMax 

def fnCambiaPinturaTrasero(inSEG,inCOD_CLASE,lsRepone):
    inCOD_PARTE = 2
    lsReponePintAve=[]
    lsReponePintMin=[]
    lsReponePintMax=[]
    lsReponeMoAv=[]
    lsReponeMoMin=[]
    lsReponeMoMax=[]
    flAverage=0
    flMin=0
    flMax=0
    flMoAv=0
    flMOMin=0
    flMoMax=0
    
    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_VALOR_MAT_TRASERO.loc[(dfVALOR_REPUESTO_VALOR_MAT_TRASERO['SEG']==inSEG)& 
                    (dfVALOR_REPUESTO_VALOR_MAT_TRASERO['COD_CLASE']==inCOD_CLASE)&
                    (dfVALOR_REPUESTO_VALOR_MAT_TRASERO['COD_PARTE']==inCOD_PARTE)&
                    (dfVALOR_REPUESTO_VALOR_MAT_TRASERO['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                        [['VALOR_MO_MEAN','VALOR_MO_STD','CANT_HS_PINT_MEAN','CANT_HS_PINT_STD',
                         'VALOR_MAT_PINT_MEAN','VALOR_MAT_PINT_STD']] 
        
        flAverage = np.round((bfID_ELEM['CANT_HS_PINT_MEAN'] + bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        flMin     = np.round(((bfID_ELEM['CANT_HS_PINT_MEAN'] - bfID_ELEM['CANT_HS_PINT_STD']) + \
                             (bfID_ELEM['VALOR_MAT_PINT_MEAN'] - bfID_ELEM['VALOR_MAT_PINT_STD'])),2) 
        flMax     = np.round(((bfID_ELEM['CANT_HS_PINT_MEAN'] + bfID_ELEM['CANT_HS_PINT_STD']) + \
                              (bfID_ELEM['VALOR_MAT_PINT_MEAN'] + bfID_ELEM['VALOR_MAT_PINT_STD'])),2)  
        
        flMoAv      = np.round(bfID_ELEM['VALOR_MO_MEAN'],2) 
        flMOMin     = np.round(((bfID_ELEM['VALOR_MO_MEAN'] - bfID_ELEM['VALOR_MO_STD'])),2) 
        flMoMax     = np.round(((bfID_ELEM['VALOR_MO_MEAN'] + bfID_ELEM['VALOR_MO_STD'])),2)  
        
        if len(flAverage)==0:flAverage=[0]
        if len(flMin)==0:flMin=[0]
        if len(flMax)==0:flMax=[0]
        if len(flMoAv)==0:flMoAv=[0]
        if len(flMOMin)==0:flMOMin=[0]
        if len(flMoMax)==0:flMoMax=[0]
                                  
        lsReponePintAve.append(flAverage) 
        lsReponePintMin.append(flMin) 
        lsReponePintMax.append(flMax) 
        lsReponeMoAv.append(flMoAv) 
        lsReponeMoMin.append(flMOMin) 
        lsReponeMoMax.append(flMoMax) 

    for index, item in enumerate(lsReponePintAve): lsReponePintAve[index]=list(set(item))[0]     
    for index, item in enumerate(lsReponePintMin): lsReponePintMin[index]=list(set(item))[0]     
    for index, item in enumerate(lsReponePintMax): lsReponePintMax[index]=list(set(item))[0]  
    for index, item in enumerate(lsReponeMoAv): lsReponeMoAv[index]=list(set(item))[0]      
    for index, item in enumerate(lsReponeMoMin): lsReponeMoMin[index]=list(set(item))[0]      
    for index, item in enumerate(lsReponeMoMax): lsReponeMoMax[index]=list(set(item))[0]        
    
    return lsReponePintAve,lsReponePintMin,lsReponePintMax,lsReponeMoAv,lsReponeMoMin,lsReponeMoMax 

def fnMolduraTrasero(inCOD_MARCA,inCOD_MODELO,lsMold):
    inCOD_PARTE = 2
    lsVersion = ['1','2','3','4','5'] 
    lsDf_MOLDURA = []
    lsMeanMold = []
    espMold = ['BAUL','PORTON','PARAGOLPE']
    
    dfMOLD_BAUL = dfMOLDURA.loc[(dfMOLDURA['COD_MARCA']  == inCOD_MARCA)  & 
                                (dfMOLDURA['COD_MODELO'] == inCOD_MODELO) &
                                (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                .sort_values(['VALOR'], ascending=[False])
    if len(dfMOLD_BAUL)==0:
            dfMOLD_BAUL = dfMOLDURA.loc[(dfMOLDURA['COD_MARCA'] == inCOD_MARCA)   & 
                                        (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                        (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                        .sort_values(['VALOR'], ascending=[False])
    # Extrae todos los que tienen numero incremental
    iIdx = 0
    for esp in lsVersion:
        dfTmp = dfMOLD_BAUL.loc[dfMOLD_BAUL['DESC_ELEM'].str.contains('|'.join(map(re.escape, esp)))]
        if len(dfTmp)==0: break
        lsDf_MOLDURA.append(dfTmp)
        iIdx+=1 
    # Extrae los que no tienen numero
    dfTmp = dfMOLD_BAUL.loc[~dfMOLD_BAUL['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]
    if len(dfTmp)!=0: lsDf_MOLDURA.append(dfTmp)    
    
    for dfMean in lsDf_MOLDURA:
        lsMeanMold.append(dfMean['VALOR'].mean().round(2))           
       
    return lsMeanMold

def fnEspejoLateral(inCOD_MARCA,inCOD_MODELO):
    lsVersion = ['1','2','3','4','5'] 
    lsDf_ESPEJO = []
    lsMeanEsp = []
    espElec = ['ESPEJO ELECTRICO']
    espMan  = ['ESPEJO MANUAL']
    espOut  = ['DER','IZQ','EMBELLEC','GIRO','MOLD','MOTOR','SONDA','SOP']
    
    dfESPEJO_ELEC = dfESPEJO.loc[(dfESPEJO['COD_MARCA'] == inCOD_MARCA) & (dfESPEJO['COD_MODELO'] == inCOD_MODELO) &
                                (dfESPEJO['DESC_ELEM'].str.contains('|'.join(map(re.escape, espElec)))) &
                                (~dfESPEJO['DESC_ELEM'].str.contains('|'.join(map(re.escape, espOut))))]\
                                .sort_values(['VALOR'], ascending=[False])
        
    if len(dfESPEJO_ELEC)==0:
        dfESPEJO_ELEC = dfESPEJO.loc[(dfESPEJO['COD_MARCA'] == inCOD_MARCA)   & 
                                (dfESPEJO['DESC_ELEM'].str.contains('|'.join(map(re.escape, espElec)))) &
                                (~dfESPEJO['DESC_ELEM'].str.contains('|'.join(map(re.escape, espOut))))]\
                                .sort_values(['VALOR'], ascending=[False])
    iIdx = 0
    for esp in lsVersion:
        dfTmp = dfESPEJO_ELEC.loc[dfESPEJO_ELEC['DESC_ELEM'].str.contains('|'.join(map(re.escape, esp)))]
        if len(dfTmp)==0: break
        lsDf_ESPEJO.append(dfTmp)
        iIdx+=1 
    
    dfTmp = dfESPEJO_ELEC.loc[~dfESPEJO_ELEC['DESC_ELEM'].str.contains('|'.join(map(re.escape, lsVersion)))]
    if len(dfTmp)!=0: lsDf_ESPEJO.append(dfTmp)

    for dfMean in lsDf_ESPEJO: lsMeanEsp.append(dfMean['VALOR'].mean().round(2))   
    
    return lsMeanEsp    

def fnMolduraLateral(inCOD_MARCA,inCOD_MODELO):
    inCOD_PARTE = 3
    #espMold = ['PUERTA','LATERAL','ZOCALO'] #Todo: Ver relaicon con cambio
    espMold = ['PUERTA']
    
    dfMOLD_LATERAL = dfMOLDURA.loc[(dfMOLDURA['COD_MARCA']  == inCOD_MARCA)  & 
                                   (dfMOLDURA['COD_MODELO'] == inCOD_MODELO) &
                                   (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                   (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                   .sort_values(['VALOR'], ascending=[False])
    
    if len(dfMOLD_LATERAL)==0:
            dfMOLD_LATERAL = dfMOLDURA.loc[(dfMOLDURA['COD_MARCA'] == inCOD_MARCA)   & 
                                           (dfMOLDURA['COD_PARTE']  == inCOD_PARTE)  &
                                           (dfMOLDURA['DESC_ELEM'].str.contains('|'.join(map(re.escape, espMold))))]\
                                           .sort_values(['VALOR'], ascending=[False])
    bfTmpMold = 0
    if len(dfMOLD_LATERAL)>=0:bfTmpMold=dfMOLD_LATERAL['VALOR'].mean().round(2)
        
    return bfTmpMold
 
def fnReparaLateral(inSEG,inCOD_CLASE,lsRepara):
    inCOD_PARTE = 3
    lsReparaAve = []
    lsReparaMin = []
    lsReparaMax = []
    flAverage = 0
    flMin     = 0
    flMax     = 0
    for index, item in enumerate(lsRepara):
        bfID_ELEM = dfVALOR_MO_UNIF_LATERAL.loc[(dfVALOR_MO_UNIF_LATERAL['SEG']==inSEG)&(dfVALOR_MO_UNIF_LATERAL['COD_CLASE']==inCOD_CLASE)& 
                                        (dfVALOR_MO_UNIF_LATERAL['COD_PARTE']==inCOD_PARTE)&
                                        (dfVALOR_MO_UNIF_LATERAL['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                                      [['VALOR_MO_MEAN','VALOR_MO_STD','CANT_HS_PINT_MEAN','CANT_HS_PINT_STD',
                                                                        'VALOR_MAT_PINT_MEAN','VALOR_MAT_PINT_STD']] 
                                                                      
        flAverage = np.round((bfID_ELEM['VALOR_MO_MEAN']+bfID_ELEM['CANT_HS_PINT_MEAN']+bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        
        flMin     = np.round((bfID_ELEM['VALOR_MO_MEAN']-bfID_ELEM['VALOR_MO_STD'])+(bfID_ELEM['CANT_HS_PINT_MEAN']-bfID_ELEM['CANT_HS_PINT_STD'])+\
                             (bfID_ELEM['VALOR_MAT_PINT_MEAN'] - bfID_ELEM['VALOR_MAT_PINT_STD']),2) 
        
        flMax     = np.round((bfID_ELEM['VALOR_MO_MEAN'] + bfID_ELEM['VALOR_MO_STD'])+(bfID_ELEM['CANT_HS_PINT_MEAN']+bfID_ELEM['CANT_HS_PINT_STD'])+\
                             (bfID_ELEM['VALOR_MAT_PINT_MEAN'] + bfID_ELEM['VALOR_MAT_PINT_STD']),2)  
        
        lsReparaAve.append(flAverage) 
        lsReparaMin.append(flMin) 
        lsReparaMax.append(flMax) 
        
    for index, item in enumerate(lsReparaAve): lsReparaAve[index]=list(set(item))[0]     
    for index, item in enumerate(lsReparaMin): lsReparaMin[index]=list(set(item))[0]     
    for index, item in enumerate(lsReparaMax): lsReparaMax[index]=list(set(item))[0]    
    
    return lsReparaAve,lsReparaMin,lsReparaMax           

def fnCambiaLateral(inSEG,inCOD_CLASE,inCOD_MARCA,inCOD_MODELO,lsRepone):
    inCOD_PARTE = 3
    lsReponeAve = []
    lsReponeMin = []
    lsReponeMax = []
    flAverage = 0
    flMin     = 0
    flMax     = 0
    
    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_MO_Unif.loc[(dfVALOR_REPUESTO_MO_Unif['SEG'] == inSEG)        & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_CLASE']    == inCOD_CLASE)  & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_MARCA']    == inCOD_MARCA)  & 
                                        (dfVALOR_REPUESTO_MO_Unif['COD_MODELO']   == inCOD_MODELO) &          
                                        (dfVALOR_REPUESTO_MO_Unif['COD_PARTE']    == inCOD_PARTE)  &
                        (dfVALOR_REPUESTO_MO_Unif['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                                                       [['PRECIO_MEAN','PRECIO_STD']] 
        flAverage = np.round(bfID_ELEM['PRECIO_MEAN'],2)
        flMin     = np.round((bfID_ELEM['PRECIO_MEAN'] - bfID_ELEM['PRECIO_STD']),2) 
        flMax     = np.round((bfID_ELEM['PRECIO_MEAN'] + bfID_ELEM['PRECIO_STD']),2)  
        
        if len(flMin) == 0: flMin = [0]
        lsReponeMin.append(flMin) 
        if len(flAverage) == 0: flAverage = [0]
        if  item.upper().count('FARO') > 0:   
            lsReponeAve.append(flMin) 
        else:
            lsReponeAve.append(flAverage)
        if len(flMax) == 0: flMax = [0]
        lsReponeMax.append(flMax) 
        
    for index, item in enumerate(lsReponeMin): lsReponeMin[index] = list(set(item))[0]     
    for index, item in enumerate(lsReponeAve): lsReponeAve[index] = list(set(item))[0]     
    for index, item in enumerate(lsReponeMax): lsReponeMax[index] = list(set(item))[0]         
    
    return lsReponeAve,lsReponeMin,lsReponeMax

def fnCambiaPinturaLateral(inSEG,inCOD_CLASE,lsRepone):
    inCOD_PARTE = 3
    lsReponePintAve = []
    lsReponePintMin = []
    lsReponePintMax = []
    lsReponeMoAv    = []
    lsReponeMoMin   = []
    lsReponeMoMax   = []
    
    flAverage = 0
    flMin     = 0
    flMax     = 0
    flMoAv    = 0
    flMOMin   = 0
    flMoMax   = 0
    
    for index, item in enumerate(lsRepone):
        bfID_ELEM = dfVALOR_REPUESTO_VALOR_MAT_LATERAL.loc[(dfVALOR_REPUESTO_VALOR_MAT_LATERAL['SEG']==inSEG)       & 
                                             (dfVALOR_REPUESTO_VALOR_MAT_LATERAL['COD_CLASE']==inCOD_CLASE) & 
                                             (dfVALOR_REPUESTO_VALOR_MAT_LATERAL['COD_PARTE']==inCOD_PARTE) &
                        (dfVALOR_REPUESTO_VALOR_MAT_LATERAL['DESC_ELEM'].astype(str).str.contains(item,case=False,regex=True))]\
                                                                                      [['VALOR_MO_MEAN','VALOR_MO_STD','CANT_HS_PINT_MEAN',
                                                                                        'CANT_HS_PINT_STD','VALOR_MAT_PINT_MEAN','VALOR_MAT_PINT_STD']] 
        
        
        flAverage = np.round((bfID_ELEM['CANT_HS_PINT_MEAN']+bfID_ELEM['VALOR_MAT_PINT_MEAN']),2)
        flMin     = np.round(((bfID_ELEM['CANT_HS_PINT_MEAN']-bfID_ELEM['CANT_HS_PINT_STD'])+(bfID_ELEM['VALOR_MAT_PINT_MEAN']-bfID_ELEM['VALOR_MAT_PINT_STD'])),2) 
        flMax     = np.round(((bfID_ELEM['CANT_HS_PINT_MEAN']+bfID_ELEM['CANT_HS_PINT_STD'])+(bfID_ELEM['VALOR_MAT_PINT_MEAN']+bfID_ELEM['VALOR_MAT_PINT_STD'])),2)  
        
        flMoAv  = np.round(bfID_ELEM['VALOR_MO_MEAN'],2) 
        flMOMin = np.round(((bfID_ELEM['VALOR_MO_MEAN']-bfID_ELEM['VALOR_MO_STD'])),2) 
        flMoMax = np.round(((bfID_ELEM['VALOR_MO_MEAN']+bfID_ELEM['VALOR_MO_STD'])),2)  
        
        if len(flAverage) == 0: flAverage = [0]
        lsReponePintAve.append(flAverage) 
        if len(flMin) == 0: flMin = [0]
        lsReponePintMin.append(flMin) 
        if len(flMax) == 0: flMax = [0]
        lsReponePintMax.append(flMax) 
        if len(flMoAv) == 0: flMoAv = [0]
        lsReponeMoAv.append(flMoAv) 
        if len(flMOMin) == 0: flMOMin = [0]
        lsReponeMoMin.append(flMOMin) 
        if len(flMoMax) == 0: flMoMax = [0]
        lsReponeMoMax.append(flMoMax) 
        
    for index, item in enumerate(lsReponePintAve): lsReponePintAve[index] = list(set(item))[0]     
    for index, item in enumerate(lsReponePintMin): lsReponePintMin[index] = list(set(item))[0]     
    for index, item in enumerate(lsReponePintMax): lsReponePintMax[index] = list(set(item))[0]  
    
    for index, item in enumerate(lsReponeMoAv): lsReponeMoAv[index] = list(set(item))[0]      
    for index, item in enumerate(lsReponeMoMin): lsReponeMoMin[index] = list(set(item))[0]      
    for index, item in enumerate(lsReponeMoMax): lsReponeMoMax[index] = list(set(item))[0]      

    return lsReponePintAve,lsReponePintMin,lsReponePintMax,lsReponeMoAv,lsReponeMoMin,lsReponeMoMax

##################################################
def resumeDataBrief(intCLIENTE,fltLAteral,fltTrasero):
    
    ftSum = fltLAteral + fltTrasero
    if intCLIENTE == 1: ftSum *= param.bfAsegurado
    elif intCLIENTE == 2: ftSum *= param.bfTercero
           
    txtValorTotal = "<span id=\"CostBrief\" class=\"pure-form-message-inline\" style=\"text-align:right;font-family:'helvetica neue';font-size:100%;color:rgb(170,27,23);\">Costo sugerido&nbsp$&nbsp{0:0.2f}".format(ftSum)+"</span>"

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
