from options import *
from pick import pick


def inicio_app():
    while True:
        # titulo y opciones del menu
        title = 'Bienvenido selecciona una opcion:'
        options = ['Iniciar Sesion', 'Registrarse',
                   'Salir']  # opciones del menu
        option, index = pick(options, title, indicator='>',
                             default_index=0)  # mostrar menu

        limpiar_pantalla()  # limpia la pantalla

        # validacion de opciones
        if option == 'Iniciar Sesion':  # si la opcion es iniciar sesion
            iniciar_sesion()

        elif option == 'Registrarse':
            registrarse()

        elif option == 'Salir':
            break


def menu_principal(user_dpi):
    df = pd.read_csv('data.csv')  # lee el archivo csv

    while True:
        limpiar_pantalla()
        # titulo y opciones del menu
        name_user = df.loc[df['DPI'] == user_dpi, 'nombre'].iloc[0]
        title = f'Bienvenido {name_user} selecciona una opcion:'
        options = ['Ver Perfil', 'Editar Perfil','Editar discapacidades', 'Buscar Empleo', 'Ver Empleos Aplicados', 'Cerrar Sesion',
                   'Salir']  # opciones del menu
        option, index = pick(options, title, indicator='>',
                             default_index=0)

        limpiar_pantalla()  # limpia la pantalla
        match option:
            case 'Ver Perfil':
                ver_perfil(user_dpi)
                input('Presione enter para continuar')
            case 'Editar Perfil':
                editar_perfil(user_dpi)
                input('Presione enter para continuar')
            case 'Editar discapacidades':
                editar_discapacidades(user_dpi)
                input('Presione enter para continuar')
            case 'Buscar Empleo':
                get_disabilities(user_dpi)
                input('Presione enter para continuar')
            case 'Ver Empleos Aplicados':
                ver_empleos_aplicados(user_dpi)
                input('Presione enter para continuar')
            case 'Cerrar Sesion':
                break
            case 'Salir':
                print("Saliendo del programa...")
                exit()
