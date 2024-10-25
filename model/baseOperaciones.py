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
    nit:str
    direccion:str

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
    

class basebuscarproducto(BaseModel):
    id : int
    nombre: str
    descripcion: str
    imagen: str
    cantidad: int
    precio:float

class baseVenta(BaseModel):
    id : int
    serie: str
    iduser: int
    fechaCompra: str

class baseVentaDetalle(BaseModel):
    id: int
    idventa: int
    idproducto: int
    cantidad : int
    preciounitario: float

class baseestadoPedido(BaseModel):
    id: int
    iduser: int
    idventa: int
    estado: str
    fechaPedido: str
    
class BaseCliente(BaseModel):
    id : int
    nombres: str
    apellidos: str
    correo: str
    nit: str
    direccion: str
    fechacreacion:str

class BasePedido(BaseModel):
    id : int
    nombres: str
    apellidos: str
    direccion: str
    idventa: int
    estado: str
    fecha: str


class BaseVentaDetalleVer(BaseModel):
    idproducto : int
    nombre: str
    descripcion: str
    cantidad: int
    precio: float
    