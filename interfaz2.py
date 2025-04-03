import tkinter as tk
from tkinter import Button, messagebox, PhotoImage, simpledialog, Label, Frame, Toplevel, Entry, SOLID, CENTER
from PIL import Image, ImageTk
import os
import winsound 

def CargarImagen(imagen): #Función que permite cargar las imagenes redimensioandas (con ayuda de Pillow)
    ruta = os.path.join("Mi Primera GUI", imagen)
    imagen_original = Image.open(ruta) 
    imagen_redimensionada = imagen_original.resize((900, 600))
    return ImageTk.PhotoImage(imagen_redimensionada)

def reproducir_musica(reproduciendo, boton): #Función para la reproducción de la música
    archivo_musica = os.path.join("Mi Primera GUI", "Supernatural_favsong_out.wav")
    
    if reproduciendo[0]:
        winsound.PlaySound(None, winsound.SND_PURGE)
        boton.config(text="▶ Reproducir")
        reproduciendo[0] = False
    else:
        winsound.PlaySound(archivo_musica, winsound.SND_ASYNC | winsound.SND_LOOP)
        boton.config(text="⏸ Pausar")
        reproduciendo[0] = True

def animacionrecursiva(contador, x, direccion): #Función que permite el movimiento del gif en la ventana principal
    if contador > 8:
        contador = 1

    nombre = os.path.join("Mi Primera GUI", f"cat{contador}.gif")
    img = PhotoImage(file=nombre)

    if hasattr(ventana, 'img_animacion_label'): #hasattr permite verificar atributos en la ventana
        ventana.img_animacion_label.destroy()

    ventana.img_animacion_label = Label(ventana, image=img, bg='#FFD1DC')
    ventana.img_animacion_label.place(x=x, y=400)
    ventana.img_animacion = img

    x += 10 * direccion #Instrucciónes para que el gif rebote cuando toque los bordes de la ventana
    if x >= 710:
        direccion = -1
    elif x <= 0:
        direccion = 1

    ventana.after(100, lambda: animacionrecursiva(contador + 1, x, direccion)) #Crea un bucle que actualiza la posición de la animación

def mostrar_tabla(numero, frame, fila=1, num=None):
    if fila == 1:
        for widget in frame.winfo_children(): #Para que cuando vuelva a poner otro número, se limpie
            widget.destroy()
        
        try:
            num = int(numero)
            Label(frame, 
                 text=f"Tabla del {num}", 
                 bg="#FFD1DC", 
                 fg="black", 
                 font=("Georgia", 14, "bold")).pack()
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número válido")
            return
    
    if fila > 10: #Para que se detenga la recursión (Caso base)
        return
    
    Label(frame, 
         text=f"{num} × {fila} = {num*fila}", 
         bg="#FFD1DC", 
         fg="#333", 
         font=("Georgia", 12)).pack()
    
    
    frame.after(500, lambda: mostrar_tabla(numero, frame, fila + 1, num)) #Crea un retraso para que se aprecie el resultado sin bloquear la interfaz grafica

def mostrar_divisores(numero, frame, intentos=0):
    if intentos >= 3: #Numeros de intentos (para poner un limite)
        messagebox.showerror("Error", "Demasiados intentos fallidos")
        return 
    
    for widget in frame.winfo_children():
        widget.destroy()
    
    try:
        num = int(numero)
        divisores = []
        
        def calcular_divisores(n, divisor=1):
            if divisor > n:
                return
            if n % divisor == 0:
                divisores.append(str(divisor))
            calcular_divisores(n, divisor + 1)
        
        calcular_divisores(num) #Llama a la función recursiva
        
        Label(frame,  #estetica
             text=f"Divisores de {num}", 
             bg="#FFD1DC", 
             fg="black", 
             font=("Georgia", 14, "bold")).pack()
        
        Label(frame, 
             text=", ".join(divisores),
             bg="#FFD1DC", 
             fg="#333", 
             font=("Georgia", 12),
             wraplength=300,
             justify="left").pack(pady=20, padx=10)
    
    except ValueError:
        messagebox.showerror("Error", "Debe ingresar un número válido")
        nuevo_numero = simpledialog.askstring("Entrada", "Ingrese un número válido:")
        if nuevo_numero:
            mostrar_divisores(nuevo_numero, frame, intentos + 1)

def AbrirVentana(boton): #Función que maneja los botones
    if boton == "Divisores Exactos": #Cuando se presione, abrira una ventana nueva de divisores
        ventana_divisores = Toplevel(ventana)
        ventana_divisores.title("Divisores Exactos")
        ventana_divisores.minsize(800, 500)
        ventana_divisores.resizable(width=False, height=False)
        
        fondo_divisores = CargarImagen("bgdiv.png")  #Parámetros de estética
        if fondo_divisores:
            Label_Divisores = Label(ventana_divisores, image=fondo_divisores)
            Label_Divisores.place(x=0, y=0)
            Label_Divisores.image = fondo_divisores
        
        divisores_label = tk.Label( #Titulo Divisores
            ventana_divisores, 
            text="Calcule los divisores exactos", 
            font=("Georgia", 30), 
            bg="purple", 
            fg="white", 
            width=21, 
            height=1,  
            justify="center"
        )
        divisores_label.pack(pady=50)
        
        frame_entrada = Frame(ventana_divisores, bg="#800080", padx=20, pady=20, bd=2, relief="ridge")
        frame_entrada.place(x=20, y=150, width=300, height=150)

        Label(frame_entrada, #Estetica del Entry
             text="Ingrese un número:", 
             bg="#800080", 
             fg="white", 
             font=("Georgia", 12)).pack(pady=5)
        
        entrada_numero = Entry(frame_entrada, font=("Georgia", 14))
        entrada_numero.pack(pady=5)
        
        frame_resultado = Frame(ventana_divisores, bg="#FFD1DC", padx=20, pady=20, bd=2, relief="ridge")
        frame_resultado.place(x=400, y=150, width=350, height=150)
        
        boton_calcular = Button( #Botón Calcular
            frame_entrada,
            text="Calcular Divisores",
            bg="#4B0082",
            fg="white",
            activebackground="#6A5ACD",
            font=("Georgia", 12),
            command=lambda: mostrar_divisores(entrada_numero.get(), frame_resultado)
        )
        boton_calcular.pack(pady=8, fill="x")

    elif boton == "Tablas de Multiplicar": #permite que al presionar el boton tablas, se abra una ventana nueva
        ventana_tablas = Toplevel(ventana)
        ventana_tablas.title("Tablas de Multiplicar")
        ventana_tablas.minsize(800, 500)
        ventana_tablas.resizable(width=False, height=False)
        
        fondo_tablas = CargarImagen("bgmulti.png") #fondo
        if fondo_tablas:
            Label_tablas = Label(ventana_tablas, image=fondo_tablas)
            Label_tablas.place(x=0, y=0)
            Label_tablas.image = fondo_tablas

        tablas_label = tk.Label( #etiqueta titulo
            ventana_tablas, 
            text="Tablas de Multiplicar", 
            font=("Georgia", 30), 
            bg="purple", 
            fg="white", 
            width=21, 
            height=1,  
            justify="center"
        )
        tablas_label.pack(pady=50)
        
        frame_entrada = Frame(ventana_tablas, 
                              bg="#800080", 
                              padx=20, 
                              pady=20, 
                              bd=2, 
                              relief="ridge")
        frame_entrada.place(x=50, y=200, width=300, height=150)

        Label(frame_entrada, 
             text="Ingrese un número:", 
             bg="#800080", 
             fg="white", 
             font=("Georgia", 12)).pack(pady=5)
        
        entrada_numero = Entry(frame_entrada, font=("Georgia", 14)) #Asignación de entry
        entrada_numero.pack(pady=5)
        
        frame_resultado = Frame(ventana_tablas, bg="#FFD1DC", padx=20, pady=20, bd=2, relief="ridge")
        frame_resultado.place(x=400, y=125, width=300, height=350)
        
        boton_calcular = Button( #Boton para calcular
            frame_entrada,
            text="Calcular Tabla",
            bg="#4B0082",
            fg="white",
            activebackground="#6A5ACD",
            font=("Georgia", 12),
            command=lambda: mostrar_tabla(entrada_numero.get(), frame_resultado)
        )
        boton_calcular.pack(pady=9, fill="x")


def VentanaAbout(): #ventana sobre mi
    ventana_about = Toplevel(ventana)
    ventana_about.title("Sobre mí")
    ventana_about.minsize(800, 500)
    ventana_about.resizable(width=False, height=False)
    
    
    fondo_about = CargarImagen("bgabout.png")
    
    
    if fondo_about:  #fondo principal
        Label_about = Label(ventana_about, image=fondo_about)
        Label_about.place(x=0, y=0)
        Label_about.image = fondo_about  
        
    
    frame_contenido = Frame(ventana_about, bg="purple", bd=2, relief=SOLID)
    frame_contenido.place(relx=0.5, rely=0.5, anchor=CENTER, width=700, height=400)

    try: #para foto personal
        me_img = Image.open(os.path.join("Mi Primera GUI", "me.png"))
        me_img = me_img.resize((200, 200), Image.Resampling.LANCZOS)
        mi_foto = ImageTk.PhotoImage(me_img)
        
        frame_me = Frame(frame_contenido, bg="purple")
        frame_me.grid(row=0, column=0, padx=20, pady=20)
        
        Label(frame_me, image=mi_foto, bg="pink").pack()
        Label(frame_me, text="Sofía Vargas González", bg="pink", font=("Georgia", 12, "bold")).pack()
        Label(frame_me, text="Edad: 19 años", bg="pink", font=("Georgia", 12)).pack()
        Label(frame_me, text="Hobbies: Escuchar música, colorear y hacer ejercicio", bg="pink", font=("Georgia", 12)).pack()
        frame_me.image = mi_foto
    except Exception as e:
        print(f"Error cargando mi foto: {e}")

    try: #para la foto con la familia
        family_img = Image.open(os.path.join("Mi Primera GUI", "family.png"))
        family_img = family_img.resize((200, 150), Image.Resampling.LANCZOS)
        family = ImageTk.PhotoImage(family_img)
        
        frame_family = Frame(frame_contenido, bg="pink")
        frame_family.grid(row=0, column=1, padx=20, pady=5)
        frame_family.place(x=420, y=20)
        
        Label(frame_family, image=family, bg="pink").pack()
        Label(frame_family, text="Familia González Quirós", bg="pink", font=("Georgia", 12, "bold")).pack()
        frame_family.image = family
    except Exception as e:
        print(f"Error cargando foto familiar: {e}")

    try: #para la foto de la pelicula
        movie_img = Image.open(os.path.join("Mi Primera GUI", "favmovie.png"))
        movie_img = movie_img.resize((200, 150), Image.Resampling.LANCZOS)
        movie = ImageTk.PhotoImage(movie_img)
        
        frame_movie = Frame(frame_contenido, bg="pink")
        frame_movie.place(x=420, y=210)
        Label(frame_movie, image=movie, bg="pink").pack()
        Label(frame_movie, text="Pelicula Favorita", bg="pink", font=("Georgia", 12, "bold")).pack()
        frame_movie.image = movie
    except Exception as e:
        print(f"Error cargando película: {e}")

        #estetica para el reproductor de la canción
    frame_music = Frame(frame_contenido, bg="pink")
    frame_music.grid(row=2, column=0, columnspan=2, pady=10)
    
    Label(frame_music,
          text="Canción Favorita: Supernatural - Ariana Grande",
          bg="pink",
          font=("Georgia", 10)
          ).pack(pady=5)
    
    reproduciendo = [False]
    boton_musica = Button(frame_music, 
                         text="▶ Reproducir", 
                         command=lambda: reproducir_musica(reproduciendo, boton_musica),
                         bg="#CF9FFF",
                         fg="white",
                         font=("Georgia", 10)
                         )
    boton_musica.pack()
    
    
    def mantener_referencias(): #Función que verifica cada segundo si la ventana esta abierta (para dejar de reproducir musica)
        ventana_after_id = ventana_about.after(1000, mantener_referencias)
        if not ventana_about.winfo_exists():
            ventana_about.after_cancel(ventana_after_id)
            winsound.PlaySound(None, winsound.SND_PURGE)
    
    mantener_referencias()

#Estetica de ventana principal
ventana = tk.Tk()
ventana.title("Mi Primera Interfaz Gráfica")
ventana.minsize(800, 500)
ventana.resizable(width=False, height=False)
fondo_principal = CargarImagen("bgmain.png")
LabelBackground = Label(ventana, image=fondo_principal)
LabelBackground.place(x=0, y=0)

mainlabel = tk.Label( #Titulo
    ventana, 
    text="Mi Primera Interfaz Gráfica", 
    font=("Georgia", 30), 
    bg="purple", 
    fg="white", 
    width=21, 
    height=1,  
    justify="center"
)
mainlabel.pack(pady=50)

animacionrecursiva(1, 20, 1) #Llama a la función de la animación para que se reproduzca


tablas = tk.Button( #config boton tablas
    ventana, 
    text="Tablas de Multiplicar", 
    command=lambda: AbrirVentana("Tablas de Multiplicar"),
    width=20,
    height=2,
    bg="purple",
    fg="white",
    font=("Georgia", 12),
    padx=10,
    pady=10
)
tablas.place(x=100, y=200)

divisores = Button( #config boton divisores
    ventana, 
    text="Divisores Exactos", 
    command=lambda: AbrirVentana("Divisores Exactos"),
    width=20,
    height=2,
    bg="purple",
    fg="white",
    font=("Georgia", 12),
    padx=10,
    pady=10
)
divisores.place(x=500, y=200)

about = Button( #config boton sobre mi
    ventana, 
    text="Sobre mí", 
    command=VentanaAbout,
    width=20,
    height=2,
    bg="purple",
    fg="white",
    font=("Arial", 12),
    padx=10,
    pady=10
)
about.place(x=300, y=300)
#mantiene la ventana abierta
ventana.mainloop()