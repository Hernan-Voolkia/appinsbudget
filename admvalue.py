import param
bfHTML = """
<html>
  <head>
    <meta http-equiv="cache-control" content="max-age=0" />
    <meta http-equiv="cache-control" content="no-cache" />
    <meta http-equiv="expires" content="0" />
    <meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />
    <meta http-equiv="pragma" content="no-cache" />  
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/pure-min.css" integrity="sha384-X38yfunGUhNzHpBaEBsWLO+A0HDYOQi8ufWDkZ0k9e0eXz/tH3II7uKZ9msv++Ls" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/grids-responsive-min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link id="favicon" rel="icon" type="image/x-icon" href="/img/favicon.ico">
    <link href='http://fonts.cdnfonts.com/css/helvetica-neue-9' rel='stylesheet' type='text/css'>
    <title>App Presupuesto</title>
    <style>
        body {background-color:rgb(255,255,255);}
        label {text-align:right;font-family:'helvetica neue';font-size: 100%;}
        .vertical-text {
            writing-mode: vertical-rl; /* Texto vertical de derecha a izquierda */
            transform: rotate(180deg); /* Opcional: rota 180 grados para cambiar la dirección */
        }
    </style>
</head>
<body>
    <div id="divContent" class="pure-g" style="text-align:center;"><div class="pure-u-*">&nbsp;</div></div>
    <div class="pure-g" style="padding-left:5px;">
        <div class="pure-u-1 pure-u-md-7-24"> <!--<div class="pure-u-1 pure-u-md-1-5">-->
            &nbsp;
        </div>
        <div class="pure-u-1 pure-u-md-7-24">
            <div class="pure-menu pure-menu-horizontal">
                <!--<a href="#" id="btnConsulta" class="pure-menu-link pure-menu-heading">Consulta</a>-->
                <ul class="pure-menu-list">
                    <li class="pure-menu-item">
                        <a href="#" id="btnConsulta" class="pure-menu-link">Consulta</a>
                    </li>
                    <li class="pure-menu-item">
                        <a href="#" id="btnHistorial" class="pure-menu-link">Historial</a>
                    </li>
                    <li class="pure-menu-item pure-menu-selected">
                        <a href="#" id="btnParams" class="pure-menu-link">Params</a>
                    </li>
                    <li class="pure-menu-item pure-menu-has-children pure-menu-allow-hover">
                        <a href="#" id="menuLink1" class="pure-menu-link">Repuestos</a>
                        <ul class="pure-menu-children">
                            <li class="pure-menu-item"></li>
                                <a href="#" id="btnDelantero" class="pure-menu-link">Delantero</a>
                            </li>
                            <li class="pure-menu-item">
                                <a href="#" id="btnLateral" class="pure-menu-link">Lateral</a>
                            </li>
                            <li class="pure-menu-item">
                                <a href="#" id="btnTrasero" class="pure-menu-link">Trasero</a>
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </div>      
    <div class="pure-g" style="padding-left:5px;">
        <div class="pure-u-1 pure-u-md-7-24"> <!--<div class="pure-u-1 pure-u-md-1-5">-->
            <img src="./img/Pos_color_RGB.jpg" alt="logo" width="128" height="128"
                 style="margin-left:auto;margin-right:auto;display:block;"/>
            <p>&nbsp;</p>
            <p class="vertical-text"
                style="margin-left:auto;margin-right:auto;display:block;
                       font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                       color:#005993;text-align:left; font-size: 20px;" >Parámetros</p>             
        </div> 
        <div class="pure-u-1 pure-u-md-7-24"> <!--<div class="pure-u-1 pure-u-md-3-5">-->
            <form class="pure-form pure-form-stacked">
                <fieldset>
                    <div class="pure-control-group">
                        <label for="stacked-Asegurado" style="color:#005993;text-align:left;">Asegurado</label>
                        <input type="text" id="stacked-Asegurado" style="min-width:343px;" value="rplBfAsegurado" onblur="validarCampoDecimal(this)"/>
                    </div>
                    <div class="pure-control-group">
                        <label for="stacked-AseguradoTercero" style="color:#005993;text-align:left;">Tercero</label>
                        <input type="text" id="stacked-Tercero" style="min-width:343px;" value="rplBfTercero" onblur="validarCampoDecimal(this)"/>
                    </div>
                    <div class="pure-control-group">
                        <label for="stacked-MObra" style="color:#005993;text-align:left;">Mano de Obra</label>
                        <input type="text" id="stacked-MObra" style="min-width:343px;" value="rplBfMObra" onblur="validarCampoDecimal(this)"/>
                    </div>
                    <div class="pure-control-group">
                        <label for="stacked-MOMinimo" style="color:#005993;text-align:left;">Mano de Obra Minimo</label>
                        <input type="text" id="stacked-MOMinimo" style="min-width:343px;" value="rplBfMOMinimo" onblur="validarCampoDecimal(this)"/>
                    </div>
                    <div class="pure-control-group">
                        <label for="stacked-Pintura" style="color:#005993;text-align:left;">Pintura</label>
                        <input type="text" id="stacked-Pintura" style="min-width:343px;" value="rplBfPintura" onblur="validarCampoDecimal(this)"/>
                    </div>
                    <div class="pure-control-group">
                        <label for="stacked-Ajuste" style="color:#005993;text-align:left;">Ajuste</label>
                        <input type="text" id="stacked-Ajuste" style="min-width:343px;" value="rplBfAjuste" onblur="validarCampoDecimal(this)"/>
                    </div>
               </fieldset>
                <br style="display: block;content:'';margin-top:5;">
                <span id="CostBrief" class="pure-form-message-inline" style="padding-left:3px;text-align:left;font-family:'helvetica neue';font-size:100%;color:rgb(170,27,23);">&nbsp;&nbsp;</span>
            </form>
        </div> 
    </div>     
    <div class="pure-g" style="padding-left:5px;">
        <div class="pure-u-1 pure-u-md-7-24">
        </div> 
        <div class="pure-u-1 pure-u-md-7-24">
            <div class="pure-controls" style="padding-left:3px;">
                <button style="background-color:#005993;color:#ffffff;" class="pure-button pure-button-primary" onclick="fnSaveData()">&nbsp;&nbsp;&nbsp;Grabar&nbsp;&nbsp;&nbsp;</button>
            </div>
        </div>
        <div class="pure-u-1 pure-u-md-7-24"></div>
    </div> 
    <br style="display: block;content:'';margin-top:5;">    
   </body>
   <script>
    document.getElementById("btnConsulta").addEventListener("click", function(event) {
        event.preventDefault(); 
        window.location.href =  "/consulta"; 
    });
    document.getElementById("btnHistorial").addEventListener("click", function(event) {
        event.preventDefault(); 
        window.location.href =  "/dbread"; 
    });
    document.getElementById("btnParams").addEventListener("click", function(event) {
        event.preventDefault(); 
        window.location.href =  "/admvalue"; 
    });
    document.getElementById("btnLateral").addEventListener("click", function(event) {
        event.preventDefault(); 
        window.location.href =  "/admreplat"; 
    });
    document.getElementById("btnTrasero").addEventListener("click", function(event) {
        event.preventDefault(); 
        window.location.href =  "/admreptra"; 
    });
    
    function validarNumeroDecimal(cadena) {
        // Expresión regular para validar números decimales con hasta dos decimales
        const regexDecimal = /^[+-]?\d+([.,]\d{1,2})?$/;
            
        // Testea la cadena con la expresión regular
        return regexDecimal.test(cadena);
    }
    function validarCampoDecimal(input) {
        const valor = input.value;
        const esValido = validarNumeroDecimal(valor);

        if (!esValido) {
            alert("Número decimal inválido. Debe tener hasta dos decimales y usar punto o coma como separador");
            input.value = "";
        } 
    }
    function fnSaveData(){
        var e = document.getElementById("stacked-Asegurado");
        var text = 'ASEGURADO=' + e.value;
        
        var e = document.getElementById("stacked-Tercero");
        text = text + '&TERCERO=' + e.value;
            
        var e = document.getElementById("stacked-MObra");
        text = text + '&MOBRA=' + e.value;

        var e = document.getElementById("stacked-MOMinimo");
        text = text + '&MOMINIMO=' + e.value;

        var e = document.getElementById("stacked-Pintura");
        text = text + '&PINTURA=' + e.value;

        var e = document.getElementById("stacked-Ajuste");
        text = text + '&AJUSTE=' + e.value;
        
        sendSearch(text);

    }
    function sendSearch(bfSearch) {
        let xhr = new XMLHttpRequest();
        let url = "/admvaluesave?" + bfSearch;
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
    </script>
 </html>    
        
 """
