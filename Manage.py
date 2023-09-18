import tkinter as tk
from tkinter import ttk
import pandas as pd
from PIL import Image, ImageTk


archivo_csv = "contraseñas.csv"


def cargar_contraseñas():
    try:
        return pd.read_csv(archivo_csv)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Sitio Web", "Nombre de Usuario", "Contraseña"])


contraseñas = cargar_contraseñas()


def guardar_contraseñas():
    contraseñas.to_csv(archivo_csv, index=False)


def guardar_contraseña():
    sitio_web = sitio_web_entry.get()
    nombre_usuario = nombre_usuario_entry.get()
    contraseña = contraseña_entry.get()
    
    contraseñas.loc[len(contraseñas)] = [sitio_web, nombre_usuario, contraseña]
    
  
    sitio_web_entry.delete(0, tk.END)
    nombre_usuario_entry.delete(0, tk.END)
    contraseña_entry.delete(0, tk.END)

    guardar_contraseñas()

def ver_contraseñas():
    ventana_ver = tk.Toplevel(ventana_principal)
    ventana_ver.title("Contraseñas")

    tabla = ttk.Treeview(ventana_ver, columns=("Sitio Web", "Nombre de Usuario", "Contraseña", "Editar"), show="headings")
    tabla.heading("Sitio Web", text="Sitio Web")
    tabla.heading("Nombre de Usuario", text="Nombre de Usuario")
    tabla.heading("Contraseña", text="Contraseña")
    tabla.heading("Editar", text="Editar")
    
    for index, row in contraseñas.iterrows():
        editar = "Editar" 
            
        tabla.insert("", index, values=(row["Sitio Web"], row["Nombre de Usuario"], row["Contraseña"], editar))
    
    tabla.pack()
    
    def editar_contraseña(event):
        seleccion = tabla.selection()
        if seleccion:
       
            item = tabla.item(seleccion)
            
            if item['values'][3] == "Editar": 
                contraseña_actual = item['values'][2]
                
            
                ventana_edicion = tk.Toplevel(ventana_ver)
                ventana_edicion.title("Editar Contraseña")
                
           
                nueva_contraseña_label = tk.Label(ventana_edicion, text="Nueva Contraseña:")
                nueva_contraseña_entry = tk.Entry(ventana_edicion)
                
                nueva_contraseña_label.pack()
                nueva_contraseña_entry.pack()
                
           
                def guardar_edición():
                    nueva_contraseña = nueva_contraseña_entry.get()
                    
                   
                    contraseñas.at[index, 'Contraseña'] = nueva_contraseña
                    
             
                    ventana_edicion.destroy()
                    
      
                    tabla.item(seleccion, values=(item['values'][0], item['values'][1], nueva_contraseña, "Editar"))
                    
               
                    guardar_contraseñas()
             
                guardar_button = tk.Button(ventana_edicion, text="Guardar", command=guardar_edición)
                guardar_button.pack()
 
    tabla.bind("<Double-1>", editar_contraseña)


ventana_principal = tk.Tk()
ventana_principal.title("Gestor de Contraseñas")

sitio_web_label = tk.Label(ventana_principal, text="Sitio web:")
nombre_usuario_label = tk.Label(ventana_principal, text="Nombre de usuario:")
contraseña_label = tk.Label(ventana_principal, text="Contraseña:")

sitio_web_entry = tk.Entry(ventana_principal)
nombre_usuario_entry = tk.Entry(ventana_principal)
contraseña_entry = tk.Entry(ventana_principal, show="*") 


linea_divisoria = ttk.Separator(ventana_principal, orient="horizontal")


guardar_button = tk.Button(ventana_principal, text="Guardar Contraseña", command=guardar_contraseña)
ver_button = tk.Button(ventana_principal, text="Ver Contraseñas", command=ver_contraseñas)


sitio_web_label.grid(row=0, column=0)
nombre_usuario_label.grid(row=1, column=0)
contraseña_label.grid(row=2, column=0)

sitio_web_entry.grid(row=0, column=1)
nombre_usuario_entry.grid(row=1, column=1)
contraseña_entry.grid(row=2, column=1)

linea_divisoria.grid(row=3, columnspan=2, sticky="ew", pady=10)

guardar_button.grid(row=4, column=0, columnspan=2)
ver_button.grid(row=5, column=0, columnspan=2)


ventana_principal.mainloop()
