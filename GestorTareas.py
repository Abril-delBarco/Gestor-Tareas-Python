import tkinter as tk
from tkinter import messagebox
import json
import os

class Tarea:
    def __init__(self,descripcion,completada = False):
        self.descripcion = descripcion
        self.completada = completada

    def tareaCompletada (self):
        self.completada = True
        return self.completada
    
    #Esto es para pasar a texto el objeto
    def to_dict(self):
        return {"descripcion": self.descripcion, "completada": self.completada}
    
    #Esto permite pasar de texto a objeto
    @staticmethod #(metodo estatico)
    def from_dict(data):
        return Tarea(data["descripcion"], data["completada"])
    

class GestorTareas:
    def __init__(self):
        self.archivo = "tareas.json" #Esto es seria como el papel
        self.tareas = [] #Esta es la lista en memoria
        self.cargar_tareas() #El gestor lee el papel
    
    def agregar_tarea(self, descripcion):  #aca tendria que haber como un papel o Objeto que represente la hoja, en este caso usaron el json 
        nueva = Tarea(descripcion)
        self.tareas.append(nueva) #Simplemente creo la tarea en una variable y la agrego
        self.guardar_tareas()     

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas.pop(indice)
            self.guardar_tareas() #Actualizamos el papel

    def completar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].tareaCompletada()
            self.guardar_tareas()

    def guardar_tareas(self):
        datos = [t.to_dict() for t in self.tareas] #Convertimos las tareas a diccionarios
        with open(self.archivo, 'w') as f:  #Abrimos el archivo y escribimos
            json.dump(datos, f)

    def cargar_tareas(self):
        try:
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
                # Convertimos los diccionarios de vuelta a Objetos Tarea
                self.tareas = [Tarea.from_dict(d) for d in datos]
        except FileNotFoundError:
            self.tareas = [] # Si no hay papel, empezamos hoja nueva


#Parte de la interfaz

class InterfazGrafica:
    def __init__(self, root):
        self.gestor = GestorTareas()
        self.root = root
        self.root.title("Tareas")
        self.root.geometry("400x500") 
        self.root.configure(bg='#f988ff')

        #Título superior
        titulo = tk.Label(root, text="Lista de Tareas", 
                         bg='#bc4ed8', fg='white', font=('Arial', 16, 'bold'))
        titulo.pack(pady=10)

        #Caja de texto
        self.entrada = tk.Entry(root, font=('Arial', 12), width=30)
        self.entrada.pack(pady=5)
        
        #Boton Agregar 
        btn_agregar = tk.Button(root, text="Agregar Tarea", command=self.agregar,
                               bg='#4c007d', fg='white', font=('Arial', 10, 'bold'),
                               cursor="hand2")
        btn_agregar.pack(pady=5)


        self.lista_box = tk.Listbox(root, font=('Arial', 12), width=40, height=15,
                                   selectbackground='#3498DB')
        self.lista_box.pack(padx=20, pady=10)

        #Panel de Botones inferiores 
        frame_botones = tk.Frame(root, bg='#f988ff')
        frame_botones.pack(pady=10)

        #Boton Completar 
        btn_completar = tk.Button(frame_botones, text="Completar", command=self.completar,
                                 bg='#2980B9', fg='white', font=('Arial', 10), width=12)
        btn_completar.pack(side='left', padx=5)

        #Boton Elimina
        btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=self.eliminar,
                                bg='#C0392B', fg='white', font=('Arial', 10), width=12)
        btn_eliminar.pack(side='left', padx=5)

        self.actualizar_vista()


    def agregar(self):
        texto = self.entrada.get()
        if texto:
            self.gestor.agregar_tarea(texto)
            self.entrada.delete(0, tk.END)
            self.actualizar_vista()

    def completar(self):
        seleccion = self.lista_box.curselection()
        if seleccion:
            index = seleccion[0]
            self.gestor.completar_tarea(index) 
            self.actualizar_vista()

    def eliminar(self):
        seleccion = self.lista_box.curselection()
        if seleccion:
            index = seleccion[0]
            self.gestor.eliminar_tarea(index)
            self.actualizar_vista()

    def actualizar_vista(self):
        self.lista_box.delete(0, tk.END)
        for t in self.gestor.tareas:
            simbolo = "✓" if t.completada else "○"
            texto_tarea = f"{simbolo}  {t.descripcion}"
            self.lista_box.insert(tk.END, texto_tarea)
            if t.completada:
                self.lista_box.itemconfig(tk.END, {'fg': '#27AE60'})

# Bloque de arranque
if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazGrafica(ventana)
    ventana.mainloop()
