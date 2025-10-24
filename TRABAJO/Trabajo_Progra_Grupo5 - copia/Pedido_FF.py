
import json
with open(r'C:\Users\34635\OneDrive\Escritorio\Porgramar\Programar\TRABAJO\pedido-1.json', 'r') as file:
    pedidos_data = json.load(file)
ruta_pedidos = r'C:\Users\34635\OneDrive\Escritorio\Porgramar\Programar\TRABAJO\pedido-1.json'


import json
with open(r'C:\\Users\\34635\\OneDrive\\Escritorio\\Porgramar\\Programar\\TRABAJO\\almacen-1.json', 'r') as file:
    almacen_data = json.load(file)
ruta_almacen = r'C:\\Users\\34635\\OneDrive\\Escritorio\\Porgramar\\Programar\\TRABAJO\\almacen-1.json'


import json
from pathlib import Path

from datetime import datetime, timedelta

# Cargar JSON
with open(ruta_pedidos, "r", encoding="utf-8") as f:
    pedidos = json.load(f)

#Imprimir todos los pedidos
def print_pedidos_linea(pedidos):
    sin_procesar =[]
    for i, pedido in enumerate(pedidos, start=1):

        P_id = pedido.get("pedido_id") or f"(sin id #{i})"

        fecha = pedido.get("fecha", "-")

        cliente = (pedido.get("cliente") or {}).get("nombre", "Desconocido")

        productos = pedido.get("productos") or []

        productos_txt = "; ".join(
            f"{p.get('nombre', '?')} x{p.get('unidades', 0)}" for p in productos
        ) or "(sin productos)"
        sin_procesar.append(pedido)
        print(f"{P_id} | {fecha} | {cliente} | {productos_txt}")
    return sin_procesar

print_pedidos_linea(pedidos)

#Procesado de pedidos
procesados = []
ids_procesados = set()  # para no duplicar(set solo unicos)

def procesar(pedidos, procesados, ids_procesados, pedido_id):
    pid_busca = pedido_id.strip()

    # Busca índice #Next:Devuelve el 1º que encuentra
    idp = next((i for i, p in enumerate(pedidos)
                if str(p.get("pedido_id", "")).strip() == pid_busca), None)

    if idp is None:
        print(f"No se encontró el pedido con id '{pid_busca}'.")
        return False

    pid_norm = str(pedidos[idp].get("pedido_id", "")).strip()
    if pid_norm in ids_procesados:
        print(f"El pedido {pid_norm} ya estaba en 'procesados'.")
        return False

    # Sacarlo CUIDADO.POP LOS ELIMINA DEL JSON
    pedido = pedidos.pop(idp)        
    # Añadirlo a procesados
    procesados.append(pedido)
    ids_procesados.add(pid_norm)
    print(f"Añadido pedido {pid_norm} a 'procesados'.")
    return True


def restar_stock_por_pedido(pedido_id, pedidos_data, almacen_data, procesados):

    #Busca el pedido
    lista_pedidos = pedidos_data if isinstance(pedidos_data, list) else pedidos_data.get("pedidos", [])
    pedido = next((p for p in lista_pedidos if str(p.get("pedido_id")) == str(pedido_id)), None)
    if not pedido:
        print(f"Pedido {pedido_id} no encontrado.")
        return
    #Busca en el almacen
    modulos = almacen_data.get("almacen", {})
    if not modulos:
        print("No hay módulos en el almacén.")
        return

    unidades_actualizadas = {}
    print(f"\nProcesando pedido {pedido_id}...")

# Por cada producto del pedido
    for item in (pedido.get("productos") or []):
        codigo = item.get("codigo")
        unidades_pedidas = (item.get("unidades", 0))
        unidades_restadas = 0

        # Stock total antes y faltantes
        stock_total = sum((m.get("stock", {}).get(codigo, 0) for m in modulos.values()))
        faltan = max(0, unidades_pedidas - stock_total)

        # +100 ANTES
        reponer = 0
        if faltan > 0:
            paquetes = (faltan + 99) // 100  # redondeo hacia arriba
            reponer = paquetes*100 #La suma se me rompia
            mod_id, mod_dest = next(iter(modulos.items()))  # 1º módulo
            mod_dest.setdefault("stock", {})
            mod_dest["stock"][codigo] = mod_dest["stock"].get(codigo, 0) + reponer
            print(f"\nReposición automática: +{reponer} uds de {codigo} en {mod_id} (faltaban {faltan}).")

        # Restar almacen
        por_retirar = unidades_pedidas
        for mid, m in modulos.items():
            if por_retirar == 0:
                break
            sdict = m.setdefault("stock", {})
            stock_mod = sdict.get(codigo, 0)
            mover = min(stock_mod, por_retirar)
            #SI HAY EN EL ALMACEN SE RESTAN
            if mover > 0:
                nuevo_stock = stock_mod - mover
                if nuevo_stock < 0:
                    nuevo_stock += 100  # sumar 100 si sale negativo
                sdict[codigo] = nuevo_stock
                por_retirar -= mover
                unidades_restadas += mover
                if sdict[codigo] == 0:
                    del sdict[codigo]

            faltan_tras_resta = por_retirar  
        # Stock Final
            stock_total_final = sum((m.get("stock", {}).get(codigo, 0) for m in modulos.values()))
            unidades_actualizadas[codigo] = stock_total_final

        # Mostrar (DENTRO del bucle)
        print(f"\n Producto: {codigo}")
        print(f"   - Unidades pedidas: {unidades_pedidas}")
        print(f"   - Restadas del almacén: {unidades_restadas}")
        print(f"   - Faltan por pedir a fábrica: {faltan_tras_resta}")
        print(f"   - Stock disponible tras reposición: {stock_total_final}")

    # Una sola vez por pedido (FUERA del bucle)
    procesados.append(pedido_id)

    print(f"\nStock actualizado para el pedido {pedido_id}.")
    print("Resumen de unidades finales por producto:")
    for cod, nuevo_stock in unidades_actualizadas.items():
        print(f"   - {cod}: {nuevo_stock} unidades en almacén")


def _stock_total_disponible(almacen_data, codigo):
    modulos = almacen_data.get("almacen", {})
    return sum(int(m.get("stock", {}).get(codigo, 0)) for m in modulos.values())

def _parse_fecha_iso(fecha_txt):
    try:
        return datetime.strptime(fecha_txt, "%Y-%m-%d").date()
    except Exception:
        return datetime.today().date()