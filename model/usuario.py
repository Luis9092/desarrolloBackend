from database import conexiondb
from mysql.connector import Error

from werkzeug.security import generate_password_hash, check_password_hash

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)


class Usuario:
    def __init__(self) -> None:
        pass

    def constructorUsuario(
        self,
        id,
        nombres,
        apellidos,
        correo,
        contrasenia,
        nit,
        direccion,
        fechaCreacion,
        idrole,
    ):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.contrasenia = contrasenia
        self.nit = nit
        self.direccion = direccion
        self.fechaCreacion = fechaCreacion
        self.idrole = idrole

    def crearUsuario(self):
        query = "INSERT INTO usuario(nombres, apellidos, correo, contrasenia, nit, direccion, fechaCreacion, idrole)\
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        conn = conexiondb.conexion
        data = (
            self.nombres,
            self.apellidos,
            self.correo,
            self.contrasenia,
            self.nit,
            self.direccion,
            self.fechaCreacion,
            self.idrole,
        )
        try:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            return 1
        except Error as e:
            print(f"Error al conectarse a la base de datos: {e}")
            return 0

    def autenticarUsuario(self, correom, passw):
        retorno = ""
        conn = conexiondb.conexion

        seleccionar = conn.cursor()
        seleccionar.execute("select * from usuario where correo='" + correom + "'")
        usuario = seleccionar.fetchone()
        if usuario is not None:
            contra = usuario[4]
            check_pass = check_password_hash(contra, passw)

            if check_pass:
                # retorno = HTTP_201_CREATED
                retorno = self.construirMenu(
                    usuario[8],
                    usuario[0],
                    usuario[1],
                    usuario[2],
                    usuario[3],
                    usuario[5],
                    usuario[6],
                )
            else:
                retorno = HTTP_400_BAD_REQUEST
        else:
            retorno = HTTP_400_BAD_REQUEST
        return retorno

    def construirMenu(self, role, id, nombres, apellidos, correo, nit, direccion):

        conn = conexiondb.conexion
        cursor = conn.cursor()

        query = (
            "select m.nombre, m.link, m.codigo, m.icon  from  menu m,   perfil p where  p.idrole = "
            + str(role)
            + " and p.idmenu = m.idmenu;"
        )
        cursor.execute(query)
        ver = cursor.fetchall()
        dictPerfil = {}
        item = ""
        for m in ver:
            item += (
                '<li title="'
                + m[0]
                + '" id="'
                + m[2]
                + '"> <a href="'
                + m[1]
                + '">'
                + m[3]
                + '<span class ="text">'
                + m[0]
                + " </span> </a></li> \n"
            )
        item += '<li title="Cerrar Sesion" id="salir">\
          <a href="/salir">\
          <i class="bx bx-log-out-circle"></i>\
          <span class="text">Cerrar Sesion</span>\
          </a>\
          </li>'
        print(item)
        dictPerfil["id"] = id
        dictPerfil["nombres"] = nombres
        dictPerfil["apellidos"] = apellidos
        dictPerfil["correo"] = correo
        dictPerfil["password"] = ""
        dictPerfil["fecha"] = ""
        dictPerfil["idrol"] = 0
        dictPerfil["menu"] = item
        dictPerfil["nit"] = nit
        dictPerfil["direccion"] = direccion
        return dictPerfil
