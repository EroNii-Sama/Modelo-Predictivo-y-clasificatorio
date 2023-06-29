Analizador de Datos - Documentación

Este proyecto es un analizador de datos implementado en Python utilizando la biblioteca Tkinter para la interfaz gráfica, Pandas para la manipulación y análisis de datos, y Scikit-learn para la clasificación y predicción de datos.

El analizador de datos consta de las siguientes características principales:
Cargar un archivo CSV

Permite al usuario cargar un archivo CSV desde su sistema de archivos local. Una vez cargado, los datos del archivo se almacenan en un objeto Pandas DataFrame para su posterior procesamiento y análisis.
Analizar los datos del archivo

Una vez cargado el archivo CSV, el usuario puede analizar los datos para realizar tareas específicas de preparación de datos. El análisis incluye lo siguiente:

    Codificación numérica de columnas de tipo "object": Si una columna contiene valores de tipo "object" (como cadenas), se realiza una codificación numérica utilizando la clase LabelEncoder de Scikit-learn. Esto permite que los algoritmos de clasificación o predicción trabajen con variables numéricas en lugar de cadenas.

    Relleno de valores faltantes en columnas numéricas: Si una columna contiene valores numéricos y tiene celdas vacías, se rellenan los valores faltantes con la media de la columna.

    Visualización de la tabla de mapeo de categorías: Se muestra una tabla que indica la columna, el valor original y el valor codificado para las columnas que se codificaron numéricamente. Esto proporciona información sobre cómo se han transformado los datos.

Entrenar un modelo

Después de analizar los datos, el usuario puede seleccionar las columnas de entrenamiento y la columna objetivo para entrenar un modelo de clasificación o predicción. Las características de esta funcionalidad incluyen:

    Selección de columnas de entrenamiento: El usuario puede seleccionar una o varias columnas para utilizar como características de entrenamiento. Estas columnas deben ser numéricas después del análisis de datos realizado anteriormente.

    Selección de columna objetivo: El usuario elige una columna para utilizar como variable objetivo. Esta columna debe ser numérica para los modelos de predicción, y puede ser numérica o categórica para los modelos de clasificación.

    Tipos de modelo: El usuario puede elegir entre dos tipos de modelo: clasificación o predicción. Para la clasificación, se utiliza un clasificador de bosque aleatorio (RandomForestClassifier) de Scikit-learn. Para la predicción, se utiliza una regresión lineal (LinearRegression) de Scikit-learn.

    Entrenamiento del modelo: Una vez seleccionadas las columnas de entrenamiento y la columna objetivo, el usuario puede entrenar el modelo con los datos proporcionados. El modelo se ajusta utilizando el algoritmo seleccionado y los datos correspondientes.

Calcular puntuación

Después de entrenar el modelo, el usuario puede ingresar valores para hacer una predicción o clasificación utilizando el modelo entrenado. Las características de esta funcionalidad son:

    Entrada de valores a predecir o clasificar: El usuario ingresa valores para cada columna de entrenamiento seleccionada. Estos valores pueden ser numéricos o se puede dejar en blanco para utilizar el valor medio de la columna.

    Cálculo de la puntuación: El modelo realiza la predicción o clasificación utilizando los valores ingresados por el usuario y muestra el resultado en una ventana emergente.

Requisitos del entorno de desarrollo

Para ejecutar este proyecto en su entorno de desarrollo local, debe tener instalado lo siguiente:

    Python 3.x: El lenguaje de programación utilizado para implementar el analizador de datos.
    Bibliotecas: Asegúrese de tener instaladas las siguientes bibliotecas de Python antes de ejecutar el código:
        tkinter: Biblioteca estándar de Python para crear interfaces gráficas.
        pandas: Biblioteca para el análisis y manipulación de datos.
        scikit-learn: Biblioteca para el aprendizaje automático y la minería de datos.
        ttkthemes: Biblioteca para aplicar temas a las interfaces gráficas de tkinter.

Instrucciones de ejecución

Siga estos pasos para ejecutar el proyecto en su entorno de desarrollo local:

    Clone el repositorio del proyecto desde GitHub.
    Asegúrese de tener todas las bibliotecas requeridas instaladas en su entorno de Python.
    Ejecute el archivo Python analizador_datos.py.
    La interfaz gráfica del analizador de datos se abrirá en una ventana separada.
    Siga las instrucciones en la interfaz gráfica para cargar un archivo CSV, analizar los datos, entrenar un modelo y realizar predicciones o clasificaciones.

Espero que esta documentación sea útil para comprender el código y las funcionalidades del analizador de datos. Si tiene alguna pregunta adicional, no dude en hacerla.
