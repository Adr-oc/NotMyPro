import pandas as pd
import os
from pick import pick
import modules
import numpy as np

trabajos = {
    "Discapacidad auditiva": ["grabador de datos", "operario de limpieza", "jardinero", "trabajador de producción", "servicio al cliente"],
    "Discapacidad visual": ["gestor de cobros", "administrativos", "telemarketing", "servicio al cliente", "recepcionista"],
    "Discapacidad intelectual": ["reponedor", "ordenanza", "mantenimiento en espacios naturales", "operador de limpieza", "trabajos manuales"],
    "Discapacidad física": ["trabajo administrativo", "teleoperador", "programador informático", "diseñador gráfico", "escritor"],
    "Discapacidad psíquica y orgánica": ["bibliotecario", "archivista", "recepcionista", "asistente administrativo", "trabajos manuales"]
}

# funcion de limpiar pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# funcion de iniciar sesion
def iniciar_sesion():

    df = pd.read_csv('data.csv')  # lee el archivo csv
    email = input('Ingrese su correo: ')
    password = input('Ingrese su contraseña: ')  # pide la contraseña

    # valida si el usuario y contraseña estan en el archivo csv
    if email in df['correo'].values and password in df['contraseña'].values:
        dpi_user = df.loc[df['correo'] == email, 'DPI'].iloc[0]
        modules.menu_principal(dpi_user)
    else:
        # retorna falso si el usuario o contraseña no estan en el archivo csv
        print('Usuario o contraseña incorrectos')
        input('Presione enter para continuar')

# funcion de registrarse
def registrarse():

    # funcion de guardar discapacidades
    def guardar_discapacidades(dpi, discapacidades_elegidas):
        df = pd.read_csv('data.csv')
        index = df.index[df['DPI'] == dpi]
        if len(index) > 0:
            index = index[0]
            for discapacidad in discapacidades_elegidas:
                df.loc[index, discapacidad] = True
            df.to_csv('data.csv', index=False)
    # funcion de imprimir datos ingresados

    def imprimir_datos_ingresados(llave, valor):
        limpiar_pantalla()
        # verificar que si existan valores en el diccionario:
        if datos[llave] != '':  # si existe un valor en el diccionario
            for key, value in datos.items():
                print(f'{key}: {value}')

        else:  # si no existe un valor en el diccionario se le asigna el valor ingresado
            datos[llave] = valor
            for key, value in datos.items():
                print(f'{key}: {value}')

    # leer el archivo csv
    df = pd.read_csv('data.csv')
    # diccionario de datos vacios
    datos = {'DPI': '', 'correo': '',
             'contraseña': '', 'nombre': '', 'apellido': ''}
    imprimir_datos_ingresados('DPI', '')

    # valida si ya existe una cuenta con ese DPI
    dpi = int(input('Ingrese su DPI: '))
    while dpi in df['DPI'].values or dpi == '':
        print('El DPI ya existe')

        dpi = int(input('Ingrese su DPI: '))
    imprimir_datos_ingresados('DPI', dpi)

    # valida si ya existe una cuenta con ese correo
    email = input('Ingrese su correo: ')
    while email in df['correo'].values or email == '':
        print('El correo ya existe')
        email = input('Ingrese su correo: ')
    imprimir_datos_ingresados('correo', email)

    # valida si las contraseñas coinciden
    password = input('Ingrese su contraseña: ')
    password2 = input('Ingrese su contraseña nuevamente: ')
    # valida si las contraseñas coinciden y si no coinciden las vuelve a pedir
    while password != password2 or password == '' or password2 == '':
        print('Las contraseñas no coinciden')
        password = input('Ingrese su contraseña: ')
        password2 = input('Ingrese su contraseña nuevamente: ')
    imprimir_datos_ingresados('contraseña', len(password)*'*')

    # pide el nombre y apellido
    nombre = input('Ingrese su nombre: ')
    imprimir_datos_ingresados('nombre', nombre)
    apellido = input('Ingrese su apellido: ')
    imprimir_datos_ingresados('apellido', apellido)

    # df para guardar los datos

    # titulo y opciones del menu
    userData = {'DPI': dpi, 'correo': email, 'contraseña': password,
                'nombre': nombre, 'apellido': apellido}
    df = pd.DataFrame(userData, index=[0])
    df.to_csv('data.csv', mode='a', header=False, index=False)
    print('Usuario registrado con exito')
    input('Presione enter para continuar')

    title = "Eliga la discapacidad: (presione espacio para seleccionar) (presione enter para continuar)"
    opciones = list(trabajos.keys())
    discapacidades_elegidas = pick(
        opciones, title, multiselect=True, min_selection_count=1)

    discapacidades_elegidas = [x[0] for x in discapacidades_elegidas]
    guardar_discapacidades(dpi, discapacidades_elegidas)

# funcion para obtener los trabajos de las discapacidades
def get_disabilities(dpi):
    def get_jobs_for_disability(discapacidad):
        jobs = {
            "Discapacidad auditiva": ["grabador de datos", "operario de limpieza", "jardinero", "trabajador de producción", "servicio al cliente"],
            "Discapacidad visual": ["gestor de cobros", "administrativos", "telemarketing", "servicio al cliente", "recepcionista"],
            "Discapacidad intelectual": ["reponedor", "ordenanza", "mantenimiento en espacios naturales", "operador de limpieza", "trabajos manuales"],
            "Discapacidad física": ["trabajo administrativo", "teleoperador", "programador informático", "diseñador gráfico", "escritor"],
            "Discapacidad psíquica y orgánica": ["bibliotecario", "archivista", "recepcionista", "asistente administrativo", "trabajos manuales"]
        }
        return jobs.get(discapacidad, [])
    
    df = pd.read_csv('data.csv')

    user_data = df[df['DPI'] == dpi]
    if user_data.empty:
        print("No se encontró ningún usuario con el DPI proporcionado.")
        return

    row = user_data.iloc[0]
    columnas_discapacidades = [col for col in df.columns if col.startswith("Discapacidad")]

    print(f"Nombre: {row['nombre']} {row['apellido']}")
    i = 0
    for discapacidad in columnas_discapacidades:
        limpiar_pantalla()
        i = 0
        valor = row[discapacidad]
        if pd.notna(valor) and valor:
            print(f"  - {discapacidad}")
            print("Trabajos disponibles:")
            jobs = get_jobs_for_disability(discapacidad)
            for job in jobs:
                i += 1
                print(f"{i}.   - {job}")
            df2 = pd.read_csv('data.csv')
            df2 = df2[df2['DPI'] == dpi]

            # Obtén los trabajos seleccionados
            trabajos_seleccionados = input("Ingrese el número de los trabajos que le interesan separados por coma: ")
            trabajos_seleccionados = trabajos_seleccionados.split(',')
            trabajos_seleccionados = [jobs[int(num) - 1] for num in trabajos_seleccionados if num.isdigit()]

            # Obtén el índice de la fila
            row_index = df2.index[0]

            # Obtiene los trabajos existentes en la fila
            trabajos_actuales = str(df2.at[row_index, "Trabajos"])  # Convertir a cadena

            # Verifica si los trabajos seleccionados ya existen en la columna "Trabajos"
            nuevos_trabajos = []
            for trabajo in trabajos_seleccionados:
                if trabajo not in trabajos_actuales:
                    nuevos_trabajos.append(trabajo)

            # Agrega los nuevos trabajos a la columna "Trabajos" si no existen
            if nuevos_trabajos:
                trabajos_nuevos = trabajos_actuales + ", " + ", ".join(nuevos_trabajos)

                # Actualiza la columna "Trabajos" con los nuevos trabajos
                df2.at[row_index, "Trabajos"] = trabajos_nuevos

                # Guarda los cambios en el archivo CSV
                df2.to_csv('data.csv', index=False)
                print("Los trabajos se agregaron exitosamente.")
            else:
                print("Los trabajos seleccionados ya existen en la lista.")

    limpiar_pantalla()          
    print("Trabajos actualizados y guardados exitosamente.")


# función para ver el perfil de un usuario
def ver_perfil(dpi):
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv('data.csv')

    # Filtrar el DataFrame para obtener el usuario específico
    usuario = df[df['DPI'] == dpi]

# Obtener los valores de las columnas correspondientes
    dpi = usuario['DPI'].values[0]
    correo = usuario['correo'].values[0]
    contraseña = usuario['contraseña'].values[0]
    nombre = usuario['nombre'].values[0]
    apellido = usuario['apellido'].values[0]

    # Imprimir los datos del usuario
    print("DPI:", dpi)
    print("Correo:", correo)
    print("Contraseña:", len(contraseña)*'*')
    print("Nombre:", nombre)
    print("Apellido:", apellido)


    # Obtener las columnas de discapacidades del DataFrame
    columnas_discapacidades = [col for col in df.columns if col.startswith("Discapacidad")]

    # Verificar y mostrar las discapacidades si son True
    print('Discapacidades:')
    # Iterar sobre las columnas de discapacidades
    for discapacidad in columnas_discapacidades:
        # Obtener el valor de la discapacidad
        valor = usuario[discapacidad].values[0]
        # Verificar si el valor es True
        if pd.notna(valor) and valor:
            # Imprimir el nombre de la discapacidad
            print(discapacidad)

# función para editar el perfil de un usuario
def editar_perfil(dpi):
    df = pd.read_csv('data.csv')

    user_data = df[df['DPI'] == dpi]
    if user_data.empty:
        print("No se encontró ningún usuario con el DPI proporcionado.")
        return

    row_index = user_data.index[0]
    row = user_data.iloc[0]

    print("Datos actuales del usuario:")
    for column, value in row.items():
        if column == 'contraseña':
            print('contraseña: ', len(value)*'*')
        else:
            print(f"{column}: {value}")

    options = ['Correo', 'Contraseña', 'Nombre', 'Apellido']

    option, _ = pick(options, "Seleccione la opción que desea editar:")

    if option.lower() == 'contraseña':
        old_password = input("Ingrese su contraseña actual: ")
        new_password = input("Ingrese su nueva contraseña: ")
        confirm_password = input("Confirme su nueva contraseña: ")

        if row['contraseña'] != old_password:
            print("La contraseña actual ingresada no coincide.")
            return
        elif new_password != confirm_password:
            print("Las nuevas contraseñas ingresadas no coinciden.")
            return
        else:
            df.at[row_index, 'contraseña'] = new_password
    else:
        new_value = input(f"Ingrese el nuevo valor para {option}: ")
        df.at[row_index, option.lower()] = new_value

    df.to_csv('data.csv', index=False)

    print("Perfil actualizado exitosamente.")

# función para editar las discapacidades de un usuario
def editar_discapacidades(dpi):
    df = pd.read_csv('data.csv')

    user_data = df[df['DPI'] == dpi]
    if user_data.empty:
        print("No se encontró ningún usuario con el DPI proporcionado.")
        return

    row_index = user_data.index[0]
    row = user_data.iloc[0]
    disabilities = [col for col in df.columns if col.startswith("Discapacidad")]
    selected_disabilities = pick(disabilities, "Seleccione las discapacidades:", multiselect=True, min_selection_count=0)
    discapacidades_elegidas = [x[0] for x in selected_disabilities]

    for disability in disabilities:
        if disability in discapacidades_elegidas:
            df.at[row_index, disability] = True
        else:
           df.at[row_index, disability] = ''

    df.to_csv('data.csv', index=False)

    print("Discapacidades actualizadas exitosamente.")

# función para ver los empleos aplicados de un usuario
def ver_empleos_aplicados(dpi):
    # Lee el archivo CSV
    df = pd.read_csv('data.csv')

    # Filtra los datos por el número de DPI especificado
    filtro_dpi = df['DPI'] == dpi
    df_filtrado = df[filtro_dpi]

    # Verifica si se encontraron registros para el DPI especificado
    if df_filtrado.empty:
        print("No se encontraron empleos aplicados para el DPI especificado.")
        return

    # Obtén los trabajos de la primera fila filtrada
    trabajos = df_filtrado.at[df_filtrado.index[0], "Trabajos"]

    # Imprime los trabajos de forma bonita
    print(f"Trabajos aplicados para DPI {dpi}:")
    if pd.isnull(trabajos):
        print("No se han seleccionado trabajos.")
    else:
        trabajos_lista = trabajos.split(", ")
        trabajos_lista = [trabajo for trabajo in trabajos_lista if pd.notnull(trabajo)]  # Omitir NaN
        if trabajos_lista:
            for i, trabajo in enumerate(trabajos_lista, start=0):
                if trabajo == 'nan':
                    pass
                else:
                    print(f"{i}. {trabajo}")
        else:
            print("No se han seleccionado trabajos.")



