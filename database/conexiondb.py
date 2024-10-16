import mysql.connector
from mysql.connector import Error

host = "localhost"
usuario = "usuariochiquis"
contrasena = "casa12345_12"
base_datos = "dbchiquis"

try:
    conexion = mysql.connector.connect(
        host=host,
        user=usuario,
        password=contrasena,
        database=base_datos,
        auth_plugin="mysql_native_password",
    )
    if conexion.is_connected():
        print("Conexión exitosa a la base de datos")


except Error as e:
    print(f"Error al conectarse a la base de datos: {e}")


# Ejemplo de uso
