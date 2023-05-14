from pick import pick
import os
import pandas as pd
from colorama import Fore , init
init()

#funcion de limpiar pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

#funcion de inicio de sesion
def inciar_sesion():
    
    df = pd.read_csv('data.csv')#lee el archivo csv
    email = input('Ingrese su correo: ')
    password = input('Ingrese su contraseña: ')# pide la contraseña

    #valida si el usuario y contraseña estan en el archivo csv
    if email in df['correo'].values and password in df['contraseña'].values:
        return True
    else:
        return False
   


def registrarse():
    
    #funcion de imprimir datos ingresados
    def imprimir_datos_ingresados(llave, valor):
        limpiar_pantalla()
        #verificar que si existan valores en el diccionario:
        if datos[llave] != '':#si existe un valor en el diccionario
            for key, value in datos.items():
                print(f'{key}: {value}')
                
        else:#si no existe un valor en el diccionario se le asigna el valor ingresado
            datos[llave] = valor
            for key, value in datos.items():
                print(f'{key}: {value}')
            
    #leer el archivo csv        
    df = pd.read_csv('data.csv')
    
    #diccionario de datos vacios
    datos = {'DPI': '', 'correo':'', 'contraseña':'', 'nombre':'', 'apellido':''}
    imprimir_datos_ingresados('DPI','')
     
    #valida si ya existe una cuenta con ese DPI
    dpi = input('Ingrese su DPI: ')
    while dpi in df['DPI'].values:
        print(Fore.RED+'El DPI ya existe')
        Fore.RESET
        dpi = input('Ingrese su DPI: ')
    imprimir_datos_ingresados('DPI',dpi) 


    #valida si ya existe una cuenta con ese correo
    email = input('Ingrese su correo: ')
    while email in df['correo'].values:
        print(Fore.RED+'El usuario ya existe')
        Fore.RESET
        email = input('Ingrese su correo: ')
    imprimir_datos_ingresados('correo',email)
    
    
    #valida si las contraseñas coinciden
    password = input('Ingrese su contraseña: ')
    password2 = input('Ingrese su contraseña nuevamente: ')
    #valida si las contraseñas coinciden y si no coinciden las vuelve a pedir
    while password != password2:
        print(Fore.RED+'Las contraseñas no coinciden')
        Fore.RESET
        password = input('Ingrese su contraseña: ')
        password2 = input('Ingrese su contraseña nuevamente: ')
    imprimir_datos_ingresados('contraseña',len(password)*'*')
    
    
    #pide el nombre y apellido
    nombre = input('Ingrese su nombre: ')
    imprimir_datos_ingresados('nombre',nombre)
    apellido = input('Ingrese su apellido: ')
    imprimir_datos_ingresados('apellido',apellido)
    
    #guarda los datos en el archivo csv uno por uno
    df = df.append([], ignore_index=True)
    df.to_csv('data.csv', index=False)
#funcion de inicio de la aplicacion     
def inicio_app():
    while True:
        #titulo y opciones del menu
        title = 'Bienvenido selecciona una opcion:'
        options = ['Iniciar Sesion', 'Registrarse', 'Salir']#opciones del menu
        option, index = pick(options, title, indicator = '=>',default_index= 0)#mostrar menu
        
        
        limpiar_pantalla()#limpia la pantalla
        
        #validacion de opciones
        if option == 'Iniciar Sesion':#si la opcion es iniciar sesion
            if inciar_sesion() == True:
                print('Bienvenido')
                
        elif option == 'Registrarse':   
            registrarse()

        elif option == 'Salir':
            break

