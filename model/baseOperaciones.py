from pydantic import BaseModel


class BaseUsuario(BaseModel):
    id: int
    nombres: str
    apellidos: str
    correo: str
    contrasenia: str
    nit: str
    direccion: str
    fechaCreacion: str
    idrole: int


class perfilUser(BaseModel):
    id: int
    nombres: str
    apellidos: str
    correo: str
    password: str
    fecha: str
    idrol: int
    menu: str

class autenticaruser(BaseModel):
    correo:str
    passw:str

class baseproducto(BaseModel):
    id: int
    nombre: str
    descripcion:str
    imagen:str
    idcategoria: int
    cantidad: int
    preciocompra: float
    precioventa:float
    fechacreacion: str
    idproveedor: int
    

class baseverProveedor(BaseModel):
    id: int
    nombre: str
    telefono: str
    correo: str
    fechacreacion:str

class baseverCategoria(BaseModel):
    id : int
    nombre: str
    