from database import conexiondb
from mysql.connector import Error


class Cliente:
    def __init__(self) -> None:
        pass

    def constructorCliente(
        self, id, nombres, apellidos, correo, nit, direccion, fechacreacion
    ):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.nit = nit
        self.direccion = direccion
        self.fechacreacion = fechacreacion

    def actualizarCliente(self):
        query = "update usuario set nombres = %s, apellidos = %s, nit = %s, direccion = %s  where idCliente = %s;"
        conn = conexiondb.conexion
        data = (
            self.nombres,
            self.apellidos,
            self.nit,
            self.direccion,
            self.id,
        )
        try:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            return 1
        except Error as e:
            print(f"Error insertar a la base de datos: {e}")
            return 0

    def eliminarCliente(self, id):
        query = "delete from usuario where idCliente =" + str(id)
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

    def VerClientes(self, id):
        try:
            conn = conexiondb.conexion
            cursor = conn.cursor()

            query = (
                "select idCliente, nombres, apellidos, correo, nit, direccion, fechacreacion from usuario where idrole ="
                + str(id)
            )
            cursor.execute(query)
            ver = cursor.fetchall()
            dicti = []
            for item in ver:
                row = {}
                row["id"] = item[0]
                row["nombres"] = item[1]
                row["apellidos"] = item[2]
                row["correo"] = item[3]
                row["nit"] = item[4]
                row["direccion"] = item[5]
                row["fechacreacion"] = item[6]
                dicti.append(row)

            return dicti

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return 0
