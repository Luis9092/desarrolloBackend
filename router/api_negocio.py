import pytz
import os
from fastapi import APIRouter, Response, Form, File, UploadFile
from fastapi import APIRouter, Response, HTTPException
from pydantic import BaseModel
from typing import List
from database import conexiondb
from model.usuario import Usuario
from model import baseOperaciones
from werkzeug.security import generate_password_hash, check_password_hash
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_404_NOT_FOUND,
)
from datetime import datetime

from model.productos import Producto
from model.compras import compras
from model.clientes import Cliente
from model.pedido import Pedido


api = APIRouter()


@api.get("/")
def root():
    seleccionar = conexiondb.conexion.cursor()
    seleccionar.execute("select * from categoria;")
    r = seleccionar.fetchall()
    print(r)

    return {"Iniciando": "Bienvenido"}


@api.post("/crearUsuario")
def crearUsuario(lista: baseOperaciones.BaseUsuario):
    us = Usuario()

    guatemala_timezone = pytz.timezone("America/Guatemala")
    horaGuatemala = datetime.now(guatemala_timezone)
    horaActual = horaGuatemala.strftime("%Y/%m/%d %H:%M:%S")

    contra = generate_password_hash(lista.contrasenia, "pbkdf2:sha256:30", 30)

    us.constructorUsuario(
        0,
        lista.nombres,
        lista.apellidos,
        lista.correo,
        contra,
        lista.nit,
        lista.direccion,
        horaActual,
        1,
    )

    retorno = us.crearUsuario()
    if retorno == 1:
        return Response(status_code=HTTP_201_CREATED)

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.post("/autenticarUsuario")
def autenticarUsuario(lista: baseOperaciones.autenticaruser):
    cl = Usuario()
    retorno = cl.autenticarUsuario(correom=lista.correo, passw=lista.passw)
    return retorno


# PRODUCTOS


@api.post("/crearProducto")
def crearProducto(items: baseOperaciones.baseproducto):
    pr = Producto()
    guatemala_timezone = pytz.timezone("America/Guatemala")
    horaGuatemala = datetime.now(guatemala_timezone)
    horaActual = horaGuatemala.strftime("%Y/%m/%d %H:%M:%S")
    precioVenta = items.preciocompra + (items.preciocompra * 1) / 150
    pr.ConsProducto(
        0,
        items.nombre,
        items.descripcion,
        items.imagen,
        items.idcategoria,
        items.cantidad,
        items.preciocompra,
        precioVenta,
        horaActual,
        items.idproveedor,
    )
    retorno = pr.agregarProducto()
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.put("/modificarProducto")
def modificarProducto(items: baseOperaciones.baseproducto):
    pr = Producto()
    guatemala_timezone = pytz.timezone("America/Guatemala")
    horaGuatemala = datetime.now(guatemala_timezone)
    horaActual = horaGuatemala.strftime("%Y/%m/%d %H:%M:%S")
    precioVenta = items.preciocompra + (items.preciocompra * 1) / 324
    pr.ConsProducto(
        items.id,
        items.nombre,
        items.descripcion,
        items.imagen,
        items.idcategoria,
        items.cantidad,
        items.preciocompra,
        precioVenta,
        horaActual,
        items.idproveedor,
    )
    retorno = pr.modificarProducto()
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.delete("/eliminarProducto/{id}")
def eliminarProducto(id: int):
    pr = Producto()
    retorno = pr.eliminarProducto(idpro=id)
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)
    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/verProductos", response_model=list[baseOperaciones.baseproducto])
def verProductos():
    pr = Producto()
    retorno = pr.verProductos()
    if retorno != 0:
        return retorno

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/verproveedores", response_model=list[baseOperaciones.baseverProveedor])
def verproveedores():
    pr = Producto()
    retorno = pr.verProveedor()
    if retorno != 0:
        return retorno
    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/vercategoria", response_model=list[baseOperaciones.baseverCategoria])
def vercategoria():
    pr = Producto()
    retorno = pr.verCateogoria()
    if retorno != 0:
        return retorno
    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/buscarproducto/<id>", response_model=baseOperaciones.basebuscarproducto)
def buscarProducto(id: int):
    pr = Producto()
    retorno = pr.buscarProducto(id)
    if retorno != 0:
        return retorno
    return Response(status_code=HTTP_404_NOT_FOUND)


@api.post("/agregarVenta")
def agregarVenta(lista: baseOperaciones.baseVenta):
    c = compras()
    c.constructorCompra(0, lista.serie, lista.iduser, lista.fechaCompra)

    retorno_venta = c.agregarCompra()
    if retorno_venta == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.post("/agregarVentaDetalle")
def agregarVentaDetalle(lista: baseOperaciones.baseVentaDetalle):
    c = compras()
    c.constuctorcompraDetalle(
        0, lista.idventa, lista.idproducto, lista.cantidad, lista.preciounitario
    )
    retorno_detalle = c.agregarCompraDetalle()
    if retorno_detalle == 1:
        c.modificarStock()
        return Response(status_code=HTTP_200_OK)
    return Response(status_code=HTTP_404_NOT_FOUND)


@api.post("/estadopedido")
def estadoPedido(lista: baseOperaciones.baseestadoPedido):
    c = compras()

    retorno = c.estadoPedido(lista.iduser, lista.idventa, lista.fechaPedido)
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/obteneridVenta/<fecha>")
def obtenerIdVenta(fecha: str):
    print(fecha)
    c = compras()
    retorno = c.buscarventa(fecha=fecha)
    if retorno != 0:
        return retorno
    return Response(status_code=HTTP_404_NOT_FOUND)


# Clientes


@api.put("/modificarCliente")
def modificarCliente(lista: baseOperaciones.BaseCliente):
    d = Cliente()
    d.constructorCliente(
        lista.id, lista.nombres, lista.apellidos, "", lista.nit, lista.direccion, ""
    )
    retorno = d.actualizarCliente()

    if retorno == 1:
        return Response(status_code=HTTP_200_OK)
    return Response(status_code=HTTP_404_NOT_FOUND)


@api.delete("/eliminarCliente/<id>")
def EliminarCliente(id: int):
    c = Cliente()
    retorno = c.eliminarCliente(id=id)
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get("/verClientes/<id>", response_model=list[baseOperaciones.BaseCliente])
def VerClientes(id: int):
    c = Cliente()
    retorno = c.VerClientes(id=id)
    if retorno != 0:
        return retorno

    return Response(status_code=HTTP_404_NOT_FOUND)


# PEDIDOS


@api.get("/verPedidos", response_model=list[baseOperaciones.BasePedido])
def verPedidos():
    p = Pedido()
    retorno = p.verPedido()
    if retorno != 0:
        return retorno

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.put("/actualizarEstadoPedidoUser/{id}")
def actualizarEstadoPedidoUser(id: int):
    p = Pedido()
    retorno = p.modificarEstadoPedidoUser(id=id)
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_404_NOT_FOUND)

@api.put("/actualizarEstadoPedidoUserrecibido/{id}")
def actualizarEstadoPedidoUserRecibido(id: int):
    p = Pedido()
    retorno = p.modificarEstadoPedidoUserRecibido(id=id)
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.get(
    "/listarCompraDetalle/<id>",
    response_model=list[baseOperaciones.BaseVentaDetalleVer],
)
def listarCompraDetalle(id: int):
    c = Pedido()
    retorno = c.verPedidoDetalle(id=id)
    if retorno != 0:
        return retorno

    return Response(status_code=HTTP_404_NOT_FOUND)


# POR USUARIO


@api.get("/verPedidosporusuario/<id>", response_model=list[baseOperaciones.BasePedido])
def verPedidosporusuario(id: int):
    p = Pedido()
    retorno = p.verPedidoPorUsuario(id=id)
    if retorno != 0:
        return retorno

    return Response(status_code=HTTP_404_NOT_FOUND)
