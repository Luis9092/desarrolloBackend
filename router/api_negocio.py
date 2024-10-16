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
    )
    retorno = pr.modificarProducto()
    if retorno == 1:
        return Response(status_code=HTTP_200_OK)

    return Response(status_code=HTTP_404_NOT_FOUND)


@api.delete("/eliminarProducto/<id>")
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
