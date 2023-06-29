import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from tkinter import ttk
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from ttkthemes import ThemedStyle


class AnalizadorDatos:
    def __init__(self):
        # Configuración de la interfaz gráfica
        self.root = tk.Tk()
        self.root.title("Predicción y Clasificación de Datos")
        self.root.configure(bg="#282C34")
        self.root.geometry("1000x1000")
        style = ThemedStyle(self.root)
        style.set_theme("equilux")  # Tema oscuro

        self.data = None
        self.columns = []
        self.selected_columns = []
        self.feature_columns = []
        self.target_column = ""
        self.model = None

        # Etiqueta para mostrar el estado del archivo cargado
        self.file_label = tk.Label(
            self.root, text="No se ha cargado ningún archivo", bg='dark gray', fg='white')
        self.file_label.pack(pady=10)

        # Botón para cargar un archivo CSV
        self.load_button = ttk.Button(
            self.root, text="Cargar CSV", command=self.cargar_csv, style="DarkButton.TButton")
        self.load_button.pack(pady=5)

        # Botón para analizar los datos del archivo
        self.analyze_button = ttk.Button(
            self.root, text="Analizar Datos", command=self.analizar_datos,
            state=tk.DISABLED, style="DarkButton.TButton")
        self.analyze_button.pack(pady=5)

        # Etiqueta y lista para seleccionar las columnas de entrenamiento
        self.training_label = tk.Label(
            self.root, text="Columnas de entrenamiento:", bg='dark gray', fg='white')
        self.training_label.pack()
        self.training_listbox = tk.Listbox(
            self.root, selectmode=tk.MULTIPLE, bg='white', fg='black', selectbackground='#0078D7')
        self.training_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        # Etiqueta y combobox para seleccionar la columna objetivo
        self.target_label = tk.Label(
            self.root, text="Columna objetivo:", bg='dark gray', fg='white')
        self.target_label.pack()
        self.target_combobox = ttk.Combobox(
            self.root, state="readonly", style="Combobox.TCombobox")
        self.target_combobox.pack(pady=5, fill=tk.BOTH, expand=True)

        # Etiqueta y combobox para seleccionar el tipo de modelo
        self.model_label = tk.Label(
            self.root, text="Selecciona el tipo de modelo:", bg='dark gray', fg='white')
        self.model_label.pack()
        self.model_combobox = ttk.Combobox(
            self.root, values=["Clasificación", "Predicción"], state="readonly", style="Combobox.TCombobox")
        self.model_combobox.pack(pady=5, fill=tk.BOTH, expand=True)

        # Botón para entrenar el modelo
        self.train_button = ttk.Button(
            self.root, text="Entrenar Modelo", command=self.entrenar_modelo,
            state=tk.DISABLED, style="DarkButton.TButton")
        self.train_button.pack(pady=5)

        # Etiqueta para ingresar los valores a predecir o clasificar
        self.score_label = tk.Label(
            self.root, text="Ingresa los valores para hacer la predicción/clasificación:",
            bg='dark gray', fg='white')
        self.score_label.pack()

        # Diccionario que guarda las entradas para los valores a predecir o clasificar
        self.score_entries = {}
        self.score_frame = tk.Frame(self.root, bg='dark gray')
        self.score_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        # Botón para calcular el score de predicción o clasificación
        self.score_button = ttk.Button(
            self.root, text="Calcular Score", command=self.calcular_puntuacion,
            state=tk.DISABLED, style="DarkButton.TButton")
        self.score_button.pack(pady=5)

        # Marco para mostrar la tabla de mapeo de categorías
        self.mapping_table_frame = tk.Frame(self.root, bg='dark gray')
        self.mapping_table_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        self.apply_button_styles()

    def apply_button_styles(self):
        # Aplicar estilos personalizados a los botones
        style = ThemedStyle(self.root)
        style.configure("DarkButton.TButton", foreground="white", background="#707070",
                        font=("Helvetica", 12, "bold"))
        style.map("DarkButton.TButton",
                  foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', '#404040'), ('active', '#404040')])

        # Estilo personalizado para el combobox
        style.configure("Combobox.TCombobox", foreground="black", background="white",
                        selectforeground="white", selectbackground="#0078D7",
                        fieldbackground="white", font=("Helvetica", 12, "bold"))

    def cargar_csv(self):
        # Función para cargar un archivo CSV
        file_path = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.file_label.config(text="Archivo cargado: " + file_path)
            self.columns = self.data.columns.tolist()
            self.analyze_button.config(state=tk.NORMAL)

    def analizar_datos(self):
        # Función para analizar los datos del archivo cargado
        self.selected_columns = []
        mapping_table_data = []

        for column in self.columns:
            data_type = str(self.data[column].dtype)
            if data_type == "object":
                # Si es una columna de tipo "object", se realiza una codificación numérica
                self.data[column].fillna("", inplace=True)
                label_encoder = LabelEncoder()
                self.data[column] = label_encoder.fit_transform(self.data[column])
                mapping_table_data.extend(
                    [(column, label_encoder.classes_[i], i) for i in range(len(label_encoder.classes_))])
            elif data_type == "float64" or data_type == "int64":
                # Si es una columna numérica, se rellenan los valores faltantes con la media
                self.data[column].fillna(self.data[column].mean(), inplace=True)
            else:
                continue
            self.selected_columns.append(column)

        # Actualización de la lista de columnas de entrenamiento y combobox de la columna objetivo
        self.training_listbox.delete(0, tk.END)
        self.training_listbox.insert(tk.END, *self.selected_columns)
        self.target_combobox.config(values=self.selected_columns, state="readonly")
        self.model_combobox.config(state="readonly")
        self.train_button.config(state=tk.NORMAL)

        # Mostrar la tabla de mapeo de categorías
        self.mostrar_tabla_mapeo(mapping_table_data)

    def mostrar_tabla_mapeo(self, mapping_data):
        # Función para mostrar la tabla de mapeo de categorías en un marco
        scrollbar = tk.Scrollbar(self.mapping_table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        mapping_table = tk.Text(
            self.mapping_table_frame, yscrollcommand=scrollbar.set, bg='#282C34',
            fg='white', insertbackground='white', font=("Helvetica", 10))
        mapping_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        mapping_table.insert(tk.END, "Columna\tValor Antiguo\tValor Nuevo\n")
        for item in mapping_data:
            mapping_table.insert(tk.END, f"{item[0]}\t{item[1]}\t{item[2]}\n")

        mapping_table.config(state=tk.DISABLED)
        scrollbar.config(command=mapping_table.yview)

    def entrenar_modelo(self):
        # Función para entrenar el modelo de clasificación o predicción
        self.feature_columns = self.training_listbox.curselection()
        self.target_column = self.target_combobox.get()

        if not self.feature_columns or not self.target_column:
            messagebox.showwarning(
                "Advertencia", "Debes seleccionar las columnas de entrenamiento y la columna objetivo.")
            return

        self.feature_columns = [self.selected_columns[i] for i in self.feature_columns]

        if self.model_combobox.get() == "Clasificación":
            self.model = RandomForestClassifier()
        else:
            self.model = LinearRegression()

        X = self.data[self.feature_columns]
        y = self.data[self.target_column]

        self.model.fit(X, y)

        messagebox.showinfo("Entrenamiento Completado", "El modelo ha sido entrenado exitosamente.")

        self.crear_entradas_puntuacion()
        self.score_button.config(state=tk.NORMAL)

    def crear_entradas_puntuacion(self):
        # Función para crear las entradas de valores a predecir o clasificar
        for widget in self.score_frame.winfo_children():
            widget.destroy()

        for i, column in enumerate(self.feature_columns):
            label = tk.Label(
                self.score_frame, text=column + ":", bg='#282C34', fg='white')
            label.grid(row=i, column=0, padx=5, pady=5, sticky=tk.E)

            entry = tk.Entry(self.score_frame, bg='#282C34', fg='white')
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.score_entries[column] = entry

    def calcular_puntuacion(self):
        # Función para calcular el score de predicción o clasificación
        score_values = []
        for column in self.feature_columns:
            value = self.score_entries[column].get()
            if value == "":
                value = self.data[column].mean()
            else:
                try:
                    value = float(value)
                except ValueError:
                    messagebox.showerror(
                        "Error", "El valor ingresado para '{}' no es válido.".format(column))
                    return
            score_values.append(value)

        score_data = [score_values]

        if self.model_combobox.get() == "Clasificación":
            prediction = self.model.predict(score_data)[0]
            messagebox.showinfo(
                "Clasificación", "La predicción para los valores ingresados es: '{}'".format(prediction))
        else:
            prediction = self.model.predict(score_data)[0]
            messagebox.showinfo(
                "Predicción", "El resultado de la predicción para los valores ingresados es: '{}'".format(prediction))


if __name__ == "__main__":
    analizador = AnalizadorDatos()
    analizador.root.mainloop()
