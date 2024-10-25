from database import conexiondb
from mysql.connector import Error


class compras:
    def __init__(self) -> None:
        pass

    def constructorCompra(self, id, serie, iduser, fechacompra):
        self.id = id
        self.serie = serie
        self.iduser = iduser
        self.fechacompra = fechacompra

    def constuctorcompraDetalle(
        self, idcompradet, idventa, idproducto, cantidad, precioUnitario
    ):
        self.idcompradet = idcompradet
        self.idventa = idventa
        self.idproducto = idproducto
        self.cantidad = cantidad
        self.precioUnitario = precioUnitario

    def agregarCompra(self):
        query = "insert into venta(serie, iduser, fechafactura) values (%s, %s, %s);"
        conn = conexiondb.conexion
        data = (
            self.serie,
            self.iduser,
            self.fechacompra,
        )
        try:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            return 1
        except Error as e:
            print(f"Error insertar a la base de datos: {e}")
            return 0

    def agregarCompraDetalle(self):
        query = "insert into ventadetalle(idventa, idproducto, cantidad, precioUnitario) values(%s, %s, %s,%s);"
        conn = conexiondb.conexion
        data = (
            self.idventa,
            self.idproducto,
            self.cantidad,
            self.precioUnitario,
        )
        try:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            return 1
        except Error as e:
            print(f"Error insertar a la base de datos: {e}")
            return 0

    def estadoPedido(self, iduser, idventa, fecha):
        query = "insert into pedido(iduser, idventa, estado, fechaPedido) values(%s,%s,%s,%s);"
        conn = conexiondb.conexion
        data = (
            iduser,
            idventa,
            "Enviado",
            fecha,
        )
        try:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            return 1
        except Error as e:
            print(f"Error insertar a la base de datos: {e}")
            return 0

    def buscarventa(self, fecha):
        try:
            print(fecha)
            conn = conexiondb.conexion
            cursor = conn.cursor()

            query = "select idventa from venta where fechaFactura ='" + str(fecha) + "'"
            cursor.execute(query)
            row = cursor.fetchone()
            return {"id": row[0]}

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def modificarStock(self):
        can = self.cantidad
        id = self.idproducto
        query = (
            "update producto set cantidad = (cantidad - "
            + str(can)
            + ") where idproducto ="
            + str(id)
        )
        conn = conexiondb.conexion

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return 1
        except Error as e:
            print(f"Error insertar a la base de datos: {e}")
            return 0
