import modelo as mod



        
        

def agregar_empleado(nombre_completo, email, cargo, fecha_contratacion, salario, departamento_id):
    departamento = mod.Departamento.get_by_id(departamento_id)
    mod.Empleado.create(
        nombre_completo=nombre_completo,
        email=email,
        cargo=cargo,
        fecha_contratacion=fecha_contratacion,
        salario=salario,
        departamento=departamento
    )

def agregar_departamento(nombre, descripcion, responsable_id=None):
    responsable = mod.Empleado.get_by_id(responsable_id) if responsable_id else None
    mod.Departamento.create(
        nombre=nombre,
        descripcion=descripcion,
        responsable=responsable
    )

def agregar_proyecto(nombre, descripcion, fecha_inicio, fecha_fin, jefe_id):
    jefe = mod.Empleado.get_by_id(jefe_id)
    mod.Proyecto.create(
        nombre=nombre,
        descripcion=descripcion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        jefe=jefe
    )
