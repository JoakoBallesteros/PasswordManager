import tkinter as tk
from tkinter import ttk
import pandas as pd
from PIL import Image, ImageTk

# Nombre del archivo CSV donde se guardarán las contraseñas
archivo_csv = "contraseñas.csv"

# Función para cargar contraseñas desde un archivo CSV
def cargar_contraseñas():
    try:
        return pd.read_csv(archivo_csv)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Sitio Web", "Nombre de Usuario", "Contraseña"])

# Cargar las contraseñas al iniciar la aplicación
contraseñas = cargar_contraseñas()

# Función para guardar contraseñas en un archivo CSV
def guardar_contraseñas():
    contraseñas.to_csv(archivo_csv, index=False)

# Función para guardar una contraseña
def guardar_contraseña():
    sitio_web = sitio_web_entry.get()
    nombre_usuario = nombre_usuario_entry.get()
    contraseña = contraseña_entry.get()
    
    # Agregar la contraseña a los datos
    contraseñas.loc[len(contraseñas)] = [sitio_web, nombre_usuario, contraseña]
    
    # Limpiar los campos de entrada
    sitio_web_entry.delete(0, tk.END)
    nombre_usuario_entry.delete(0, tk.END)
    contraseña_entry.delete(0, tk.END)

    # Guardar las contraseñas en el archivo CSV
    guardar_contraseñas()

# Función para ver y editar contraseñas
def ver_contraseñas():
    ventana_ver = tk.Toplevel(ventana_principal)
    ventana_ver.title("Contraseñas")

    # Crear y mostrar una tabla de contraseñas
    tabla = ttk.Treeview(ventana_ver, columns=("Sitio Web", "Nombre de Usuario", "Contraseña", "Editar"), show="headings")
    tabla.heading("Sitio Web", text="Sitio Web")
    tabla.heading("Nombre de Usuario", text="Nombre de Usuario")
    tabla.heading("Contraseña", text="Contraseña")
    tabla.heading("Editar", text="Editar")
    
    for index, row in contraseñas.iterrows():
        editar = "Editar"  # Mostrar el texto "Editar" en la columna de edición
            
        tabla.insert("", index, values=(row["Sitio Web"], row["Nombre de Usuario"], row["Contraseña"], editar))
    
    tabla.pack()
    
    # Función para editar la contraseña seleccionada
    def editar_contraseña(event):
        seleccion = tabla.selection()
        if seleccion:
            # Obtener la contraseña seleccionada
            item = tabla.item(seleccion)
            
            if item['values'][3] == "Editar":  # Verificar si se permite la edición
                contraseña_actual = item['values'][2]
                
                # Crear una ventana emergente de edición
                ventana_edicion = tk.Toplevel(ventana_ver)
                ventana_edicion.title("Editar Contraseña")
                
                # Agregar etiquetas y entradas para la edición
                nueva_contraseña_label = tk.Label(ventana_edicion, text="Nueva Contraseña:")
                nueva_contraseña_entry = tk.Entry(ventana_edicion)
                
                nueva_contraseña_label.pack()
                nueva_contraseña_entry.pack()
                
                # Función para guardar la contraseña editada
                def guardar_edición():
                    nueva_contraseña = nueva_contraseña_entry.get()
                    
                    # Actualizar la contraseña en los datos
                    contraseñas.at[index, 'Contraseña'] = nueva_contraseña
                    
                    # Cerrar la ventana de edición
                    ventana_edicion.destroy()
                    
                    # Actualizar la tabla con la nueva contraseña
                    tabla.item(seleccion, values=(item['values'][0], item['values'][1], nueva_contraseña, "Editar"))
                    
                    # Guardar las contraseñas en el archivo CSV
                    guardar_contraseñas()
                
                # Botón para guardar la edición
                guardar_button = tk.Button(ventana_edicion, text="Guardar", command=guardar_edición)
                guardar_button.pack()
    
    # Enlazar la función de edición al evento de doble clic en la tabla
    tabla.bind("<Double-1>", editar_contraseña)

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Gestor de Contraseñas")

# Etiquetas y entradas
sitio_web_label = tk.Label(ventana_principal, text="Sitio web:")
nombre_usuario_label = tk.Label(ventana_principal, text="Nombre de usuario:")
contraseña_label = tk.Label(ventana_principal, text="Contraseña:")

sitio_web_entry = tk.Entry(ventana_principal)
nombre_usuario_entry = tk.Entry(ventana_principal)
contraseña_entry = tk.Entry(ventana_principal, show="*")  # Para ocultar la contraseña

# Línea divisoria
linea_divisoria = ttk.Separator(ventana_principal, orient="horizontal")

# Botones
guardar_button = tk.Button(ventana_principal, text="Guardar Contraseña", command=guardar_contraseña)
ver_button = tk.Button(ventana_principal, text="Ver Contraseñas", command=ver_contraseñas)

# Posicionar elementos en la ventana
sitio_web_label.grid(row=0, column=0)
nombre_usuario_label.grid(row=1, column=0)
contraseña_label.grid(row=2, column=0)

sitio_web_entry.grid(row=0, column=1)
nombre_usuario_entry.grid(row=1, column=1)
contraseña_entry.grid(row=2, column=1)

linea_divisoria.grid(row=3, columnspan=2, sticky="ew", pady=10)

guardar_button.grid(row=4, column=0, columnspan=2)
ver_button.grid(row=5, column=0, columnspan=2)

# Iniciar la aplicación
ventana_principal.mainloop()
