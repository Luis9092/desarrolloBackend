from database import conexiondb
from mysql.connector import Error

class Producto:
    def _init_(self) -> None:
        pass

    def ConsProducto(
        self,
        idproducto,
        nombre,
        descripcion,
        imagen,
        idcategoria,
        cantidad,
        preciocompra,
        precioventa,
        fechacreacion,
        idproveedor,
    ):
        self.idproducto = idproducto
        self.nombre = nombre
        self.descripcion = descripcion
        self.imagen = imagen
        self.idcategoria = idcategoria
        self.cantidad = cantidad
        self.preciocompra = preciocompra
        self.precioventa = precioventa
        self.fechacreacion = fechacreacion
        self.idproveedor = idproveedor

    def agregarProducto(self):
        query = "INSERT INTO producto(nombre, descripcion, imagen, idcategoria, cantidad, preciocompra, precioventa, fechacreacion, idproveedor)\
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        conn = conexiondb.conexion
        data = (
            self.nombre,
            self.descripcion,
            self.imagen,
            self.idcategoria,
            self.cantidad,
            self.preciocompra,
            self.precioventa,
            self.fechacreacion,
            self.idproveedor,
        )
        try:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            return 1
        except Error as e:
            print(f"Error insertar a la base de datos: {e}")
            return 0

    def modificarProducto(self):
        query = "update producto set nombre = %s, descripcion = %s, imagen = %s, idcategoria = %s, cantidad = %s, preciocompra = %s, precioventa = %s, idproveedor = %s where idproducto = %s;"
        conn = conexiondb.conexion
        data = (
            self.nombre,
            self.descripcion,
            self.imagen,
            self.idcategoria,
            self.cantidad,
            self.preciocompra,
            self.precioventa,
            self.idproveedor,
            self.idproducto,
        )
        try:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            return 1
        except Error as e:
            print(f"Error insertar a la base de datos: {e}")
            return 0

    def eliminarProducto(self, idpro):
        query = "delete from producto where idproducto =" + str(idpro)
        conn = conexiondb.conexion
        try:
            cursor = conn.cursor()
            cursor.execute(
                query,
            )
            conn.commit()
            return 1
        except Error as e:
            print(f"Error eliminar a la base de datos: {e}")
            return 0

    def verProductos(self):
        try:
            conn = conexiondb.conexion
            cursor = conn.cursor()

            query = "select idproducto, nombre, descripcion, imagen, idcategoria, cantidad, preciocompra, precioventa, fechacreacion, idproveedor from producto;"
            cursor.execute(query)
            ver = cursor.fetchall()
            dicti = []
            for item in ver:
                row = {}
                row["id"] = item[0]
                row["nombre"] = item[1]
                row["descripcion"] = item[2]
                row["imagen"] = item[3]
                row["idcategoria"] = item[4]
                row["cantidad"] = item[5]
                row["preciocompra"] = item[6]
                row["precioventa"] = item[7]
                row["fechacreacion"] = item[8]
                row["idproveedor"] = item[9]
                dicti.append(row)

            return dicti

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def verProveedor(self):
        try:
            conn = conexiondb.conexion
            cursor = conn.cursor()

            query = "select idproveedor, nombre, telefono, correo, fechacreacion from proveedor;"
            cursor.execute(query)
            ver = cursor.fetchall()
            dicti = []
            for item in ver:
                row = {}
                row["id"] = item[0]
                row["nombre"] = item[1]
                row["telefono"] = item[2]
                row["correo"] = item[3]
                row["fechacreacion"] = item[4]
                dicti.append(row)

            return dicti

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def verCateogoria(self):
        try:
            conn = conexiondb.conexion
            cursor = conn.cursor()

            query = "select idcategoria, nombrecategoria from categoria;"
            cursor.execute(query)
            ver = cursor.fetchall()
            dicti = []
            for item in ver:
                row = {}
                row["id"] = item[0]
                row["nombre"] = item[1]
                dicti.append(row)

            return dicti

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def buscarProducto(self, id):
        try:
            conn = conexiondb.conexion
            cursor = conn.cursor()

            query = (
                "select idproducto, nombre, descripcion, imagen,  cantidad,  precioventa  from producto where idproducto = "
                + str(id)
            )
            cursor.execute(query)
            ver = cursor.fetchone()
            row = {}
            row["id"] = ver[0]
            row["nombre"] = ver[1]
            row["descripcion"] = ver[2]
            row["imagen"] = ver[3]
            row["cantidad"] = ver[4]
            row["precio"] = ver[5]

            return row

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0
