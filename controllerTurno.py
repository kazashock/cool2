from config_bd import get_conexion

# query para que me muestre los datos en la lista de turnos
def obtener_lista_turno():
    query = """
           SELECT tur.IdTurno, est.Nombre, DATE_FORMAT(tur.FechaTurno, '%d/%m/%Y'), DATE_FORMAT(tur.HoraDesde, '%H:%i'), DATE_FORMAT(tur.HoraHasta, '%H:%i'), pac.IdPaciente, pac.Nombre, pac.Apellido, pac.NumeroDocumento,
            esp.Nombre, rec.Nombre
            FROM estadoturno AS est, turno AS tur, paciente AS pac, especialidad AS esp , profesional AS prof, recurso AS rec
            WHERE est.IdEstadoTurno = tur.IdEstadoTurno
            AND pac.IdPaciente = tur.IdPaciente
            AND tur.IdEspecialidad = esp.IdEspecialidad
            AND prof.idEspecialidad = esp.IdEspecialidad
            AND prof.IdRecurso = rec.IdRecurso
            AND tur.FechaBaja is null;             
            """
    conexion = get_conexion()
    turno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    turno = cur.fetchall()
    conexion.close()
    return turno

   
    ## Select tipo de turno - Lista de valores
def obtener_tipoTurno():
    query = "SELECT IdTipoTurno, Nombre FROM tipoturno WHERE FechaBaja is null;"
    conexion = get_conexion()
    tipoTurno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    tipoTurno = cur.fetchall()
    conexion.close()
    return tipoTurno

## Select Especialidades - Lista de valores
def obtener_especialidad_turnos(id): 
    query = """Select IdEspecialidad, Nombre from especialidad 
    WHERE IdEspecialidad in (Select esp.IdEspecialidad from configuracionturno as config, especialidad as esp 
    WHERE config.IdEspecialidad = esp.IdEspecialidad AND config.CantidadComputados <> config.CantidadDisponibles 
    AND config.FechaBaja is null AND config.IdPaciente = {})""".format(id)
    conexion = get_conexion()
    IdEspecialidad = []
    with conexion.cursor() as cur:
        cur.execute(query)
    IdEspecialidad = cur.fetchall()
    conexion.close()
    return IdEspecialidad


## Select profesionales según especialidad - Lista de valores
def obtener_profesionales_especialidad(id):
    query = """
            SELECT pro.idprofesional, rec.nombre, rec.apellido, esp.idespecialidad, esp.nombre
            FROM profesional AS pro, recurso AS rec, especialidad AS esp
            WHERE pro.idespecialidad = esp.idespecialidad
            AND pro.idrecurso = rec.idrecurso
            AND esp.IdEspecialidad = {};""".format(id)
    conexion = get_conexion()
    profesionales_especialidad = []
    with conexion.cursor() as cur:
        cur.execute(query)
    profesionales_especialidad = cur.fetchall()
    conexion.close()
    return profesionales_especialidad 
    

def obtener_turno_por_id(id_turno):
    query = """SELECT est.IdEstadoTurno, est.Nombre, tur.FechaTurno, DATE_FORMAT(tur.HoraDesde, '%H:%i'), DATE_FORMAT(tur.HoraHasta, '%H:%i'), pac.IdPaciente, pac.Nombre, 
                pac.Apellido, pac.NumeroDocumento, tt.IdTipoTurno, tt.Nombre, tur.IdEspecialidad, esp.Nombre, prof.IdProfesional,rec.Nombre, rec.apellido
                FROM estadoturno AS est, turno AS tur, tipoturno AS tt, paciente AS pac, especialidad AS esp , profesional AS prof,recurso AS rec
                WHERE est.IdEstadoTurno = tur.IdEstadoTurno
                AND pac.IdPaciente = tur.IdPaciente
                AND tur.IdTipoTurno = tt.IdTipoTurno
                AND tur.IdEspecialidad = esp.IdEspecialidad
                AND prof.idEspecialidad = esp.IdEspecialidad
                AND prof.IdRecurso = rec.IdRecurso
                AND tur.FechaBaja is null
                AND tur.IdTurno = {}""".format(id_turno)
    conexion = get_conexion()
    id_turno = None
    with conexion.cursor() as cur:
        cur.execute(query),(id_turno)
    id_turno = cur.fetchone()
    conexion.close()
    return id_turno


## Lista de valores de MOTIVOS de anulación de turnos
def obtener_motivoTurno(): 
    query = "SELECT IdMotivo, NombreMotivo FROM motivo WHERE FechaBaja is null;"
    conexion = get_conexion()
    motivoTurno = []
    with conexion.cursor() as cur:
        cur.execute(query)
    motivoTurno = cur.fetchall()
    conexion.close()
    return motivoTurno

## Acá obtengo el ID del turno que está macheado en el app.py
def obtener_id_estado_turno_por_estado(estado):
    query = "SELECT IdEstadoTurno FROM estadoturno WHERE LOWER(Nombre) like LOWER('{}') AND FechaBaja is null".format(estado)
    conexion = get_conexion()
    with conexion.cursor() as cur:
        cur.execute(query)    
    id_estado_turno = cur.fetchone()[0]
    print("esto tiene mi fetchone -> {}".format(id_estado_turno))
    conexion.close()
    return id_estado_turno


## Agregar un nuevo turno en estado asignado:
def insertar_turno_asignado(tipoTurno, idEspecialidadDropdown, idProfesionalDropdown, idPacienteAsignarTurno, fechaTurno, horaDesde, horaHasta, idEstadoTurno):
    conexion = get_conexion()
    query = """
        INSERT INTO turno (IdTipoTurno, IdEspecialidad, IdProfesionalReceptado, IdPaciente, FechaTurno, HoraDesde, HoraHasta, IdEstadoTurno, FechaAsignado, IdUsuarioAsignado, FechaAlta)
        VALUES ({},{},{},{},'{}','{}','{}',{},now(),1,now())""".format(tipoTurno, idEspecialidadDropdown, idProfesionalDropdown, idPacienteAsignarTurno, fechaTurno, horaDesde, horaHasta, idEstadoTurno)
    print("Este es mi insertar turno asignado -> {}".format(query))    
    idTurno_asignado = None    
    with conexion.cursor() as cur:
        cur.execute(query)
        idTurno_asignado = cur.lastrowid
    conexion.commit()
    conexion.close()
    return idTurno_asignado


## Acá obtengo el ID del turno asignado para poder actualizar los turnos computados
def obtener_id_configuracion_turno(id_paciente, id_especialidad):
    query = "SELECT IdconfiguracionTurno FROM configuracionTurno WHERE IdPaciente = {} and IdEspecialidad = {} AND FechaBaja is null;".format(id_paciente, id_especialidad)
    conexion = get_conexion()
    with conexion.cursor() as cur:
        cur.execute(query)
    idConfigTurno = cur.fetchone()[0]
    conexion.close()
    return idConfigTurno


def actualizar_turnos_computados(id_paciente, id_especialidad,id_configturno):
    conexion = get_conexion()
    query = """UPDATE configuracionTurno SET CantidadComputados=(SELECT count(IdTurno) from turno WHERE IdPaciente = {} and IdEspecialidad = {} AND FechaBaja is null),
                FechaModificacion=NOW()
                WHERE IdconfiguracionTurno = {};""".format(id_paciente, id_especialidad, id_configturno)
    print("Este es mi insertar turnos computados -> {}".format(query))  
    turnos_computados = None    
    with conexion.cursor() as cur:
        cur.execute(query)
        turnos_computados = cur.lastrowid
    conexion.commit()
    conexion.close()
    return turnos_computados