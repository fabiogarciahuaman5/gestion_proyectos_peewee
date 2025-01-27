from peewee import *
import datetime
import configparser, pymysql


CONFIG_FILE ="config.ini"





def crearBBDD():
    try:
        config = cargarConfiguracion(CONFIG_FILE)['database']
        
        connection = pymysql.connect(host=config['host'],
                            user=config['user'],
                            password=config['password'],
                            port=config.getint('port'))
        
        print("Conexión al servidor MySQL exitosa.")

        # Crear un cursor para ejecutar comandos SQL
        cursor = connection.cursor()

        # Nombre de la base de datos que deseas crear
        database_name = config['database_name']

        # Crear la base de datos
        cursor.execute(f"CREATE DATABASE {database_name};")
        print(f"Base de datos '{database_name}' creada con éxito.")
                             
    except pymysql.Error as e:
        print(f"Error al conectar o crear la base de datos: {e}")
        return None
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None

    finally:
        # Cerrar el cursor y la conexión
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
            print("Conexión cerrada.")
        






def getObjetoMySQLDatabase(archivo):
    """
    Crea y retorna una instancia de un objeto MySQLDatabase utilizando la configuración cargada desde un archivo.

    Parámetros:
        archivo (str): Ruta del archivo de configuración.

    Retorna:
        MySQLDatabase: Objeto de conexión a la base de datos MySQL configurado con los parámetros del archivo.
    """
    # Cargar la configuración desde el archivo.
    config = cargarConfiguracion(archivo)
    
    # Verificar si la sección 'database' existe en el archivo de configuración.
    if 'database' not in config:
        raise ValueError("La sección 'database' no está presente en el archivo de configuración.")
    
    # Obtener la configuración de la base de datos.
    db_config = config['database']
    
    # Crear y retornar una instancia de MySQLDatabase con los parámetros de conexión.
    return MySQLDatabase(
        db_config['database_name'],
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host'],
        port=db_config.getint('port') 
    )






def cargarConfiguracion(archivo):
    """
    Carga y retorna la configuración desde un archivo INI.

    Parámetros:
        archivo (str): Ruta del archivo de configuración.

    Retorna:
        ConfigParser: Objeto que contiene la configuración cargada desde el archivo.
    """
    config = configparser.ConfigParser()
    # Leer el archivo de configuración.
    config.read(archivo)
    
    # Verificar si el archivo se leyó correctamente.
    if not config.sections():
        raise FileNotFoundError(f"No se pudo leer el archivo de configuración: {archivo}")
    
    return config




def conexionBBDD(db=getObjetoMySQLDatabase(CONFIG_FILE)):
    """
    Intenta establecer una conexión a la base de datos MySQL utilizando un objeto MySQLDatabase.

    Parámetros:
        db (MySQLDatabase): Objeto de conexión a la base de datos. Si no se proporciona, se crea uno utilizando la configuración predeterminada.

    Retorna:
        MySQLDatabase: Objeto de conexión a la base de datos si la conexión es exitosa.
    """
    # Intentar establecer la conexión a la base de datos.
    db.connect()
    print('Conexión exitosa')
    return db



def crearTablas():
    try:
        con = conexionBBDD()
        con.create_tables([Departamento, Empleado, Proyecto, Asignacion])
        print("Se crearon las tablas")
        return True
    except OperationalError as e:
        # Capturar errores de conexión.
        print(f"Error de conexión en ingresarDepartamento: {e}")
        return False
    except PeeweeException as e:
        # Capturar otros errores relacionados con Peewee.
        print(f"Error en ingresarDepartamento: {e}")
        return False
    except Exception as e:
        # Capturar cualquier otra excepción no prevista.
        print(f"Error inesperado en ingresarDepartamento: {e}")
        return False
    finally:
        # Cerrar la conexión si está abierta.
        if con and not con.is_closed():
            con.close()
            print("Conexión cerrada.")
            
            
            

def ingresarDepartamento(diccionario: dict):
    """
    Intenta ingresar un departamento en la base de datos.

    Parámetros:
        lista (list): Lista de datos del departamento.

    Retorna:
        bool: True si la operación fue exitosa, False si hubo un error.
    """
    con = None
    try:
        # Intentar establecer la conexión a la base de datos. NO es necesaria esta apertura de conexion
        con = conexionBBDD()
        
        # Crear y guardar un nuevo departamento en la base de datos.
        usuario = Departamento(nombre=diccionario['nombre'], descripcion=diccionario['descripcion'], 
                               idResponsable=diccionario['idResponsable'])
        usuario.save()
        
        print("Se ingreso exitosamente el departamento.")
        
        # Retornar True para indicar que la operación fue exitosa.
        return True
    
    except OperationalError as e:
        # Capturar errores de conexión.
        print(f"Error de conexión en ingresarDepartamento: {e}")
        return False
    except PeeweeException as e:
        # Capturar otros errores relacionados con Peewee.
        print(f"Error en ingresarDepartamento: {e}")
        return False
    except Exception as e:
        # Capturar cualquier otra excepción no prevista.
        print(f"Error inesperado en ingresarDepartamento: {e}")
        return False
    finally:
        # Cerrar la conexión si está abierta.
        if con and not con.is_closed():
            con.close()
            print("Conexión cerrada.")
            
            
def eliminarDepartamento(nombre):
    """
    Intenta eliminar de la base de datos el departamento con el nombre pasado por argumento.

    Retorna:
        bool: True si la operación fue exitosa, False si hubo un error.
    """

    try:
        # Eliminar el registro con el nombre del departamento pasado por argumento.
        query = Departamento.delete().where(Departamento.nombre == nombre)
        query.execute()
        
        # Retornar True para indicar que la operación fue exitosa.
        return True
    
    except OperationalError as e:
        # Capturar errores de conexion.
        print(f"Error de conexión en getTodoDepartamentos: {e}")
        return False
    except PeeweeException as e:
        # Capturar otros errores relacionados con Peewee.
        print(f"Error en getTodoDepartamentos: {e}")
        return False
    except Exception as e:
        # Capturar cualquier otra excepcion no prevista.
        print(f"Error inesperado en getTodoDepartamentos: {e}")
        return False 
    


def getTodoDepartamentos():
    """
    Intenta iterar todos los nombres de departamentos en la base de datos.

    Retorna:
        list: una lista con los nombres de todos los departamentos.

    Lanza:
        OperationalError: si hay un error de conexión a la base de datos.
        PeeweeException: si hay un error relacionado con Peewee.
        Exception: si ocurre cualquier otro error inesperado.
    """
    listaDeptos = []
    try:
        # Obtener todos los registros de la tabla Departamento.
        departamentos = Departamento.select()
        
        for departamento in departamentos:
            listaDeptos.append(departamento.nombre)
        
        return listaDeptos
    
    except OperationalError as e:
        # Capturar errores de conexión.
        raise OperationalError(f"Error de conexión en getTodoDepartamentos: {e}") 
    except InterfaceError as e:
        # Capturar  errores como configuración incorrecta de la base de datos, problemas de red o errores en el controlador de la base de datos.
        raise InterfaceError(f"Error de interfaz en getTodoDepartamentos: {e}")
    except DatabaseError as e:
        # Capturar cualquier error relacionado con la base de datos.
        raise DatabaseError(f"Error en base de datos en getTodoDepartamentos: {e}")
    except Exception as e:
        # Capturar cualquier otra excepción no prevista.
        raise Exception(f"Error inesperado en getTodoDepartamentos: {e}")
    


def consultarDepartamento(nombreDepto:str)->dict:
    listaDeptos = {}
    try:
        # Obtener el registro del nombre del departamento consultado
        departamento = Departamento.get(Departamento.nombre == nombreDepto)
        
        listaDeptos['nombre']=departamento.nombre
        listaDeptos['descripcion']=departamento.descripcion
        
        #Validar que cuando no haya un id en el campo idResponsable 
        #a la lista retornada se le agrega el nombre del empleado asociado a ese id
        if(departamento.idResponsable!=None):
            empleado = Empleado.select(Empleado.nombre).where(Empleado.id==departamento['responsable'])
            listaDeptos['responsable']=empleado
        
        
        else: listaDeptos['responsable']=departamento.idResponsable 
        
        return listaDeptos
    
    except OperationalError as e:
        # Capturar errores de conexión.
        raise OperationalError(f"Error de conexión en getTodoDepartamentos: {e}") 
    except InterfaceError as e:
        # Capturar  errores como configuración incorrecta de la base de datos, problemas de red o errores en el controlador de la base de datos.
        raise InterfaceError(f"Error de interfaz en getTodoDepartamentos: {e}")
    except DatabaseError as e:
        # Capturar cualquier error relacionado con la base de datos.
        raise DatabaseError(f"Error en base de datos en getTodoDepartamentos: {e}")
    except Exception as e:
        # Capturar cualquier otra excepción no prevista.
        raise Exception(f"Error inesperado en getTodoDepartamentos: {e}")
        
        
        
        
def modificarDepartamento(nombreCampo:str, nombreDepto:str, nuevoValor: str):
    try:
        # Obtener el registro del departamento por su nombre
        departamento = Departamento.get(Departamento.nombre == nombreDepto)

        # Validar si el campo existe en el modelo
        if nombreCampo in Departamento._meta.fields:
            # Actualizar el campo y guardar
            setattr(departamento, nombreCampo, nuevoValor)
            departamento.save()
            print(f"Campo '{nombreCampo}' actualizado a '{nuevoValor}' en el departamento '{nombreDepto}'.")
        else:
            raise AttributeError(f"El campo '{nombreCampo}' no existe en el modelo Departamento.")

    except Departamento.DoesNotExist:
        raise DoesNotExist(f"El departamento '{nombreDepto}' no existe en la base de datos.")
    except IntegrityError as e:
        raise IntegrityError(f"Error de integridad al actualizar el campo '{nombreCampo}': {e}")
    except OperationalError as e:
        raise OperationalError(f"Error de operación en la base de datos: {e}")
    except AttributeError as e:
        raise AttributeError(f"Error de atributo: {e}")
    except DatabaseError as e:
        raise DatabaseError(f"Error general en la base de datos: {e}")
    except Exception as e:
        raise Exception(f"Error inesperado: {e}")




class BaseModel(Model):
    class Meta:
        database = getObjetoMySQLDatabase(CONFIG_FILE)  # Asignar la base de datos al modelo base

class Empleado(BaseModel):
    nombreCompleto = CharField()
    email = CharField(unique=True)
    cargo = CharField()
    fechaContratacion = DateField()
    salario = DecimalField(max_digits=10, decimal_places=2)
    idDepartamento = ForeignKeyField('self', null=True, backref='empleados')  # Referencia circular

class Departamento(BaseModel):
    nombre = CharField(unique=True)
    descripcion = TextField()
    idResponsable = ForeignKeyField(Empleado, null=True, backref='departamento_responsable')  # Referencia directa

class Proyecto(BaseModel):
    nombre = CharField(unique=True)
    descripcion = TextField()
    fechaInicio = DateField()
    fechaFin = DateField(null=True)
    jefe = ForeignKeyField(Empleado, backref='proyectos_jefe')

class Asignacion(BaseModel):
    proyecto = ForeignKeyField(Proyecto, backref='asignaciones')
    empleado = ForeignKeyField(Empleado, backref='asignaciones')

   
