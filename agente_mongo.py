from datetime import datetime
import random
import tkinter as tk
from tkinter import messagebox
import certifi
from pymongo import MongoClient


MONGO_URI = "mongodb+srv://hector1985:Aime131985@karla.t5uvbw4.mongodb.net/ventas_db?retryWrites=true&w=majority"


class AgenteClimatizacionGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Agente de Climatización - MongoDB Atlas")
        self.root.geometry("460x500")
        self.root.config(bg="#f0f2f5")

      
        try:
            self.client = MongoClient(
                MONGO_URI,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=5000,
            )
            
            self.db = self.client["ventas_db"]
            self.coleccion = self.db["registros_clima"]

          
            self.client.admin.command("ping")
            self.estado_mongo = "🟢 Conectado a MongoDB Atlas"
        except Exception as e:
            self.estado_mongo = f"🔴 Error de conexión: {e}"

       
        self.temperatura = 0.0
        self.humedad = 0.0
        self.accion = ""

        
        self.crear_widgets()

    def crear_widgets(self):
    
        lbl_titulo = tk.Label(
            self.root,
            text="Agente de Climatización",
            font=("Helvetica", 16, "bold"),
            bg="#f0f2f5",
            fg="#1a73e8",
        )
        lbl_titulo.pack(pady=15)

        
        frame_sensores = tk.LabelFrame(
            self.root,
            text=" Lecturas del Sensor ",
            font=("Helvetica", 11, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15,
        )
        frame_sensores.pack(padx=20, pady=10, fill="x")

        self.lbl_temp = tk.Label(
            frame_sensores,
            text="Temperatura: -- °C",
            font=("Helvetica", 12),
            bg="#ffffff",
        )
        self.lbl_temp.pack(anchor="w", pady=5)

        self.lbl_humedad = tk.Label(
            frame_sensores,
            text="Humedad: -- %",
            font=("Helvetica", 12),
            bg="#ffffff",
        )
        self.lbl_humedad.pack(anchor="w", pady=5)

        
        frame_accion = tk.LabelFrame(
            self.root,
            text=" Decisión del Agente ",
            font=("Helvetica", 11, "bold"),
            bg="#ffffff",
            padx=15,
            pady=15,
        )
        frame_accion.pack(padx=20, pady=10, fill="x")

        self.lbl_accion = tk.Label(
            frame_accion,
            text="Acción: Esperando simulación...",
            font=("Helvetica", 11, "bold"),
            fg="#d93025",
            bg="#ffffff",
            wraplength=360,
            justify="left",
        )
        self.lbl_accion.pack(anchor="w")

      
        self.btn_simular = tk.Button(
            self.root,
            text="Simular y Guardar en Atlas",
            font=("Helvetica", 11, "bold"),
            bg="#1a73e8",
            fg="white",
            activebackground="#1557b0",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=8,
            command=self.procesar_lectura,
        )
        self.btn_simular.pack(pady=15)

       
        lbl_db = tk.Label(
            self.root,
            text=self.estado_mongo,
            font=("Helvetica", 9, "italic"),
            bg="#f0f2f5",
            fg="#5f6368",
            wraplength=420,
        )
        lbl_db.pack(side="bottom", pady=10)

    def tomar_decision(self):
        """Reglas de condición y acción del agente."""
        if self.temperatura > 30 and self.humedad > 70:
            return "Encender aire acondicionado (Modo Deshumidificador)"
        elif self.temperatura > 30:
            return "Encender ventilador"
        elif self.temperatura < 18:
            return "Encender calefacción"
        else:
            return "Mantener sistema apagado"

    def procesar_lectura(self):
       
        self.temperatura = round(random.uniform(15.0, 35.0), 1)
        self.humedad = round(random.uniform(40.0, 90.0), 1)

      
        self.accion = self.tomar_decision()

        
        self.lbl_temp.config(text=f"Temperatura: {self.temperatura} °C")
        self.lbl_humedad.config(text=f"Humedad: {self.humedad} %")
        self.lbl_accion.config(text=f"Acción: {self.accion}")

       
        documento = {
            "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperatura": self.temperatura,
            "humedad": self.humedad,
            "accion": self.accion,
        }

        try:
            resultado = self.coleccion.insert_one(documento)
            messagebox.showinfo(
                "¡Éxito en Atlas!",
                f"Documento guardado correctamente.\nID: {resultado.inserted_id}",
            )
        except Exception as e:
            messagebox.showerror(
                "Error al guardar",
                f"No se pudo registrar en la nube:\n{e}",
            )


if __name__ == "__main__":
    ventana = tk.Tk()
    app = AgenteClimatizacionGUI(ventana)
    ventana.mainloop()
