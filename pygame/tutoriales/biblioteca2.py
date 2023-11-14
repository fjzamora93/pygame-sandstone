"""
Este ejercicio consiste en la construcción de una biblioteca con los siguientes requisitos:
1.	Mantener un registro de los libros en la biblioteca, incluyendo información como título, autor, género y disponibilidad.
2.	Permitir a los usuarios:
•	Consultar la lista de libros disponibles.
•	Tomar prestado un libro si está disponible.
•	Devolver un libro prestado.
3.	Implementar un sistema de autenticación para los usuarios, donde se les pide que ingresen un nombre de usuario y una contraseña para acceder a las funciones de préstamo y devolución de libros.
4.	Registrar el historial de préstamos de cada usuario, incluyendo la fecha en que tomaron prestado un libro y la fecha en que lo devolvieron.
5.	Proporcionar información detallada sobre los libros, como la cantidad de ejemplares disponibles y la información del autor

"""
import csv,sys
import datetime
catalogo=[]
base_datos_usuarios=[]



with open ('biblioteca.csv','r',encoding='utf-8',newline="") as archivo_csv:
    lector_csv=csv.DictReader(archivo_csv)
    for fila in lector_csv:
        catalogo.append(fila)

with open ('usuario.csv','r',encoding='utf-8',newline="") as archivo_csv:
    lector_csv=csv.DictReader(archivo_csv)
    for fila in lector_csv:
        base_datos_usuarios.append(fila)

def main():
    global usuario
    global base_datos_usuarios
    usuario=login()
    biblio()
    
def biblio():    
    if usuario:
        print (f"\nBienvenido a la biblioteca📚📚📚, {usuario['Nombre']}")
    else:
        print ("\nBienvenido a la biblioteca 📚📚📚\n Recuerda que para retirar o devolver un libro, es necesario estar registrado. ")
    bibliotecaria=input("¿Qué operación te gustaría realizar?:\
                         \n 1. Retirar 📗↪️\
                         \n 2. Devolver ↩️📕\
                         \n 3. Consultar 🔍\
                         \n 4. Donar💙\
                         \n 5. Atrás ⏪\
                         \n 6. Salir 🚪\n")
    if usuario and bibliotecaria=="1":
        tomar_prestado(usuario)
    elif usuario and bibliotecaria=="2":
        devolver()
    elif bibliotecaria=="3": 
        consulta()
    elif bibliotecaria=="4": 
        donar()
    elif bibliotecaria=="5":
        main()
    elif bibliotecaria=="6":
        sys.exit("¡Hasta pronto!👋👋👋")
    else:
        print ("⛔Permisos insuficientes. Regístrate o crea una cuenta de usuario")
        main()

def tomar_prestado(usuario):
    if usuario['Libros Retirados'] != "Sin libros retirados":
        print (f"⚠️   \n En este momento no es posible retirar más libros. \n Recuerda que tienes pendiente de entrega {usuario['Libros Retirados']}")
        siguiente()
    peticion = input("¿Qué libro quieres retirar?: ")
    busqueda = False
    for libro in catalogo:
        if peticion == libro["Título"] and libro["Disponibilidad"] == "True" and usuario["Libros Retirados"]=="Sin libros retirados":
            busqueda = True
            libro["Disponibilidad"] = "False"
            reescribir_csv()
            usuario["Libros Retirados"] = libro["Título"]
            usuario["Fecha Retirada"]=datetime.date.today()
            usuario["Fecha Devolución"]=usuario["Fecha Retirada"]+datetime.timedelta(days=15)

            reescribir_usuario(base_datos_usuarios)
            print(f"📚 Acabas de sacar {libro['Título']}.\n \
            Recuerda devolver el libro antes del {usuario['Fecha Devolución']}📅")
            break
        elif peticion.lower() in libro["Título"].lower():
            verificar = input(f"Quizás quería referirse a: {libro['Título']}.\n Escriba 'Sí' para confirmar: \n ")
            if verificar.lower() == "sí" or verificar.lower() == "si":
                print("CÓDIGO PENDIENTE DE CORREGIR")
            else:
                pass

        elif peticion == libro["Título"] and libro["Disponibilidad"] == "False":
            busqueda = True
            print("⚠️   Libro no disponible ❕ \n")
        
    if busqueda==False:
        print("⚠️   El libro no existe \n")

    siguiente()
    

def devolver():
    devolucion=False
    peticion=input("¿Qué libro quieres devolver? ")
    for libro in catalogo:
        if peticion == usuario["Libros Retirados"]:
            libro["Disponibilidad"]="True"
            usuario["Libros Retirados"]="Sin libros retirados"
            usuario["Fecha Retirada"]=None
            usuario["Fecha Devolución"]=None
            print ("El libro se ha devuelto exitosamente\n")
            reescribir_csv()
            reescribir_usuario(base_datos_usuarios)
            devolucion=True
    if not devolucion:
        print ("El libro mencionado no forma parte de nuestra biblioteca \n")
    siguiente()

def consulta():
    peticion=input("Introduzca cualquier palabra clave: ")
    resultado=False
    for libro in catalogo:
        if peticion in libro["Título"]:
            print (f"-{libro['Título']} de {libro['Autor']}")
            resultado=True
        elif peticion in libro["Autor"]:
            print (f"-{libro['Título']} de {libro['Autor']}")
            resultado=True
        elif peticion in libro["Género"]:
            print (f"GÉNERO {libro['Género'].upper()}: {libro['Título']} de {libro['Autor']}")
            resultado=True
    if resultado==False:
        print("No hay resultados en esta búsqueda\n")
    siguiente()
    

def donar():
    donacion={}
    donacion["Título"]= input("Título: ")
    donacion["Autor"]= input("Autor: ")
    donacion["Género"]= input("Género: ")
    donacion["Disponibilidad"]= True
    catalogo.append(donacion)
    reescribir_csv()
    siguiente()

def reescribir_csv():
    with open ("biblioteca.csv", "w",encoding='utf-8',newline="") as archivo_csv:
        encabezados=["Título","Autor","Género","Disponibilidad"]
        escritor_csv=csv.DictWriter(archivo_csv,fieldnames=encabezados)
        escritor_csv.writeheader()

        for fila in catalogo:
            escritor_csv.writerow(fila)

def reescribir_usuario(base_datos_usuarios):
    with open("usuario.csv", "w", encoding='utf-8', newline="") as archivo_csv:
        encabezados = ["Nombre", "Contraseña", "Libros Retirados", "Fecha Retirada", "Fecha Devolución"]
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=encabezados)
        escritor_csv.writeheader()
        
        for usuario in base_datos_usuarios:
            escritor_csv.writerow(usuario)

def login():
    global base_datos_usuarios
    registro=input(" 1. Nuevo usuario \n 2. Iniciar sesión \n 3. Entrar sin registrar \n ")
    match registro:
        case "1":
            usuario = new_user() 
            return usuario       
        case "2":
            name= input ("Introduzca un nombre de Usuario: ")
            password= input ("Introduzca contraseña: ")
            usuario= iniciar_sesion(name,password,base_datos_usuarios) 
            return usuario
        case "3":
            usuario=False
            return usuario


def una_mayuscula(cadena):
    for letra in cadena:
        if letra.isupper():
            return False
        else:
            return True
        
def iniciar_sesion(name,password,base_datos_usuarios):
    usuario=None
    for usuario in base_datos_usuarios:
        if name == usuario["Nombre"] and password== usuario["Contraseña"]:
            return usuario     
    if not usuario:
        print ("Usuario o contraseña incorrecta \n")
        usuario=None
        login()   

def new_user():
    global base_datos_usuarios
    nuevo_usuario = {}
    while True:
        nuevo_usuario["Nombre"] = input("Introduzca un nombre de Usuario: ")
        nuevo_usuario["Contraseña"] = input("Crear nueva contraseña: ")
        nuevo_usuario["Libros Retirados"] = "Sin libros retirados"
        nuevo_usuario["Fecha Retirada"] = None
        nuevo_usuario["Fecha Devolución"] = None
        if len(nuevo_usuario["Contraseña"]) < 4 or not any(c.isupper() for c in nuevo_usuario["Contraseña"]):
            print("La contraseña debe tener más de 4 caracteres y contener al menos una mayúscula")
        else:
            nombres_usuarios = [user["Nombre"] for user in base_datos_usuarios]
            if nuevo_usuario["Nombre"] in nombres_usuarios:
                print("El nombre de usuario ya está en uso. Elija otro.")
            else:
                base_datos_usuarios.append(nuevo_usuario)
                with open("usuario.csv", "w", encoding='utf-8', newline="") as archivo_csv:
                    encabezados = ["Nombre", "Contraseña", "Libros Retirados", "Fecha Retirada", "Fecha Devolución"]
                    escritor_csv = csv.DictWriter(archivo_csv, fieldnames=encabezados)
                    escritor_csv.writeheader()

                    for fila in base_datos_usuarios:
                        escritor_csv.writerow(fila)
                return nuevo_usuario

def siguiente():
    transicion=input("¿Te gustaría realizar alguna otra operación? \n 1. Sí \n 2. No \n")
    match transicion:
        case "1":
            biblio()
        case "2":
            sys.exit("¡Hasta pronto!👋👋👋")


if __name__=="__main__":
    main()