import MetaTrader5 as mt5
from datetime import datetime
import time
import requests

# Inicializar MetaTrader 5
if not mt5.initialize():
    print("Error al inicializar MetaTrader 5")
    print(mt5.last_error())  # Mostrar el error específico
    exit()  # Salir si no se puede inicializar

# Función para obtener operaciones cerradas
def obtener_operaciones_cerradas(fecha_inicio, fecha_fin):
    historial = mt5.history_deals_get(fecha_inicio, fecha_fin)
    if historial is None:
        print("No se encontraron operaciones cerradas.")
        print("Error:", mt5.last_error())  # Mostrar el error si ocurre
        return []
    print(f"Se encontraron {len(historial)} operaciones cerradas:")
    for op in historial:
        print(f"Ticket: {op.ticket}, Símbolo: {op.symbol}, Profit: {op.profit}")
    return historial

# Función para obtener información de la cuenta
def obtener_informacion_cuenta():
    cuenta = mt5.account_info()
    if cuenta is None:
        print("No se pudo obtener la información de la cuenta.")
        print("Error:", mt5.last_error())  # Mostrar el error si ocurre
        return None
    print("Información de la cuenta obtenida con éxito:")
    print(f"ID de la cuenta: {cuenta.login}")
    print(f"Nombre del servidor: {cuenta.server}")
    print(f"Saldo: {cuenta.balance}")
    print(f"Margen disponible: {cuenta.margin_free}")
    print(f"Equidad: {cuenta.equity}")
    print(f"Ganancia flotante: {cuenta.profit}")
    print(f"Nivel de margen: {cuenta.margin_level}")
    print(f"Estado de la cuenta: {'En trading' if cuenta.trade_allowed else 'Trading deshabilitado'}")
    return cuenta

# Establecer el rango de fechas para las operaciones cerradas
fecha_inicio = datetime(2023, 1, 1)
fecha_fin = datetime.now()

# Llamar a las funciones
print("\n=== Operaciones Cerradas ===")
operaciones_cerradas = obtener_operaciones_cerradas(fecha_inicio, fecha_fin)

print("\n=== Información de la Cuenta ===")
informacion_cuenta = obtener_informacion_cuenta()

# Cerrar la conexión
mt5.shutdown()
print("\nConexión a MetaTrader 5 cerrada.")

import asyncio
from telegram import Bot

TELEGRAM_TOKEN = "7774991841:AAEh3I9s2tC-Qo3rO-H64UO1MANAIYpc4lM"
CHAT_ID = "6278975175"

async def send_message():
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        # Puedes agregar el código que desees aquí para enviar otro tipo de mensaje o ejecutar otra acción
        print("El bot está listo para recibir y enviar mensajes.")
    except Exception as e:
        print(f"Error: {e}")

# Llamada a la función asincrónica
asyncio.run(send_message())

import MetaTrader5 as mt5

# Inicializar MetaTrader 5
if not mt5.initialize():
    print("Error al inicializar MetaTrader 5")
    print(mt5.last_error())  # Mostrar el error específico
    exit()  # Salir si no se puede inicializar

# Función para obtener información de las operaciones abiertas
def obtener_operaciones_abiertas():
    operaciones = mt5.positions_get()
    if operaciones is None:
        print("No se encontraron operaciones abiertas.")
        print("Error:", mt5.last_error())  # Mostrar el error si ocurre
        return []
    elif len(operaciones) > 0:
        print(f"Se encontraron {len(operaciones)} operaciones abiertas:")
        for op in operaciones:
            print(f"""
            Ticket: {op.ticket}
            Símbolo: {op.symbol}
            Volumen: {op.volume}
            Precio de Apertura: {op.price_open}
            Stop Loss: {op.sl}
            Take Profit: {op.tp}
            Ganancia Flotante: {op.profit}
            """)
        return operaciones
    else:
        print("No hay operaciones abiertas actualmente.")
        return []

# Llamar a la función
print("\n=== Operaciones Abiertas ===")
operaciones_abiertas = obtener_operaciones_abiertas()

# Cerrar la conexión
mt5.shutdown()
print("\nConexión a MetaTrader 5 cerrada.")

import MetaTrader5 as mt5
from datetime import datetime

# Inicializar MetaTrader 5
if not mt5.initialize():
    print("Error al inicializar MetaTrader 5")
    print(mt5.last_error())  # Mostrar el error específico
    exit()

# Función para obtener información financiera de la cuenta
def obtener_informacion_financiera():
    # Información de la cuenta
    cuenta = mt5.account_info()
    if cuenta is None:
        print("No se pudo obtener la información de la cuenta.")
        print("Error:", mt5.last_error())
        return

    # Mostrar el estado de la cuenta primero
    print("\n=== Estado de la Cuenta ===")
    print(f"Estado de la cuenta: {'En trading' if cuenta.trade_allowed else 'Trading deshabilitado'}")

    # Obtener historial de operaciones cerradas
    fecha_inicio = datetime(2023, 1, 1)  # Fecha de inicio para las operaciones cerradas
    fecha_fin = datetime.now()  # Fecha actual
    historial = mt5.history_deals_get(fecha_inicio, fecha_fin)
    if historial is None:
        print("No se pudo obtener el historial de operaciones.")
        print("Error:", mt5.last_error())
        return

    # Mostrar resultados de la cuenta
    total_swap = 0.0
    total_comision = 0.0
    total_depositos = 0.0
    total_perdida_o_beneficio = 0.0

    for operacion in historial:
        total_swap += operacion.swap  # Swap acumulado
        total_comision += operacion.commission  # Comisión acumulada
        total_perdida_o_beneficio += operacion.profit  # Beneficio o pérdida acumulado

        # Identificar depósitos y créditos
        if operacion.type == mt5.DEAL_TYPE_BALANCE or operacion.type == mt5.DEAL_TYPE_CREDIT:
            total_depositos += operacion.profit  # Solo considerar los depósitos (no ganancias/pérdidas)

    # Cálculos adicionales
    balance = cuenta.equity - total_depositos  # Cálculo del balance como equidad menos depósito

    # Beneficio/Pérdida total (cerradas): balance - comisión total - swap
    beneficio_o_perdida_total = balance - total_comision - total_swap

    # Mostrar resultados finales
    print("\n=== Información Financiera de la Cuenta ===")
    print(f"Balance (calculado): {balance:.2f}")  # Balance calculado
    print(f"Equidad: {cuenta.equity:.2f}")  # Equidad
    print(f"Swap acumulado: {total_swap:.2f}")  # Swap acumulado
    print(f"Comisiones totales: {total_comision:.2f}")  # Comisión acumulada
    print(f"Depósitos realizados: {total_depositos:.2f}")  # Depósitos realizados
    print(f"Beneficio/Pérdida total (cerradas): {beneficio_o_perdida_total:.2f}")  # Beneficio/Pérdida total

# Llamar a la función para obtener la información
obtener_informacion_financiera()

# Cerrar la conexión
mt5.shutdown()
print("\nConexión a MetaTrader 5 cerrada.")

import sqlite3
from datetime import datetime

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('bot_inversiones.db')
cursor = conn.cursor()

# Función para crear las tablas
def crear_tablas():
    # Crear tabla de operaciones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS operaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        par_divisa TEXT NOT NULL,
        tipo_operacion TEXT NOT NULL, 
        tamaño REAL NOT NULL,
        precio_apertura REAL NOT NULL,
        precio_cierre REAL NOT NULL,
        fecha_apertura DATETIME NOT NULL,
        fecha_cierre DATETIME,
        beneficio_perdida REAL,
        comision REAL,
        swap REAL,
        estado TEXT NOT NULL
    )
    ''')

    # Crear tabla de patrones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patrones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_patron TEXT NOT NULL,
        par_divisa TEXT NOT NULL,
        fecha_deteccion DATETIME NOT NULL,
        detalles TEXT
    )
    ''')

    # Crear tabla de configuraciones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS configuraciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parametro TEXT NOT NULL,
        valor TEXT NOT NULL
    )
    ''')

    # Guardar cambios
    conn.commit()

# Función para insertar una operación
def insertar_operacion(par_divisa, tipo_operacion, tamaño, precio_apertura, precio_cierre, fecha_apertura, fecha_cierre, beneficio_perdida, comision, swap, estado):
    cursor.execute('''
    INSERT INTO operaciones (par_divisa, tipo_operacion, tamaño, precio_apertura, precio_cierre, fecha_apertura, fecha_cierre, beneficio_perdida, comision, swap, estado)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (par_divisa, tipo_operacion, tamaño, precio_apertura, precio_cierre, fecha_apertura, fecha_cierre, beneficio_perdida, comision, swap, estado))
    conn.commit()

# Función para insertar un patrón
def insertar_patron(tipo_patron, par_divisa, detalles):
    fecha_deteccion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO patrones (tipo_patron, par_divisa, fecha_deteccion, detalles)
    VALUES (?, ?, ?, ?)
    ''', (tipo_patron, par_divisa, fecha_deteccion, detalles))
    conn.commit()

# Función para insertar configuración
def insertar_configuracion(parametro, valor):
    cursor.execute('''
    INSERT INTO configuraciones (parametro, valor)
    VALUES (?, ?)
    ''', (parametro, valor))
    conn.commit()

# Función para obtener todas las operaciones cerradas
def obtener_operaciones_cerradas():
    cursor.execute('SELECT * FROM operaciones WHERE estado = "cerrada"')
    return cursor.fetchall()

# Función para obtener los patrones detectados en un par de divisa
def obtener_patrones(par_divisa):
    cursor.execute('SELECT * FROM patrones WHERE par_divisa = ?', (par_divisa,))
    return cursor.fetchall()

# Función para obtener una configuración
def obtener_configuracion(parametro):
    cursor.execute('SELECT valor FROM configuraciones WHERE parametro = ?', (parametro,))
    return cursor.fetchone()

# Crear las tablas si no existen
crear_tablas()

# Ejemplo de inserción de datos (puedes modificar según lo que necesites)
insertar_operacion('EURUSD', 'compra', 0.1, 1.1000, 1.1050, '2025-01-13 10:00:00', '2025-01-13 10:30:00', 50.0, 1.2, 0.5, 'cerrada')
insertar_patron('martillo', 'EURUSD', 'Patrón de martillo detectado en el gráfico.')
insertar_configuracion('riesgo_maximo', '2%')

# Ejemplo de consulta de datos
operaciones_cerradas = obtener_operaciones_cerradas()
print("Operaciones Cerradas:")
for operacion in operaciones_cerradas:
    print(operacion)

patrones_detectados = obtener_patrones('EURUSD')
print("\nPatrones Detectados en EURUSD:")
for patron in patrones_detectados:
    print(patron)

configuracion_riesgo = obtener_configuracion('riesgo_maximo')
print("\nConfiguración de Riesgo Máximo:")
print(configuracion_riesgo)

# Cerrar la conexión
conn.close()
