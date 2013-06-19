var t_sectores = null,
    t_segmentos = null,
    t_fotos = null,
    t_registros = null;

function actualiza_storage(obj)
{
  switch(obj.nombre)
    {
      case "sector": delete localStorage.t_sectores; localStorage.t_sectores = JSON.stringify(obj.filas); break;
      case "segmento": delete localStorage.t_segmentos; localStorage.t_segmentos = JSON.stringify(obj.filas); break;
      case "foto": delete localStorage.t_fotos; localStorage.t_fotos = JSON.stringify(obj.filas); break;
      case "registro": delete localStorage.t_registros; localStorage.t_registros = JSON.stringify(obj.filas); break;
    }
}

function cargar_desde_localstorage()
{
  var data = {};
  var tables = ["sectores", "segmentos", "fotos", "registros"];
  for (var key in tables)
  {
    if (localStorage["t_"+tables[key]] !== undefined)
    {
      data[tables[key]] = JSON.parse(localStorage["t_"+tables[key]]);
      for (var i = 0; i < data[tables[key]].length; i++)
      {
        window["t_"+tables[key]].agregaFilaObjeto(data[tables[key]][i]);
      }
    }
    localStorage["t_"+tables[key]] = JSON.stringify(window["t_"+tables[key]].filas);
  }

  if (localStorage["descripcion"] !== undefined)
  {
    $("#descripcion").val(localStorage["descripcion"]);
  }
}

var filaAgregada = function(dato)
{
    $("#select_"+this.nombre).append("<option value='"+dato[0]+"'>"+dato[1]+"</option>");
    actualiza_storage(this);
};
var filaEliminada = function(dato)
{
  
    $("#select_"+this.nombre).find("option[value='"+dato[0]+"']").remove();
    actualiza_storage(this);
};

function guardar()
{
  var predet = localStorage.nombre !== undefined ? localStorage.nombre : "";
  var nombre = prompt("Indique un nombre para el evento: ", predet);
  if (!nombre || nombre == null) return;
  localStorage.nombre = nombre;
  $.post("/guardaEvento", localStorage, function(response)
  {
    if (response == "success")
    {
      alert("Datos guardados.");
      location.reload();
    }
  });
}
function blanquear(confirmado)
{
  if ((confirmado !== undefined && confirmado) || confirm("¿Crear un evento nuevo? Se perderán los cambios no guardados."))
  {
    var tables = ["sectores", "segmentos", "fotos", "registros"];
    for (key in tables)
      window["t_"+tables[key]].truncar();
    $("#descripcion").val("");
    localStorage.descripcion = "";
  }
}

function cargar(evento)
{
  $.get("/cargaEvento", {archivo: evento}, function(data)
  {
    if (data == "failure")
    {
      alert("Error al intentar cargar el archivo.");
      return;
    }

    blanquear(true);

    for (x in data)
    {
      localStorage[x] = data[x];
    }
    delete x;

    cargar_desde_localstorage();

    $("a[data-archivo]").each(function()
    {
      if ($(this).attr("data-archivo") == evento)
      {
        $(this).removeClass("loader").addClass("muted");
        $(this).find("i").removeClass("icon-folder-close").addClass("icon-folder-open");
      }
      else
      {
        $(this).removeClass("muted").addClass("loader");
        $(this).find("i").removeClass("icon-folder-open").addClass("icon-folder-close"); 
      }
    });
  });
}
$(function()
{
  t_sectores = new Tabla("#sectores",["Codigo", "Etiqueta"], "sector", true);
  t_segmentos = new Tabla("#segmentos", ["Codigo", "Etiqueta"], "segmento", true);
  t_fotos = new Tabla("#fotos", ["Foto", "Etiqueta"], "foto", true);
  t_registros = new Tabla("#registros", ["Sector", "Segmento", "Entradas", "Foto"], "registro");


  t_sectores.obtenerDatos = function()
  {
    var codigo = prompt("Codigo del sector:");
    var sector = prompt("Nombre del sector:");
    if (!codigo || codigo == null) return null;
    if (!sector || sector == null) return null;
    if (t_sectores.mapear(codigo) !== null)
    {
      alert("El código ya está en uso. ("+codigo+")");
      return;
    }
    return [codigo, sector];
  };

  t_segmentos.obtenerDatos = function()
  {
    var codigo = prompt("Codigo del segmento:");
    var seg = prompt("Nombre del segmento:");
    if (!seg || seg == null) return null;
    if (!codigo || codigo == null) return null;
    if (t_segmentos.mapear(codigo) !== null)
    {
      alert("El código ya está en uso. ("+codigo+")");
      return;
    }
    return [codigo, seg];
  };

  t_sectores.filaAgregada = filaAgregada;
  t_segmentos.filaAgregada = filaAgregada;
  t_fotos.filaAgregada = filaAgregada;

  t_sectores.filaEliminada = filaEliminada;
  t_segmentos.filaEliminada = filaEliminada;
  t_fotos.filaEliminada = filaEliminada;

  t_registros.filaAgregada = function(dato) { actualiza_storage(this); };
  t_registros.filaEliminada = function(dato) { actualiza_storage(this); };

  t_fotos.obtenerDatos = function()
  {
    var file_form = $("#hiddendiv").find("input[type='file']");
    file_form.click();
    file_form.one("change",function()
    {
         var etiqueta = prompt("Etiqueta de la foto:");
         if (!etiqueta || etiqueta == null) return;
         $("#hiddenform input[name='etiqueta']").val(etiqueta);
         $("#hiddenform").submit();
    });
    return null;
  };
  t_fotos.formatea = function(columna, valor)
  {
    switch(columna)
    {
      case "Etiqueta": return valor;
      case "Foto": return "<img src='" + valor + "' />";
    }
  };

  function mapear(valor)
  {
    for (var i = 0; i < this.filas.length; i++)
    {
      if (this.filas[i]["Codigo"] == valor)
      {
        return this.filas[i]["Etiqueta"];
      }
    }
    return null;
  }

  t_sectores.mapear = mapear;
  t_segmentos.mapear = mapear;

  t_registros.mapear = function(valor)
  {
    // se espera un par
    for (var i = 0; i < this.filas.length; i++)
    {
      if (this.filas[i]["Sector"] == valor[0] && this.filas[i]["Segmento"] == valor[1])
      {
        return {
          "Entradas": this.filas[i]["Entradas"],
          "Foto": this.filas[i]["Foto"]
        };
      }
    }
    return null;

  }

  t_registros.formatea = function(columna, valor)
  {
    switch(columna)
    {
      case "Foto": return "<img src='" + valor + "' />";
      case "Sector": return t_sectores.mapear(valor);
      case "Segmento": return t_segmentos.mapear(valor);
    }
    return valor;
  }

  $("#button_add").click(function()
  {
    var sec = $("#select_sector").val();
    var seg = $("#select_segmento").val();
    var fot = $("#select_foto").val();
    var ent = $("#select_entradas").val();

    if (sec == "null" || seg == "null" || fot == "null" || ent.length == 0)
    {
      alert("Complete todos los datos para agregar el registro.");
      return;
    }
    if (!parseInt(ent) || ent < 1)
    {
      alert("La cantidad de entradas debe ser un número entero positivo, mayor a cero.");
      return;
    }
    if (t_registros.mapear([sec,seg]) !== null)
    {
      alert("Esta entrada ("+t_sectores.mapear(sec)+","+t_segmentos.mapear(seg)+") ya existe.");
      return;
    }
    t_registros.agregaFila([sec,seg,ent,fot]);
  });
  
  
  cargar_desde_localstorage();

  localStorage["descripcion"] = $("#descripcion").val();

  $("#descripcion").change(function()
  {
    localStorage["descripcion"] = $(this).val();
  })

  $(".loader").click(function()
  {
    if ($(this).hasClass("muted")) return;
    var archivo = $(this).attr("data-archivo");
    cargar(archivo);
  });

  $(".saver").click(function()
  {
    guardar();
  });

  $(".new").click(function()
  {
    blanquear();
  });
});
