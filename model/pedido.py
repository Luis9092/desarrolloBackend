from database import conexiondb
from mysql.connector import Error


class Pedido:
    def __init__(self) -> None:
        pass

    def constructorPedido(
        self, id, nombres, apellidos, direccion, idventa, estado, fecha
    ):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.direccion = direccion
        self.idventa = idventa
        self.estado = estado
        self.fecha = fecha

    def verPedido(self):
        try:
            conn = conexiondb.conexion
            cursor = conn.cursor()

            query = "select p.iduser, u.nombres, u.apellidos, u.direccion, p.idventa, p.estado, p.fechaPedido\
                from pedido p, usuario u where p.iduser = u.idCliente order by idventa desc;"
            cursor.execute(query)
            ver = cursor.fetchall()
            dicti = []
            for item in ver:
                row = {}
                estado = ""
                if item[5] == "Enviado":
                    estado = "No Entregado"
                else:
                    estado = item[5]

                row["id"] = item[0]
                row["nombres"] = item[1]
                row["apellidos"] = item[2]
                row["direccion"] = item[3]
                row["idventa"] = item[4]
                row["estado"] = estado
                row["fecha"] = item[6]
                dicti.append(row)

            return dicti

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def verPedidoPorUsuario(self, id):
        try:
            conn = conexiondb.conexion
            cursor = conn.cursor()

            query = (
                "select p.iduser, u.nombres, u.apellidos, u.direccion, p.idventa, p.estado, p.fechaPedido from pedido p, usuario u where p.iduser = u.idCliente and p.iduser = "
                + str(id)
                + " order by p.idventa desc;"
            )
            cursor.execute(query)
            ver = cursor.fetchall()
            dicti = []
            for item in ver:
                row = {}

                row["id"] = item[0]
                row["nombres"] = item[1]
                row["apellidos"] = item[2]
                row["direccion"] = item[3]
                row["idventa"] = item[4]
                row["estado"] = item[5]
                row["fecha"] = item[6]
                dicti.append(row)

            return dicti

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0

    def modificarEstadoPedidoUser(self, id):
        query = "update pedido set estado = 'En Proceso' where idventa =" + str(id)
        conn = conexiondb.conexion

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return 1
        except Error as e:
            print(f"Error insertar a la base de datos: {e}")
            return 0
        
    def modificarEstadoPedidoUserRecibido(self, id):
        query = "update pedido set estado = 'Entregado' where idventa =" + str(id)
        conn = conexiondb.conexion

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return 1
        except Error as e:
            print(f"Error insertar a la base de datos: {e}")
            return 0

    def verPedidoDetalle(self, id):
        try:
            conn = conexiondb.conexion
            cursor = conn.cursor()

            query = (
                "select m.idproducto, p.nombre, p.descripcion, m.cantidad, m.precioUnitario from ventadetalle m, producto p\
                    where m.idproducto = p.idproducto and m.idventa ="
                + str(id)
            )
            cursor.execute(query)
            ver = cursor.fetchall()
            dicti = []
            for item in ver:
                row = {}

                row["idproducto"] = item[0]
                row["nombre"] = item[1]
                row["descripcion"] = item[2]
                row["cantidad"] = item[3]
                row["precio"] = item[4]
                dicti.append(row)

            return dicti

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0
