bfHTML = """
<html>
  <head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/pure-min.css" integrity="sha384-X38yfunGUhNzHpBaEBsWLO+A0HDYOQi8ufWDkZ0k9e0eXz/tH3II7uKZ9msv++Ls" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/grids-responsive-min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link id="favicon" rel="icon" type="image/x-icon" href="/img/favicon.ico">
    <link href='http://fonts.cdnfonts.com/css/helvetica-neue-9' rel='stylesheet' type='text/css'>
    <title>App Presupuesto</title>
    <style>
        body {background-color:rgb(255,255,255);}
        label {text-align:right;font-family:'helvetica neue';font-size: 100%;}
    </style>
    </style>
    </style>
    </style>
    </style>
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
    <div class="pure-g" style="justify-content: center;">
        <div class="pure-u-1 pure-u-md-1-5">
            <img src="./img/Pos_color_RGB.jpg" alt="logo" width="128" height="128"/>
        </div> 
        <div class="pure-u-1 pure-u-md-3-5">
            <form class="pure-form pure-form-aligned">
                <fieldset>
                    <div class="pure-control-group" style="min-width:250px;">
                        <label for="aligned-name" style="color:#005993;">Cliente</label>
                        <select id="stacked-cliente" style="min-width:250px;">
                            <option id=0></option>
                            <option id=1>ASEGURADO</option>
                            <option id=2 selected>TERCERO</option>
                        </select>
                    </div>
                    <div class="pure-control-group">
                        <label for="aligned-name" style="color:#005993;">Clase</label>
                        <select id="stacked-clase" style="min-width:250px;" onchange="fnGetClase()">
                            <option id=0></option>
                            <option id=901>SEDAN</option>
                            <option id=907>SUV</option>
                        </select>
                    </div>
                    <div class="pure-control-group">
                        <label for="aligned-name" style="color:#005993;">Marca</label>
                        <select id="stacked-marca" style="min-width:250px;max-width:255px;" onchange="fnGetModelo()">
                            <option id=0></option>
                        </select>
                    </div>
                    <div class="pure-control-group">
                        <label for="aligned-name" style="color:#005993;">Modelo</label>
                        <select id="stacked-modelo" style="min-width:250px;">
                            <option id=0></option>
                        </select>
                    </div>
                    <div class="pure-control-group"  style="color:#005993;">
                        <label for="aligned-name">Siniestro</label>
                        <input type="email" id="stacked-siniestro" placeholder="" style="min-width:250px;" onblur="checkLength(this)"/>
                    </div>
               </fieldset>
            </form>
        </div> 
    </div>     
    <div class="pure-g">
        <div class="pure-u-3-8">
        </div> 
        <div class="pure-u-3-8">
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
                        <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Espejo</td>
                        <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_ESPEJO"/></td>
                        <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_ESPEJO"/></td>
                        <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                    </tr>
                    <tr>
                        <td style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:3px;padding-top:5px;">Moldura</td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_DER_MOLDURA"/></td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_CAM_IZQ_MOLDURA"/></td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
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
                        <td style="background-color:#FFFFFF;color:#000000;padding-left:5px;padding-right:3px;padding-bottom:3px;padding-top:5px;">Puerta Panel Tras</td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_REP_DER_PUERTA_TRA_PANEL"/></td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="LAT_REP_IZQ_PUERTA_TRA_PANEL"/></td>
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
        </div>                        
        <div class="pure-u-3-8">
        </div>
    </div>  
    <br style="display: block;content:'';margin-top:5;">
    <div class="pure-g">
        <div class="pure-u-3-8">
        </div> 
        <div class="pure-u-3-8">
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
                        <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Baul/Portón</td>
                        <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_BAUL"/></td>
                        <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                    </tr>
                    <tr>
                        <td style="padding-left:5px;padding-right:5px;padding-bottom:3px;padding-top:3px;background-color:#FFFFFF;color:#000000;">Faro</td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_FARO"/></td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_IZQ_FARO"/></td>
                        <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                    </tr>
                    <tr>
                        <td style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Guardabarro</td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_GUARDABARRO" onclick="unCheckOps('TRA_CAM_DER_GUARDABARRO','TRA_REP_DER_GUARDABARRO')"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_REP_DER_GUARDABARRO" onclick="unCheckOps('TRA_REP_DER_GUARDABARRO','TRA_CAM_DER_GUARDABARRO')"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_IZQ_GUARDABARRO" onclick="unCheckOps('TRA_CAM_IZQ_GUARDABARRO','TRA_REP_IZQ_GUARDABARRO')"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_REP_IZQ_GUARDABARRO" onclick="unCheckOps('TRA_REP_IZQ_GUARDABARRO','TRA_CAM_IZQ_GUARDABARRO')"/></td>
                        </tr>
                        <tr>
                            <td style="padding-left:5px;padding-right:5px;padding-bottom:3px;padding-top:3px;background-color:#FFFFFF;color:#000000;">Luneta</td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_LUNETA"/></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Moldura</td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_MOLDURA"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td class="pure-table-odd" style="background-color:#FFFFFF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Panel Cola</td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_PANELCOLA" onclick="unCheckOps('TRA_CAM_DER_PANELCOLA','TRA_REP_DER_PANELCOLA')"/></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_REP_DER_PANELCOLA" onclick="unCheckOps('TRA_REP_DER_PANELCOLA','TRA_CAM_DER_PANELCOLA')"/></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#FFFFFF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                        <tr>
                            <td style="background-color:#DEF3FF;color:#000000;padding-left:3px;padding-right:3px;padding-bottom:5px;padding-top:5px;">Paragolpe</td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_CAM_DER_PARAGOLPE" onclick="unCheckOps('TRA_CAM_DER_PARAGOLPE','TRA_REP_DER_PARAGOLPE')"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"><input type="checkbox" id="TRA_REP_DER_PARAGOLPE" onclick="unCheckOps('TRA_REP_DER_PARAGOLPE','TRA_CAM_DER_PARAGOLPE')"/></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                            <td style="background-color:#DEF3FF;color:#000000;padding-bottom:5px;padding-top:5px;text-align:center;"></td>
                        </tr>
                    </tbody>
                </table>
        </div>
        <div class="pure-u-3-8">
        </div>
    </div>       
   <div class="pure-g">
        <div class="pure-u-3-8">
        </div> 
        <div class="pure-u-3-8">
            <span id="CostBrief" class="pure-form-message-inline" style=\"text-align:right; font-family:'helvetica neue';font-size:100%;\">&nbsp;&nbsp;</span>
        </div>
        <div class="pure-u-3-8">
        </div>
    </div>       
    <div class="pure-g" style="justify-content: center;">
        <div class="pure-u-1 pure-u-md-2-5">
            &nbsp;
        </div> 
        <div class="pure-u-1 pure-u-md-3-5">
            <div class="pure-controls"><input type="hidden" id="HiddenData" value="">&nbsp;</div>
            <div class="pure-controls" style="justify-content: center;">
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   
                <button style="background-color:#005993;color:#ffffff;" class="pure-button pure-button-primary" onclick="fnGetData()">Consultar</button>
                <button style="background-color:#005993;color:#ffffff;" class="pure-button pure-button-primary"  onclick="fnClean()">&nbsp;&nbsp;Limpiar&nbsp;&nbsp;</button>
            </div>
        </div>
    </div>     
    <div class="pure-g" style="justify-content: center;">
        <div class="pure-u-1 pure-u-md-2-5">
            &nbsp;
        </div> 
        <div class="pure-u-1 pure-u-md-3-5">
            &nbsp;
        </div>
    </div>     
   </body>
   <script>
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
            
        var e = document.getElementById("lateral_chk");
            e.checked = false;    
        var e = document.getElementById("lateral_repara");    
            e.checked = false; 
        var e = document.getElementById("lateral_cambia");
            e.checked = false; 
        
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
        var e = document.getElementById("LAT_CAM_DER_ESPEJO");
            e.checked = false;  
        var e = document.getElementById("LAT_CAM_IZQ_ESPEJO");
            e.checked = false;                   
        var e = document.getElementById("LAT_CAM_DER_MOLDURA");
            e.checked = false;       
        var e = document.getElementById("LAT_CAM_IZQ_MOLDURA");
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
        var e = document.getElementById("TRA_CAM_DER_FARO");    
            e.checked = false;    
        var e = document.getElementById("TRA_CAM_IZQ_FARO");
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
            e.innerHTML = '&nbsp;&nbsp;';
    }
    function fnGetData(){
        var e = document.getElementById("stacked-cliente");
        var text = 'CLIENTE=' + e.options[e.selectedIndex].id;
        var e = document.getElementById("stacked-clase");
            text = text + '&CLASE=' + e.options[e.selectedIndex].id;
        var e = document.getElementById("stacked-marca");
            text = text + '&MARCA=' + e.options[e.selectedIndex].id;
        var e = document.getElementById("stacked-modelo");
            text = text + '&MODELO=' + e.options[e.selectedIndex].id;
        var e = document.getElementById("stacked-siniestro");
            text = text + '&SINIESTRO=' + e.value;
        
        if (document.getElementById('lateral_chk').checked){ 
            var e=(document.getElementById('LAT_CAM_DER_CRISTAL_DEL').checked==true)?1:0;
            var lateral=e + '-'; 
            e=(document.getElementById('LAT_CAM_IZQ_CRISTAL_DEL').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_DER_CRISTAL_TRA').checked==true)?1:0;
            lateral+= e + '-';  
            e=(document.getElementById('LAT_CAM_IZQ_CRISTAL_TRA').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_DER_ESPEJO').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_IZQ_ESPEJO').checked==true)?1:0;
            lateral+= e + '-';
            e= (document.getElementById('LAT_CAM_DER_MOLDURA').checked==true)?1:0;
            lateral+= e + '-';
            e=(document.getElementById('LAT_CAM_IZQ_MOLDURA').checked==true)?1:0;
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
            e=(document.getElementById('TRA_CAM_DER_FARO').checked==true)?1:0;
            trasero+= e + '-';
            e=(document.getElementById('TRA_CAM_IZQ_FARO').checked==true)?1:0;
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
                    //e.disabled = false;
            }
        }
        xhr.send();
    }   
    function fnGetClase(){
        var e = document.getElementById("stacked-clase");
        var bfClase = e.options[e.selectedIndex].id;
        
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
   </script>
 </html>            
 """