import tkinter as tk

from tkinter import ttk

from tkinter import messagebox

import sqlite3

import csv


# CONEXION CON SQLITE

conexion = sqlite3.connect("inventario2.db")
cursor = conexion.cursor()

# CREAR TABLA SI NO EXISTE

cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL
    )
""")

conexion.commit()

STOCK_MINIMO = 10

ventana = tk.Tk()

ventana.title("Sistema de Gestion de Productos")
ventana.geometry("800x800")
ventana.resizable(False,False)

#estilo de la tabla

estilo =ttk.Style()

estilo.theme_use("clam")

estilo.configure(
    "Treeview",
    font=("Calibri",11),
    rowheight=28,
    background="white",
    foreground="black",
    fieldbackground="white"
    
)

estilo.configure(
    "Treeview.Heading",
    font=("Calibri",11,"bold"),
    background="#024987",
    foreground="white"
)


#Titulo principal

titulo =tk.Label(
    ventana,
    text="GESTION DE PRODUCTOS",
    font=("Calibri", 15 , "bold"),
    fg="white",
    bg="#024987"

)

titulo.pack(fill="x", pady=20)

#Subtitulo

subtitulo = tk.Label(
    ventana,
    text="Sistema de administracion de inventario",
    font=("Calibri", 10)
)

subtitulo.pack(pady=10)

#contenedor formulario

formulario = tk.Frame(ventana)
formulario.pack(pady=10)




#Campo nombre

tk.Label(formulario, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)

entrada_nombre =tk.Entry(formulario)
entrada_nombre.grid(row=0, column=1, padx=10, pady=5)


#Campo categoria

tk.Label(formulario, text="Categoria:").grid(row=1, column=0, padx=10, pady=5)

entrada_categoria = tk.Entry(formulario)
entrada_categoria.grid(row=1, column=1, padx=10, pady=5)

# Campo cantidad
tk.Label(formulario, text="Cantidad:").grid(row=2, column=0, padx=10, pady=5)

entrada_cantidad = tk.Entry(formulario)
entrada_cantidad.grid(row=2, column=1, padx=10, pady=5)

#Campo precio

tk.Label(formulario, text="Precio:").grid(row=3, column=0, padx=10, pady=5)
entrada_precio = tk.Entry(formulario)
entrada_precio.grid(row=3, column=1, padx=10, pady=5)


# tabla de productos

#Frame de la tabla

frame_tabla = tk.Frame(ventana)
frame_tabla.pack(pady=10)

tabla = ttk.Treeview(
    frame_tabla,
    columns=("ID", "Nombre", "Categoria", "Cantidad", "Precio"),
    show="headings",
    height=8

)

# Encabezados

tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Categoria", text="Categoria")
tabla.heading("Cantidad", text="Cantidad")
tabla.heading("Precio", text="Precio")


# Columnas

tabla.column("ID", width=50, anchor= "center")
tabla.column("Nombre", width=150)
tabla.column("Categoria", width=150)
tabla.column("Cantidad", width=100, anchor="center")
tabla.column("Precio", width=100, anchor="center")

# Mostrar tabla

tabla.pack(pady=20)

#Buscador
buscador = tk.Frame(ventana)
buscador.pack(pady=10)

entrada_busqueda = tk.Entry(buscador, width=30)
entrada_busqueda.grid(row=0, column=0, padx=5)

#funcion listar productos

def listar_productos():

    # Limpiar tabla
    for item in tabla.get_children():
        tabla.delete(item)

    # Consultar productos en SQLite
    cursor.execute("""
        SELECT id, nombre, categoria, cantidad, precio
        FROM productos
    """)

    registros = cursor.fetchall()

    # Mostrar registros en Treeview
    for producto in registros:
        producto = list(producto)
        producto[4] = int(producto[4])

        tabla.insert("", tk.END, values=producto)

def buscar_producto():

    nombre_buscado = entrada_busqueda.get().strip()

    if not nombre_buscado:
        messagebox.showwarning(
            "Busqueda",
            "Ingrese nombre de producto."
        )
        return

    # Limpiar Treeview

    for item in tabla.get_children():
        tabla.delete(item)

    # Buscar producto en SQLite

    cursor.execute("""
        SELECT id, nombre, categoria, cantidad, precio
        FROM productos
        WHERE nombre LIKE ?
    """, (f"%{nombre_buscado}%",))

    registros = cursor.fetchall()

    # Mostrar resultados

    if registros:

        for producto in registros:
            tabla.insert(
                "",
                tk.END,
                values=producto
            )

    else:
        messagebox.showinfo(
            "Busqueda",
            "No se encontraron productos."
        )


def mostrar_todos():

    entrada_busqueda.delete(0, tk.END)

    listar_productos()


def reporte_stock_minimo():

    # Limpiar Treeview

    for item in tabla.get_children():
        tabla.delete(item)

    # Consultar productos con stock minimo

    cursor.execute("""
        SELECT id, nombre, categoria, cantidad, precio
        FROM productos
        WHERE cantidad <= ?
    """, (STOCK_MINIMO,))

    registros = cursor.fetchall()

    # Mostrar resultados

    if registros:

        for producto in registros:

            tabla.insert(
                "",
                tk.END,
                values=producto
            )

    else:

        messagebox.showinfo(
            "Stock minimo",
            "No hay productos con stock minimo."
        )

def exportar_csv():

    cursor.execute("""
        SELECT id, nombre, categoria, cantidad, precio
        FROM productos
    """)

    registros = cursor.fetchall()

    if not registros:
        messagebox.showinfo(
            "Exportar",
            "No hay productos para exportar."
        )
        return

    with open("inventario_exportado.csv", "w", newline="", encoding="utf-8-sig") as archivo:

        escritor = csv.writer(archivo, delimiter=";")

        escritor.writerow([
            "ID",
            "Nombre",
            "Categoria",
            "Cantidad",
            "Precio"
        ])

        escritor.writerows(registros)

    messagebox.showinfo(
        "Exportar",
        "Inventario exportado correctamente."
    )
    
def seleccionar_producto(event):
    seleccionado = tabla.selection()

    if seleccionado:

        producto = tabla.item(seleccionado[0], "values")

        entrada_nombre.delete(0, tk.END)
        entrada_categoria.delete(0, tk.END)
        entrada_cantidad.delete(0, tk.END)
        entrada_precio.delete(0, tk.END)

        entrada_nombre.insert(0, producto[1])
        entrada_categoria.insert(0, producto[2])
        entrada_cantidad.insert(0, producto[3])
        entrada_precio.insert(0, producto[4])

#asociar evento tabla
tabla.bind("<<TreeviewSelect>>", seleccionar_producto)

#funcion eliminar producto


def eliminar_producto():

    seleccionado = tabla.selection()

    if not seleccionado:
        messagebox.showwarning(
            "Seleccion requerida",
            "Seleccione un producto para eliminar."
        )
        return

    # Obtener producto seleccionado

    producto = tabla.item(seleccionado[0], "values")

    id_producto = int(producto[0])

    nombre_producto = producto[1]

    # Confirmar eliminación

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Desea eliminar el producto {nombre_producto}?"
    )

    if not confirmar:
        return

    # Eliminar registro de SQLite

    cursor.execute("""
        DELETE FROM productos
        WHERE id = ?
    """, (id_producto,))

    conexion.commit()

    # Actualizar Treeview

    listar_productos()

    # Limpiar formulario

    entrada_nombre.delete(0, tk.END)
    entrada_categoria.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)
    entrada_precio.delete(0, tk.END)

    messagebox.showinfo(
        "Eliminación",
        "Producto eliminado correctamente."
    )


def agregar_producto():

    nombre = entrada_nombre.get().strip()
    categoria = entrada_categoria.get().strip()
    cantidad_texto = entrada_cantidad.get().strip()
    precio_texto = entrada_precio.get().strip()

    # Validar campos vacios

    if not nombre or not categoria or not cantidad_texto or not precio_texto:
        messagebox.showwarning(
            "Campos incompletos",
            "Debe completar todos los campos."
        )
        return

    # Validar datos numericos

    try:
        cantidad = int(cantidad_texto)
        precio = int(precio_texto)

    except ValueError:
        messagebox.showerror(
            "Error de datos",
            "Cantidad y Precio deben ser números enteros."
        )
        return

    # Validar valores negativos

    if cantidad < 0 or precio < 0:
        messagebox.showwarning(
            "Valores incorrectos",
            "Cantidad y Precio no pueden ser negativos."
        )
        return

    # Guardar producto en SQLite

    cursor.execute("""
        INSERT INTO productos (nombre, categoria, cantidad, precio)
        VALUES (?, ?, ?, ?)
    """, (nombre, categoria, cantidad, precio))

    conexion.commit()

    # Actualizar Treeview

    listar_productos()

    # Limpiar formulario

    entrada_nombre.delete(0, tk.END)
    entrada_categoria.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)
    entrada_precio.delete(0, tk.END)

    messagebox.showinfo(
        "Excelente",
        "Producto agregado correctamente."
    )



def actualizar_producto():

    seleccionado = tabla.selection()

    if not seleccionado:
        messagebox.showwarning(
            "Seleccion requerida",
            "Seleccione el producto a actualizar."
        )
        return

    # Obtener datos del producto seleccionado

    producto = tabla.item(seleccionado[0], "values")

    id_producto = int(producto[0])

    # Obtener datos del formulario

    nombre = entrada_nombre.get().strip()
    categoria = entrada_categoria.get().strip()
    cantidad_texto = entrada_cantidad.get().strip()
    precio_texto = entrada_precio.get().strip()

    # Validar campos vacios

    if not nombre or not categoria or not cantidad_texto or not precio_texto:
        messagebox.showwarning(
            "Campos incompletos",
            "Debe completar todos los campos."
        )
        return

    # Validar datos numericos

    try:
        cantidad = int(cantidad_texto)
        precio = int(precio_texto)

    except ValueError:
        messagebox.showerror(
            "Error en los datos",
            "Cantidad y Precio deben ser numeros enteros."
        )
        return

    # Validar valores negativos

    if cantidad < 0 or precio < 0:
        messagebox.showwarning(
            "Valores incorrectos",
            "Cantidad y Precio no pueden ser negativos."
        )
        return

    # Actualizar registro en SQLite

    cursor.execute("""
        UPDATE productos
        SET nombre = ?,
            categoria = ?,
            cantidad = ?,
            precio = ?
        WHERE id = ?
    """, (nombre, categoria, cantidad, precio, id_producto))

    conexion.commit()

    # Actualizar Treeview

    listar_productos()

    # Limpiar formulario

    entrada_nombre.delete(0, tk.END)
    entrada_categoria.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)
    entrada_precio.delete(0, tk.END)

    messagebox.showinfo(
        "Exito",
        "Producto actualizado correctamente."
    )

def cerrar_aplicacion():
    conexion.close()
    ventana.destroy()




#Frame de botones ppales

frame_botones =tk.Frame(ventana)
frame_botones.pack(pady=10)


# BOTON AGREGAR
boton_agregar = tk.Button(
    frame_botones,
    text="Agregar producto",
    command=agregar_producto,
    bg="green",
    fg="white"
)

boton_agregar.pack(side="left", padx=5, pady=10)


# BOTON ELIMINAR
boton_eliminar = tk.Button(
    frame_botones,
    text="Eliminar producto",
    command=eliminar_producto,
    bg="red",
    fg="white"
)

boton_eliminar.pack(side="left", padx=5, pady=10)

# BOTON ACTUALIZAR
boton_actualizar = tk.Button(
    frame_botones,
    text="Actualizar producto",
    command=actualizar_producto,
    bg="blue",
    fg="white"
)
boton_actualizar.pack(side="left", padx=5, pady=10)
#BOTON BUSCAR

boton_buscar = tk.Button(
    buscador,
    text="Buscar",
    command=buscar_producto
)

boton_buscar.grid(row=0, column=1, padx=5)


#BOTON MOSTRAR TODOS

boton_mostrar = tk.Button(
    buscador,
    text="Mostrar todos",
    command=mostrar_todos
)

boton_mostrar.grid(row=0, column=2, padx=5)

#BOTON STOCK

boton_stock = tk.Button(
    frame_botones,
    text="Reporte stock mínimo",
    command=reporte_stock_minimo
)

boton_stock.pack(side="left",padx=5, pady=10)



boton_actualizar.pack(pady=5)


#BOTON SALIR

boton_salir = tk.Button(
    frame_botones,
    text="Salir",
    command=cerrar_aplicacion,
)

boton_salir.pack(side="left",padx=5, pady=10)

boton_exportar = tk.Button(
    frame_botones,
    text="Exportar CSV",
    command=exportar_csv,
    bg="green",
    fg="white"
)

boton_exportar.pack(pady=5)

# CARGAR PRODUCTOS
listar_productos()


# INICIAR VENTANA
ventana.mainloop()
