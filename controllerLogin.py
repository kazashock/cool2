from config_bd import get_conexion

# query para que me muestre los datos en la lista de USUARIOS
def obtener_idusuarios(usuario):
    query = """ 
           SELECT IdUsuario FROM usuario WHERE Nombre = '{}';         
            """.format(usuario)
    conexion = get_conexion()
    with conexion.cursor() as cur:
        cur.execute(query)
    usuario = cur.fetchone()[0]
    print("esto tiene mi fetchone -> {}".format(usuario))
    conexion.close()
    return usuario

# query para que me muestre los datos del recurso a seleccionar
def obtener_idpassword(user):
    query = """ 
           SELECT Contraseña FROM usuario WHERE IdUsuario = {};         
            """.format(user)
    conexion = get_conexion()
    with conexion.cursor() as cur:
        cur.execute(query)
    passwordDB = cur.fetchone()[0]
    conexion.close()
    return passwordDB


