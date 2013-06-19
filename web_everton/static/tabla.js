function Tabla(selector, columnas, nombre, agregador)
{
	this.nombre = nombre;
	this.selector = selector;
	this.columnas = columnas;
	this.filas = [];
	this.agregador = agregador !== undefined && agregador == true;
	var referencia = this;

	this.actualiza();


	return true;
}

Tabla.prototype.agregaFila = function(vals)
{
	var ref = this;
	if (this.filas.length == 0)
		this.nodo.find(".empty").remove();

	var vals_obj = {};
	for (var i = 0; i < vals.length; i++)
		vals_obj[this.columnas[i]] = vals[i];

	this.filas.push(vals_obj);

	this.actualiza();

	if (this.filaAgregada)
		this.filaAgregada(vals);

	
};

Tabla.prototype.formatea = function(columna, valor)
{
	return valor;
};

Tabla.prototype.eliminaFila = function(vals)
{
	
	var indice = this.buscar(vals);
	
	var fila = this.nodo.find("tbody tr").eq(indice);
	fila.remove();
	this.filas.splice(indice, 1);

	this.actualiza();

	if (this.filaEliminada)
		this.filaEliminada(vals);
	
}

Tabla.prototype.mapear = function(llave)
{
	return null;
};

Tabla.prototype.agregaFilaObjeto = function(obj)
{
	var fila = [];
	for (var i = 0; i < this.columnas.length; i++)
	{
		fila.push(obj[this.columnas[i]]);
	}
	this.agregaFila(fila);
};

Tabla.prototype.aObjeto = function(vals)
{
	var obj = {};
	for (var i = 0; i < this.columnas.length; i++)
	{
		obj[this.columnas[i]] = vals[i];
	}
	return obj;
};

Tabla.prototype.truncar = function()
{
	while(this.filas.length > 0)
	{
		this.eliminaFila(this.aArreglo(this.filas[0]));
	}
};

Tabla.prototype.aArreglo = function(obj)
{
	var fila = [];
	for (var i = 0; i < this.columnas.length; i++)
	{
		fila.push(obj[this.columnas[i]]);
	}
	return fila;
};

Tabla.prototype.buscar = function(vals)
{
	for (var i = 0; i < this.filas.length; i++)
	{
		var pass = true;
		for (var j = 0; j < this.columnas.length; j++)
		{
			console.log("Comparando " + this.filas[i][this.columnas[j]] + " con " + vals[j]);
			if (this.filas[i][this.columnas[j]] != vals[j])
			{
				pass = false;
				break;
			}
		}
		if (pass)
			return i;
	}
	return -1;
};

Tabla.prototype.actualiza = function()
{
	$(this.selector).html("");
	this.nodo = $("<table></table>");

	this.nodo.attr("class", "table table-bordered table-condensed");

	this.nodo.append("<thead><tr></tr></thead><tbody></tbody>");
	for (var x = 0; x < this.columnas.length; x++)
	{
		this.nodo.find("tr").append("<th>" + this.columnas[x] + "</th>");
	}
	this.nodo.find("tr").append("<th>&nbsp;</th>");

	if (this.filas.length == 0)
		this.nodo.find("tbody").append("<tr><td class='empty' colspan='" + (this.columnas.length + 1) + "'>Sin elementos.</td></tr>");
	$(this.selector).append(this.nodo);
	var ref = this;
	if (this.agregador)
	{
		$(this.selector).append("<p><button class='btn btn-primary agrega'><i class='icon-plus icon-white'></i></button></p>");
		$(this.selector).find(".agrega").click(function()
		{
			var datos = ref.obtenerDatos();
			if (!datos || datos == null) return;
			ref.agregaFila(datos);
		});
	}
	
	for (var ix = 0; ix < this.filas.length; ix++)
	{
		var vals_obj = this.filas[ix];
		var fila = $("<tr></tr>");
		for (var i = 0; i < this.columnas.length; i++)
		{
			fila.append("<td>" + this.formatea(this.columnas[i], vals_obj[this.columnas[i]]) + "</td>");
		}
		fila.append("<td><button class='btn btn-danger elimina' data-index='"+ix+"'><i class='icon-remove icon-white'></i></button></td>");
		this.nodo.find("tbody").append(fila);
	}
	this.nodo.find("button.elimina").click(function()
	{
		var idx = parseInt($(this).attr("data-index"));
		ref.eliminaFila(ref.aArreglo(ref.filas[idx]));
	});
}