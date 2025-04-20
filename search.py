bfHTML = """
<html>
  <head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/pure-min.css" integrity="sha384-X38yfunGUhNzHpBaEBsWLO+A0HDYOQi8ufWDkZ0k9e0eXz/tH3II7uKZ9msv++Ls" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/grids-responsive-min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link id="favicon" rel="icon" type="image/x-icon" href="/img/favicon.ico">
    <link href='http://fonts.cdnfonts.com/css/helvetica-neue-9' rel='stylesheet' type='text/css'>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

    <style>
        body {background-color:rgb(255,255,255);}
        label {text-align:right;font-family:'helvetica neue';font-size: 100%;}
        .vertical-text {
            writing-mode: vertical-rl; /* Texto vertical de derecha a izquierda */
            transform: rotate(180deg); /* Opcional: rota 180 grados para cambiar la dirección */
        }
    </style>
    <title>App Presupuesto</title>
</head>
<body>
    <div class="pure-g" style="text-align:center;"><div class="pure-u-*">&nbsp;</div></div> 
    <!--
    <div class="pure-g" style="text-align:center;">
        <div class="pure-u-1 pure-u-md-5-5"> 
            <div class="pure-menu pure-menu-horizontal">
                <ul class="pure-menu-list">
                    <li class="pure-menu-item pure-menu-selected">
                        <a href="#" class="pure-menu-link">Consultar</a>
                    </li>
                    <li class="pure-menu-item">
                        <a href="#" class="pure-menu-link">&nbsp;&nbsp;&nbsp;</a>
                    </li>
                    <li class="pure-menu-item">
                        <a href="#" class="pure-menu-link">Salir</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
     -->
    <div id = "divContent" class="pure-g" style="text-align:center;"><div class="pure-u-*">&nbsp;</div></div>
    <div class="pure-g" style="padding-left:5px;">
        <div class="pure-u-1 pure-u-md-7-24"> <!--<div class="pure-u-1 pure-u-md-1-5">-->
            <img src="./img/Pos_color_RGB.jpg" alt="logo" width="128" height="128"
             style="margin-left:auto;margin-right:auto;display:block;"/>
            <p>&nbsp;</p>
            <p class="vertical-text"
                style="margin-left:auto;margin-right:auto;display:block;
                       font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                       color:#005993;text-align:center; font-size: 25px;">Cotizador</p>
        </div> 
        <div id = "divPrint"> 
            <div class="pure-u-1 pure-u-md-7-24"> <!--<div class="pure-u-1 pure-u-md-3-5">-->
                <form class="pure-form pure-form-aligned">
                    <fieldset>
                        <div class="pure-control-group">
                            <label for="aligned-name" style="color:#005993;text-align:left;">Cliente</label>
                            <select id="stacked-cliente" style="min-width:343px;">
                                <option id=0></option>
                                <option id=1>ASEGURADO</option>
                                <option id=2 selected>TERCERO</option>
                            </select>
                        </div>
                        <div class="pure-control-group">
                            <label for="aligned-name" style="color:#005993;text-align:left;">Clase</label>
                            <select id="stacked-clase" style="min-width:343px;" onchange="fnGetClase()">
                                <option id=0></option>
                                <option id=901>SEDAN</option>
                                <option id=907>SUV</option>
                                <option id=915>MOTO</option>
                            </select>
                        </div>
                        <div class="pure-control-group">
                            <label for="aligned-name" style="color:#005993;text-align:left;">Marca</label>
                            <select id="stacked-marca" style="min-width:343px;max-width:255px;" onchange="fnGetModelo()">
                                <option id=0></option>
                            </select>
                        </div>
                        <div class="pure-control-group">
                            <label for="aligned-name" style="color:#005993;text-align:left;">Modelo</label>
                            <select id="stacked-modelo" style="min-width:343px;">
                                <option id=0></option>
                            </select>
                        </div>
                        <div class="pure-control-group">
                            <label for="aligned-name" style="color:#005993;text-align:left;">Siniestro</label>
                            <input type="email" id="stacked-siniestro" placeholder="" style="min-width:343px;" onblur="checkLength(this)"/>
                        </div>
                        <div class="pure-control-group">
                            <label for="aligned-name" style="color:#005993;text-align:left;">Perito</label>
                            <input type="email" id="stacked-perito" placeholder="" style="min-width:343px;"/>
                        </div>
                        <div class="pure-control-group">
                            <label for="aligned-name" style="color:#005993;text-align:left;">Valor</label>
                            <input type="email" id="stacked-valorperito" placeholder="" style="min-width:343px;"/>
                        </div>
                </fieldset>
                </form>
                <table class="pure-table pure-table-striped">
                    <thead>
                        <tr>
                            <th style="min-width:105px;max-width:105px;background-color:#005993;color:#ffffff;"><input type="checkbox" id="frente_chk" onclick="return viewGrid(this,'frente');return false;"/>&nbsp;Frente&nbsp;&nbsp;</th>
                            <th id="frente_repara" style="min-width:70px;max-width:70px;background-color:#005993;color:#ffffff;border-spacing:2px" colspan="2">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
                            <th id="frente_cambia" style="min-width:70px;max-width:70px;background-color:#005993;color:#ffffff;border-spacing:2px" colspan="2">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
                        </tr>
                    </thead>
                    <tbody id="frente" style="display:none">
                        <tr>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">&nbsp;</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Cambia</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Repara</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Cambia</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Repara</td>
                        </tr>
                        <tr>
                            <td style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Capot</td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_DER_CAPOT" onclick="unCheckOps('FRT_CAM_DER_CAPOT','FRT_REP_DER_CAPOT')"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_REP_DER_CAPOT" onclick="unCheckOps('FRT_REP_DER_CAPOT','FRT_CAM_DER_CAPOT')"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Farito</td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_DER_FARITO"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_IZQ_FARITO"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Faro</td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_DER_FARO"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_IZQ_FARO"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Faro&nbsp;Auxiliar</td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_DER_FARO_AUXILIAR"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_IZQ_FARO_AUXILIAR"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Frente</td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_DER_FRENTE" onclick="unCheckOps('FRT_CAM_DER_FRENTE','FRT_REP_DER_FRENTE')"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_REP_DER_FRENTE" onclick="unCheckOps('FRT_REP_DER_FRENTE','FRT_CAM_DER_FRENTE')"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Guardabarro</td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_DER_GUARDABARRO" onclick="unCheckOps('FRT_CAM_DER_GUARDABARRO','FRT_REP_DER_GUARDABARRO')"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_REP_DER_GUARDABARRO" onclick="unCheckOps('FRT_REP_DER_GUARDABARRO','FRT_CAM_DER_GUARDABARRO')"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_IZQ_GUARDABARRO" onclick="unCheckOps('FRT_CAM_IZQ_GUARDABARRO','FRT_REP_IZQ_GUARDABARRO')"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_REP_IZQ_GUARDABARRO" onclick="unCheckOps('FRT_REP_IZQ_GUARDABARRO','FRT_CAM_IZQ_GUARDABARRO')"/</td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:3px;padding-top:5px;">Parabrisas</td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_DER_PARABRISAS"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:3px;padding-top:5px;">Paragolpe&nbsp;Alma</td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_DER_PARAGOLPE_ALMA" onclick="unCheckOps('FRT_CAM_DER_PARAGOLPE_ALMA','FRT_CAM_REP_PARAGOLPE_ALMA')"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_REP_PARAGOLPE_ALMA" onclick="unCheckOps('FRT_CAM_REP_PARAGOLPE_ALMA','FRT_CAM_DER_PARAGOLPE_ALMA')"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Paragolpe&nbsp;Ctro</td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_DER_PARAGOLPE_CTRO" onclick="unCheckOps('FRT_CAM_DER_PARAGOLPE_CTRO','FRT_REP_DER_PARAGOLPE_CTRO')"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_REP_DER_PARAGOLPE_CTRO" onclick="unCheckOps('FRT_REP_DER_PARAGOLPE_CTRO','FRT_CAM_DER_PARAGOLPE_CTRO')"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Paragolpe&nbsp;Rejilla</td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_DER_PARAGOLPE_REJILLA"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Rejilla&nbsp;Radiador</td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="FRT_CAM_DER_REJILLA_RADIADOR"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                    </tbody>
                </table>
                <table class="pure-table pure-table-striped">
                    <thead>
                        <tr>
                            <th style="min-width:105px;max-width:105px;background-color:#005993;color:#ffffff;"><input type="checkbox" id="lateral_chk" onclick="return viewGrid(this,'lateral');return false;"/>&nbsp;Lateral&nbsp;&nbsp;</th>
                            <th id="lateral_repara" style="min-width:70px;max-width:70px;background-color:#005993;color:#ffffff;border-spacing:2px" colspan="2">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
                            <th id="lateral_cambia" style="min-width:70px;max-width:70px;background-color:#005993;color:#ffffff;border-spacing:2px" colspan="2">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
                        </tr>
                    </thead>
                    <tbody id="lateral" style="display:none">
                        <tr>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">&nbsp;</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Cambia</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Repara</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Cambia</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Repara</td>
                        </tr>
                        <tr>
                            <td style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Cristal Delantero</td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_CRISTAL_DEL"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_CRISTAL_DEL"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Cristal Trasero</td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_CRISTAL_TRA"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_CRISTAL_TRA"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Espejo El&eacute;ctrico</td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_ESPEJO_ELEC" onclick="document.getElementById('LAT_CAM_DER_ESPEJO_MAN').checked=false;"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_ESPEJO_ELEC" onclick="document.getElementById('LAT_CAM_IZQ_ESPEJO_MAN').checked=false;"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Espejo Manual</td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_ESPEJO_MAN" onclick="document.getElementById('LAT_CAM_DER_ESPEJO_ELEC').checked=false;"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_ESPEJO_MAN" onclick="document.getElementById('LAT_CAM_IZQ_ESPEJO_ELEC').checked=false;"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Manija Pta Del</td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_MANIJA_DEL"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_MANIJA_DEL"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Manija Pta Tras</td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_MANIJA_TRA"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_MANIJA_TRA"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:3px;padding-top:5px;">Moldura Pta Del</td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_MOLDURA_DEL"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_MOLDURA_DEL"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:3px;padding-top:5px;">Moldura Pta Tras</td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_MOLDURA_TRA"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_MOLDURA_TRA"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Puerta Delantera</td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_PUERTA_DEL"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_PUERTA_DEL"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Puerta Trasera</td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_PUERTA_TRA"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_PUERTA_TRA"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Puerta Panel Del</td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_REP_DER_PUERTA_DEL_PANEL"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_REP_IZQ_PUERTA_DEL_PANEL"/></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-left:5px;padding-right:3px;padding-bottom:3px;padding-top:5px;">Puerta Panel Tras</td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_REP_DER_PUERTA_TRA_PANEL"/></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_REP_IZQ_PUERTA_TRA_PANEL"/></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Zocalo</td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_ZOCALO" onclick="unCheckOps('LAT_CAM_DER_ZOCALO','LAT_REP_DER_ZOCALO')"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_REP_DER_ZOCALO" onclick="unCheckOps('LAT_REP_DER_ZOCALO','LAT_CAM_DER_ZOCALO')"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_ZOCALO" onclick="unCheckOps('LAT_CAM_IZQ_ZOCALO','LAT_REP_IZQ_ZOCALO')"/></td>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_REP_IZQ_ZOCALO" onclick="unCheckOps('LAT_REP_IZQ_ZOCALO','LAT_CAM_IZQ_ZOCALO')"/></td>
                        </tr>
                    </tbody>
                </table>
                <table class="pure-table pure-table-striped">
                    <thead>
                        <tr>
                            <th style="min-width:105px;max-width:105px;background-color:#005993;color:#ffffff;"><input type="checkbox" id="trasero_chk" onclick="return viewGrid(this,'trasero');return false;"/>&nbsp;Trasero&nbsp;</th>
                            <th id="trasero_repara" style="min-width:70px;max-width:70px;background-color:#005993;color:#ffffff;border-spacing:2px" colspan="2">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
                            <th id="trasero_cambia" style="min-width:70px;max-width:70px;background-color:#005993;color:#ffffff;border-spacing:2px" colspan="2">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th>
                        </tr>
                    </thead>
                    <tbody id="trasero" style="display:none">
                        <tr>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">&nbsp;</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Cambia</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Repara</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Cambia</td>
                            <td height="10px" style="font-size:small;text-align:center;vertical-align:middle;background-color:#FFFFFF;color:#000000;padding-bottom:2px;padding-left:3px;padding-top:2px;padding-right:3px;">Repara</td>
                        </tr>
                        <tr>
                            <td style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Baul/Port&oacute;n</td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_BAUL" onclick="unCheckOps('TRA_CAM_DER_BAUL','TRA_REP_DER_BAUL')"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_REP_DER_BAUL"  onclick="unCheckOps('TRA_REP_DER_BAUL','TRA_CAM_DER_BAUL')"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td style="padding-left:5px;padding-right:5px;padding-bottom:3px;padding-top:3px;background-color:#FFFFFF;color:#000000;">Faro Ext</td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_FARO_EXT"/></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_IZQ_FARO_EXT"/></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td style="padding-left:5px;padding-right:5px;padding-bottom:3px;padding-top:3px;background-color:#DEF3FF;color:#000000;">Faro Int</td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_FARO_INT"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_IZQ_FARO_INT"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Guardabarro</td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_GUARDABARRO" onclick="unCheckOps('TRA_CAM_DER_GUARDABARRO','TRA_REP_DER_GUARDABARRO')"/></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_REP_DER_GUARDABARRO" onclick="unCheckOps('TRA_REP_DER_GUARDABARRO','TRA_CAM_DER_GUARDABARRO')"/></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_IZQ_GUARDABARRO" onclick="unCheckOps('TRA_CAM_IZQ_GUARDABARRO','TRA_REP_IZQ_GUARDABARRO')"/></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_REP_IZQ_GUARDABARRO" onclick="unCheckOps('TRA_REP_IZQ_GUARDABARRO','TRA_CAM_IZQ_GUARDABARRO')"/></td>
                        </tr>
                        <tr>
                            <td style="background-color:#DEF3FF;color:#000000;padding-left:5px;padding-right:5px;padding-bottom:3px;padding-top:3px;">Luneta</td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_LUNETA"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Moldura</td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_MOLDURA"/></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Panel Cola</td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_PANELCOLA" onclick="unCheckOps('TRA_CAM_DER_PANELCOLA','TRA_REP_DER_PANELCOLA')"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_REP_DER_PANELCOLA" onclick="unCheckOps('TRA_REP_DER_PANELCOLA','TRA_CAM_DER_PANELCOLA')"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Paragolpe</td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_PARAGOLPE" onclick="unCheckOps('TRA_CAM_DER_PARAGOLPE','TRA_REP_DER_PARAGOLPE')"/></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_REP_DER_PARAGOLPE" onclick="unCheckOps('TRA_REP_DER_PARAGOLPE','TRA_CAM_DER_PARAGOLPE')"/></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                    </tbody>
                </table>
                <br style="display: block;content:'';margin-top:5;">
                <span id="CostBrief" class="pure-form-message-inline" style="padding-left:3px;text-align:left;font-family:'helvetica neue';font-size:100%;color:rgb(170,27,23);">&nbsp;&nbsp;</span>
            </div>
        </div>     
    </div>     
    <div class="pure-g" style="padding-left:5px;">
        <div class="pure-u-1 pure-u-md-7-24"></div> 
        <div class="pure-u-1 pure-u-md-7-24">
            <div class="pure-controls"><input type="hidden" id="HiddenData" value="">&nbsp;</div>
            <div class="pure-controls" style="padding-center;">
                <button style="background-color:#005993;color:#ffffff;" class="pure-button pure-button-primary" onclick="fnGetData()">Consultar</button>
                <button style="background-color:#005993;color:#ffffff;" class="pure-button pure-button-primary"  onclick="fnClean()">&nbsp;&nbsp;Limpiar&nbsp;&nbsp;</button>
                <button style="background-color:#005993;color:#ffffff;" class="pure-button pure-button-primary" id="descargar">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PDF&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</button>
            </div>
        </div>
        <div class="pure-u-1 pure-u-md-7-24"></div>
    </div> 
    <br style="display: block;content:'';margin-top:5;">    
   </body>
   <script>
        document.getElementById("descargar").disabled = true;
        document.getElementById("descargar").addEventListener("click", function () {
            
            const seleccionadosFrente  = obtenerCheckeadosFrente("frente_chk", "#frente tr");
            const seleccionadosLateral = obtenerCheckeadosFrente("lateral_chk", "#lateral tr");
            const seleccionadosTrasero = obtenerCheckeadosFrente("trasero_chk", "#trasero tr");
            
            let mensaje = '<h3>Elementos Incluidos en el Presupuesto</h3>';
            if (seleccionadosFrente.length > 0) {
                mensaje += '<h4>Frente</h4>';
                seleccionadosFrente.forEach(item => { mensaje += "<p>&nbsp;&nbsp;&nbsp;" + item.descripcion  + "</p>"; });
              }
            if (seleccionadosLateral.length > 0) {
                mensaje += '<h4>Lateral</h4>';
                seleccionadosLateral.forEach(item => { mensaje += "<p>&nbsp;&nbsp;&nbsp;" + item.descripcion  + "</p>"; });
              }
            if (seleccionadosTrasero.length > 0) {
                mensaje += '<h4>Trasero</h4>';
                seleccionadosTrasero.forEach(item => { mensaje += "<p>&nbsp;&nbsp;&nbsp;" + item.descripcion  + "</p>"; });
              } 
                       
            const divPrint = document.getElementById("divPrint");
            const resultadoAhora = obtenerYFormatearFechaHoraActual();
            cDiaHora = resultadoAhora.formatoCompleto;
            cDia = resultadoAhora.diaSeparado;
            cHora = resultadoAhora.horaSeparada;
            
            formatoTXT = procesarDivParaImprimir(divPrint, cDia, cHora, mensaje);
            const tempDiv = document.createElement("div");
            tempDiv.innerHTML = formatoTXT;
            document.body.appendChild(tempDiv);
           
            html2canvas(tempDiv).then(canvas => {
                const imgData = canvas.toDataURL('image/png');
                const { jsPDF } = window.jspdf;
                const doc = new jsPDF();
                doc.addImage(imgData, 'PNG', 10, 10);
                doc.save(cDiaHora + '_presupuesto.pdf');
                document.body.removeChild(tempDiv);
            });

        });

    function obtenerCheckeadosFrente(cTableId, cTableBody) {
        const chkTableId = document.getElementById(cTableId);
        if (!chkTableId.checked) {return [];}

        const traducciones = {
            "FRT": "Frente",
            "LAT": "Lateral",
            "TRA": "Trasero",
            "CAM": "Cambia",
            "REP": "Repara",
            "DER": "Derecho",
            "IZQ": "Izquierdo"
        };

        const seleccionados = [];
        const filas = document.querySelectorAll(cTableBody);

        filas.forEach(fila => {
            const tds = fila.querySelectorAll("td");
            if (tds.length === 0) return;

            const nombrePieza = tds[0].textContent.trim();
            for (let i = 1; i < tds.length; i++) {
                const chk = tds[i].querySelector("input[type='checkbox']");
                if (chk && chk.checked) {
                    const partes = chk.id.split('_');
                    let descripcionID = partes.slice(1, -1).map(p => traducciones[p] || p).join(" ");
                    seleccionados.push({
                        id: chk.id,
                        descripcion: `${descripcionID} ${nombrePieza}`
                    });
                }
            }
        });

        return seleccionados;
    }
        
    function fnClean(){
        var e = document.getElementById("stacked-cliente");
            e.selectedIndex = 0;
        var e = document.getElementById("stacked-clase");
            e.selectedIndex = 0;
        var e = document.getElementById("stacked-marca");
            e.selectedIndex = 0;
        var e = document.getElementById("stacked-modelo");
            e.selectedIndex = 0;
            e.style.width = "250px";
        var e = document.getElementById("stacked-siniestro");
            e.value = "";
        var e = document.getElementById("stacked-perito");
            e.value = "";
        var e = document.getElementById("stacked-valorperito");
            e.value = "";        

        var e = document.getElementById("frente_chk");
            e.checked = false;    
        var e = document.getElementById("frente_repara");    
            e.innerText = "";
        var e = document.getElementById("frente_cambia");
            e.innerText = "";
        
        var e = document.getElementById("frente");
            e.style.display = "none";      

        var e = document.getElementById("FRT_CAM_DER_CAPOT");
            e.checked = false;       
        var e = document.getElementById("FRT_REP_DER_CAPOT");
            e.checked = false;       
        var e = document.getElementById("FRT_CAM_DER_FARITO");
            e.checked = false;       
        var e = document.getElementById("FRT_CAM_IZQ_FARITO");
            e.checked = false;       
        var e = document.getElementById("FRT_CAM_DER_FARO");
            e.checked = false;       
        var e = document.getElementById("FRT_CAM_IZQ_FARO");
            e.checked = false;    
        var e = document.getElementById("FRT_CAM_DER_FARO_AUXILIAR");
            e.checked = false;                  
        var e = document.getElementById("FRT_CAM_IZQ_FARO_AUXILIAR");
            e.checked = false;  
        var e = document.getElementById("FRT_CAM_DER_FRENTE");
            e.checked = false;                   
        var e = document.getElementById("FRT_REP_DER_FRENTE");
            e.checked = false;  
        var e = document.getElementById("FRT_CAM_DER_GUARDABARRO");
            e.checked = false;                   
        var e = document.getElementById("FRT_REP_DER_GUARDABARRO");
            e.checked = false;  
        var e = document.getElementById("FRT_CAM_IZQ_GUARDABARRO");
            e.checked = false;  
        var e = document.getElementById("FRT_REP_IZQ_GUARDABARRO");
            e.checked = false;  
        var e = document.getElementById("FRT_CAM_DER_PARABRISAS");
            e.checked = false;  
        var e = document.getElementById("FRT_CAM_DER_PARAGOLPE_ALMA");
            e.checked = false;       
        var e = document.getElementById("FRT_CAM_REP_PARAGOLPE_ALMA");
            e.checked = false;       
        var e = document.getElementById("FRT_CAM_DER_PARAGOLPE_CTRO");
            e.checked = false;       
        var e = document.getElementById("FRT_REP_DER_PARAGOLPE_CTRO");
            e.checked = false;       
        var e = document.getElementById("FRT_CAM_DER_PARAGOLPE_REJILLA");
            e.checked = false;       
        var e = document.getElementById("FRT_CAM_DER_REJILLA_RADIADOR");
            e.checked = false;       
            
        var e = document.getElementById("lateral_chk");
            e.checked = false;    
        var e = document.getElementById("lateral_repara");    
            e.innerText = ""; 
        var e = document.getElementById("lateral_cambia");
            e.innerText = ""; 
        
        var e = document.getElementById("lateral");
            e.style.display = "none";      
            
        var e = document.getElementById("LAT_CAM_DER_CRISTAL_DEL");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_IZQ_CRISTAL_DEL");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_DER_CRISTAL_TRA");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_IZQ_CRISTAL_TRA");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_DER_ESPEJO_ELEC");
            e.checked = false;  
        var e = document.getElementById("LAT_CAM_IZQ_ESPEJO_ELEC");
            e.checked = false;                   
        var e = document.getElementById("LAT_CAM_DER_ESPEJO_MAN");
            e.checked = false;  
        var e = document.getElementById("LAT_CAM_IZQ_ESPEJO_MAN");
            e.checked = false;                   
        var e = document.getElementById("LAT_CAM_DER_MANIJA_DEL");
            e.checked = false;  
        var e = document.getElementById("LAT_CAM_IZQ_MANIJA_DEL");
            e.checked = false;  
        var e = document.getElementById("LAT_CAM_DER_MANIJA_TRA");
            e.checked = false;  
        var e = document.getElementById("LAT_CAM_IZQ_MANIJA_TRA");
            e.checked = false;  
        var e = document.getElementById("LAT_CAM_DER_MOLDURA_DEL");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_IZQ_MOLDURA_DEL");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_DER_MOLDURA_TRA");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_IZQ_MOLDURA_TRA");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_DER_PUERTA_DEL");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_IZQ_PUERTA_DEL");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_DER_PUERTA_TRA");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_IZQ_PUERTA_TRA");
            e.checked = false;       
        var e = document.getElementById("LAT_REP_DER_PUERTA_DEL_PANEL");
            e.checked = false;       
        var e = document.getElementById("LAT_REP_IZQ_PUERTA_DEL_PANEL");
            e.checked = false;       
        var e = document.getElementById("LAT_REP_DER_PUERTA_TRA_PANEL");
            e.checked = false;       
        var e = document.getElementById("LAT_REP_IZQ_PUERTA_TRA_PANEL");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_DER_ZOCALO");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_IZQ_ZOCALO");
            e.checked = false;       
        var e = document.getElementById("LAT_REP_DER_ZOCALO");
            e.checked = false;       
        var e = document.getElementById("LAT_REP_IZQ_ZOCALO");
            e.checked = false;       

        var e = document.getElementById("trasero_chk");
            e.checked = false;    
        var e = document.getElementById("trasero_repara");    
            e.innerText = ""; 
        var e = document.getElementById("trasero_cambia");    
            e.innerText = ""; 
                      
        var e = document.getElementById("trasero");
            e.style.display = "none";    
            
        var e = document.getElementById("TRA_CAM_DER_BAUL");
            e.checked = false; 
        var e = document.getElementById("TRA_REP_DER_BAUL");
            e.checked = false;                
        var e = document.getElementById("TRA_CAM_DER_FARO_EXT");    
            e.checked = false;    
        var e = document.getElementById("TRA_CAM_IZQ_FARO_EXT");
            e.checked = false;     
        var e = document.getElementById("TRA_CAM_DER_FARO_INT");    
            e.checked = false;    
        var e = document.getElementById("TRA_CAM_IZQ_FARO_INT");
            e.checked = false;     
        var e = document.getElementById("TRA_CAM_DER_GUARDABARRO");
            e.checked = false;    
        var e = document.getElementById("TRA_CAM_IZQ_GUARDABARRO");    
            e.checked = false; 
        var e = document.getElementById("TRA_REP_DER_GUARDABARRO");
            e.checked = false;    
        var e = document.getElementById("TRA_REP_IZQ_GUARDABARRO");    
            e.checked = false; 
        var e = document.getElementById("TRA_CAM_DER_LUNETA");
            e.checked = false;    
        var e = document.getElementById("TRA_CAM_DER_MOLDURA");
            e.checked = false;    
        var e = document.getElementById("TRA_REP_DER_PANELCOLA");
            e.checked = false;    
        var e = document.getElementById("TRA_CAM_DER_PANELCOLA");
            e.checked = false;    
        var e = document.getElementById("TRA_CAM_DER_PARAGOLPE");
            e.checked = false;    
        var e = document.getElementById("TRA_REP_DER_PARAGOLPE");
            e.checked = false;    

        var e = document.getElementById("CostBrief");
            e.innerHTML = '&nbsp;';
    }
    function fnGetData(){
        
        var e = document.getElementById("stacked-cliente");
        if(e.options[e.selectedIndex].id == 0) 
        {
            alert('Debe seleccionar Cliente');
            e.focus(); 
            return
        }    
        var text = 'CLIENTE=' + e.options[e.selectedIndex].id;
        
        var e = document.getElementById("stacked-clase");
        if(e.options[e.selectedIndex].id == 0) 
        {
            alert('Debe seleccionar Clase');
            e.focus(); 
            return
        }    
        text = text + '&CLASE=' + e.options[e.selectedIndex].id;
        isMoto = e.options[e.selectedIndex].id;
            
        if(isMoto!="915") 
        {           
            var e = document.getElementById("stacked-marca");
            if(e.options[e.selectedIndex].id == 0) 
            {
                alert('Debe seleccionar Marca');
                e.focus(); 
                return
            }    
            text = text + '&MARCA=' + e.options[e.selectedIndex].id;
                
            var e = document.getElementById("stacked-modelo");
            if(e.options[e.selectedIndex].id == 0) 
            {
                alert('Debe seleccionar Modelo');
                e.focus(); 
                return
            }    
            text = text + '&MODELO=' + e.options[e.selectedIndex].id;
        }    
            
        var e = document.getElementById("stacked-siniestro");
            text = text + '&SINIESTRO=' + e.value;
        
        var e = document.getElementById("stacked-perito");
        if(e.value.trim() === "" && isMoto=="915") 
            {
                alert('Debe escribir el nombre del Perito');
                e.focus(); 
                return
            }  
        text = text + '&PERITO=' + e.value;
            
        var e = document.getElementById("stacked-valorperito");
        if(e.value.trim() === "" && isMoto=="915") 
            {
                alert('Debe escribir el valor');
                e.focus(); 
                return
            } 
        text = text + '&VALORPERITO=' + e.value;            
        
        if (document.getElementById('lateral_chk').checked == 0 &&
            document.getElementById('trasero_chk').checked == 0  &&
            document.getElementById('frente_chk').checked  == 0  &&
            isMoto!="915"){
                alert('Debe seleccionar elementos de lateral o trasero');
                return
        }
        
        if (document.getElementById('frente_chk').checked){
            var e=(document.getElementById('FRT_CAM_DER_CAPOT').checked==true)?1:0;
            var frente=e + '-'; 
            e=(document.getElementById('FRT_REP_DER_CAPOT').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_DER_FARITO').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_IZQ_FARITO').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_DER_FARO').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_IZQ_FARO').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_DER_FARO_AUXILIAR').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_IZQ_FARO_AUXILIAR').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_DER_FRENTE').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_REP_DER_FRENTE').checked==true)?1:0;
            frente+= e + '-';
            e= (document.getElementById('FRT_CAM_DER_GUARDABARRO').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_REP_DER_GUARDABARRO').checked==true)?1:0;
            frente+= e + '-';
            e= (document.getElementById('FRT_CAM_IZQ_GUARDABARRO').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_REP_IZQ_GUARDABARRO').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_DER_PARABRISAS').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_DER_PARAGOLPE_ALMA').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_REP_PARAGOLPE_ALMA').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_DER_PARAGOLPE_CTRO').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_REP_DER_PARAGOLPE_CTRO').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_DER_PARAGOLPE_REJILLA').checked==true)?1:0;
            frente+= e + '-';
            e=(document.getElementById('FRT_CAM_DER_REJILLA_RADIADOR').checked==true)?1:0;
            frente+= e;   
            text = text + '&FRENTE=' + frente;  
        }
        else{
            text = text + '&FRENTE=0';
        } 
        if (document.getElementById('lateral_chk').checked){ 
            var e=(document.getElementById('LAT_CAM_DER_CRISTAL_DEL').checked==true)?1:0;
            var lateral=e + '-'; 
            e=(document.getElementById('LAT_CAM_IZQ_CRISTAL_DEL').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_DER_CRISTAL_TRA').checked==true)?1:0;
            lateral+= e + '-';  
            e=(document.getElementById('LAT_CAM_IZQ_CRISTAL_TRA').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_DER_ESPEJO_ELEC').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_IZQ_ESPEJO_ELEC').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_IZQ_ESPEJO_MAN').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_DER_ESPEJO_MAN').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_DER_MANIJA_DEL').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_IZQ_MANIJA_DEL').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_DER_MANIJA_TRA').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_IZQ_MANIJA_TRA').checked==true)?1:0;
            lateral+= e + '-';
            e= (document.getElementById('LAT_CAM_DER_MOLDURA_DEL').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_IZQ_MOLDURA_DEL').checked==true)?1:0;
            lateral+= e + '-';
            e= (document.getElementById('LAT_CAM_DER_MOLDURA_TRA').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_IZQ_MOLDURA_TRA').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_DER_PUERTA_DEL').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_IZQ_PUERTA_DEL').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_DER_PUERTA_TRA').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_IZQ_PUERTA_TRA').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_REP_DER_PUERTA_DEL_PANEL').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_REP_IZQ_PUERTA_DEL_PANEL').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_REP_DER_PUERTA_TRA_PANEL').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_REP_IZQ_PUERTA_TRA_PANEL').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_DER_ZOCALO').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_REP_DER_ZOCALO').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_IZQ_ZOCALO').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_REP_IZQ_ZOCALO').checked==true)?1:0;
            lateral+= e;   
            text = text + '&LATERAL=' + lateral;                                                                        
        }
        else{
            text = text + '&LATERAL=0';
        }    
        if (document.getElementById('trasero_chk').checked){ 
            var e=(document.getElementById('TRA_CAM_DER_BAUL').checked==true)?1:0;
            var trasero=e + '-';
            e=(document.getElementById('TRA_REP_DER_BAUL').checked==true)?1:0;
            trasero+=e + '-'; 
            e=(document.getElementById('TRA_CAM_DER_FARO_EXT').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_CAM_IZQ_FARO_EXT').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_CAM_DER_FARO_INT').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_CAM_IZQ_FARO_INT').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_CAM_DER_GUARDABARRO').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_REP_DER_GUARDABARRO').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_CAM_IZQ_GUARDABARRO').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_REP_IZQ_GUARDABARRO').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_CAM_DER_LUNETA').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_CAM_DER_MOLDURA').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_CAM_DER_PANELCOLA').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_REP_DER_PANELCOLA').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_CAM_DER_PARAGOLPE').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_REP_DER_PARAGOLPE').checked==true)?1:0;
            trasero+= e;
            text = text + '&TRASERO=' + trasero;
        }
        else{
            text = text + '&TRASERO=0';
        }
        sendSearch(text);
    }
    function sendSearch(bfSearch) {
        let xhr = new XMLHttpRequest();
        let url = "/search?" + bfSearch;
        //var e = document.getElementById("HiddenData");
        //    e.value = bfSearch;
        xhr.open("POST", url, true);
        xhr.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var e = document.getElementById("CostBrief");
                    e.innerHTML = this.responseText; 
                    document.getElementById("descargar").disabled = false;
                    //e.disabled = false;
            }
        }
        xhr.send();
    }   
    function fnGetClase(){
        var e = document.getElementById("stacked-clase");
        var bfClase = e.options[e.selectedIndex].id;
        
        if (bfClase =="915")
           {
           var e = document.getElementById("stacked-marca");
           e.selectedIndex = 0;
           var e = document.getElementById("stacked-modelo");
           e.selectedIndex = 0;
           
           setTimeout(() => {document.getElementById("stacked-perito").focus();}, 100);
           }
        else    
           runClase(bfClase);

    }
    function runClase(bfClase) {
       let xhr = new XMLHttpRequest();
  
        let url = '/vh?CLASE=' + bfClase ;
        xhr.open("POST", url, true);
     
        xhr.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var e = document.getElementById("stacked-marca");
                options = [];
                options.push(this.responseText);
                e.innerHTML = options; 
            }
        }
        xhr.send();
    }     
    function fnGetModelo(){
        var e = document.getElementById("stacked-clase");
        var bfClase = e.options[e.selectedIndex].id;
            if(bfClase==0){
                alert("Se debe cargar la 'CLASE'");
                document.getElementById("stacked-clase").focus();
                document.getElementById("stacked-marca").selectedIndex = 0;
                return;
                }
        var e = document.getElementById("stacked-marca");
        var bfMarca = e.options[e.selectedIndex].id;

        runModelo(bfClase, bfMarca);
    }  
    function runModelo(bfClase, bfMarca) {
       let xhr = new XMLHttpRequest();
  
        let url = '/modelo?CLASE=' + bfClase + '&MARCA=' + bfMarca ;
        xhr.open("POST", url, true);
     
        xhr.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var e = document.getElementById("stacked-modelo");
                options = [];
                options.push(this.responseText);
                e.selectedIndex = 0;
                e.style.width = "250px";
                e.innerHTML = options; 
            }
        }
        xhr.send();
    }  
    function fnGetDetail() {
        
        var e = document.getElementById("HiddenData");
        let bfSearch = String(e.value);
        
        let xhr = new XMLHttpRequest();
        let url =  '/searchcomplete?' + bfSearch;
        console.log(url);
        xhr.open("POST", url, true);
     
        xhr.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var e =  document.documentElement;
                    e.innerHTML = this.responseText; 
            }
        }
        xhr.send();    
    }    
    function fnRtnSearch() {
        let xhr = new XMLHttpRequest();
        let url = "/consulta";

        xhr.open("get", url, true);
        xhr.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var e =  document.documentElement;
                    e.innerHTML = this.responseText; 
            }
        }
        xhr.send();
    }
    function viewGrid(objRef, elementID){
        if(objRef.checked == 1){
            document.getElementById(elementID).style.display = ""; 
            document.getElementById(elementID+'_repara').innerText = "Derecho"; 
            document.getElementById(elementID+'_repara').style.width = "25px";
            document.getElementById(elementID+'_repara').style.textAlign = "center";
            document.getElementById(elementID+'_cambia').innerText = "Izquierdo"; 
            document.getElementById(elementID+'_cambia').style.width = "25px";
            document.getElementById(elementID+'_cambia').style.textAlign = "center";
        }else{
            document.getElementById(elementID).style.display = "none";
            document.getElementById(elementID+'_repara').innerText = ""; 
            document.getElementById(elementID+'_repara').style.width = "35px";
            document.getElementById(elementID+'_cambia').innerText = ""; 
            document.getElementById(elementID+'_cambia').style.width = "35px";
        }
    }
    function checkLength(el) {
        let bfField = el.value;
        bfField = bfField.trim();
        if (bfField.length != 11 & bfField.length != 0) {
           alert("La longitud del campo siniestro es de 11 dígitos o cambo vacio");
           el.value = "";
           el.focus();
           return false;
        }
        if (bfField.length == 11) {
            const regex = /^[0-9]{11}$/;
            if (!regex.test(bfField)){    
                alert("Solo se deben ingresar números");
                el.value = "";
                el.focus();
                return false;
            }
            const primerDigito = bfField[0];
            const todosIguales = bfField.split('').every(digito => digito === primerDigito);
            if (todosIguales) {
               alert('Número de siniestro no válido'); 
               el.value = "";
               el.focus();
               return false;
            }
        }
        return true;
    }
    function unCheckOps(elNamePos, elName) {
        if (document.getElementById(elNamePos).checked){ 
            document.getElementById(elName).checked=false; 
        }
    }   
    
    function procesarDivParaImprimir(divRecibido, cDia, cHora, cElementos) {
        if (!(divRecibido instanceof HTMLElement)) {
            console.error("Error: El argumento debe ser un elemento HTML div.");
            return '';
        }
        const bfCliente = divRecibido.querySelector('#stacked-cliente')?.value || '';
        const bfClase = divRecibido.querySelector('#stacked-clase')?.value || '';
        const bfMarca = divRecibido.querySelector('#stacked-marca')?.value || '';
        const bfModelo = divRecibido.querySelector('#stacked-modelo')?.value || '';
        const bfSiniestro = divRecibido.querySelector('#stacked-siniestro')?.value || '';
        const bfPerito = divRecibido.querySelector('#stacked-perito')?.value || '';
        
        const spanExterior  = document.getElementById('CostBrief');
        valorLimpio = '';
        if (spanExterior ) {
            const spanInterior = spanExterior.querySelector('#CostBrief'); 
            if (spanInterior) {
                const textoCompleto = spanInterior.textContent;
                const valorNumerico = textoCompleto.split('$')[1]; 
                valorLimpio = valorNumerico ? valorNumerico.trim() : ''; 
            }    
        }    
        
        const formato =`
        <table style="border-collapse: collapse;">
            <thead>
                <tr>
                    <th colspan="3" style="padding-bottom: 20px;">Detalle de Siniestro</th>
                </tr>
                <tr>
                    <th>Dia</th>
                    <th>Hora</th>
                    <th>Monto Sugerido</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><input type="text" placeholder="${cDia}" style="text-align: center;"></td>
                    <td><input type="text" placeholder="${cHora}" style="text-align: center;"></td>
                    <td><input type="text" placeholder="${valorLimpio}" style="text-align: center;"></td>
                </tr>
                <tr>
                    <th style="padding-top: 10px;">Tipo Cliente</th>
                    <th style="padding-top: 10px;">Tipo Vehículo</th>
                    <th style="padding-top: 10px;">Marca</th>
                </tr>
                <tr>
                    <td><input type="text" placeholder="${bfCliente}" style="text-align:center;"></td>
                    <td><input type="text" placeholder="${bfClase}" style="text-align:center;"></td>
                    <td><input type="text" placeholder="${bfMarca}" style="text-align:center;"></td>
                </tr>
            </tbody>
            <tfoot>
                <tr>
                    <th style="padding-top: 10px;">Modelo</th>
                    <th style="padding-top: 10px;">Siniestro</th>
                    <th style="padding-top: 10px;">Perito</th>
                </tr>
                <tr>
                    <td><input type="text" placeholder="${bfModelo}" style="text-align:center;"></td>
                    <td><input type="text" placeholder="${bfSiniestro}" style="text-align:center;"></td>
                    <td><input type="text" placeholder="${bfPerito}" style="text-align:center;"></td>
                </tr>
            </tfoot>
        </table>
        <p>${cElementos}</p>
        `;   
        return formato;
        }    
        
        function obtenerYFormatearFechaHoraActual() {
            const ahora = new Date();

            const año = ahora.getFullYear();
            const mes = String(ahora.getMonth() + 1).padStart(2, '0'); // Meses van de 0 a 11
            const dia = String(ahora.getDate()).padStart(2, '0');
            const hora = String(ahora.getHours()).padStart(2, '0');
            const minuto = String(ahora.getMinutes()).padStart(2, '0');
            const segundo = String(ahora.getSeconds()).padStart(2, '0');

            const formatoCompleto = `${año}-${mes}-${dia}H${hora}_${minuto}_${segundo}`;
            const diaSeparado = `${año}-${mes}-${dia}`;
            const horaSeparada = `${hora}:${minuto}:${segundo}`;

            return {
                formatoCompleto: formatoCompleto,
                diaSeparado: diaSeparado,
                horaSeparada: horaSeparada
            };
            } 
   </script>
 </html>            
 """