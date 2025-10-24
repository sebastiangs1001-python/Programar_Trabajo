
import json
with open(r'C:\\Users\\34635\\OneDrive\\Escritorio\\Porgramar\\Programar\\TRABAJO\\almacen-1.json', 'r') as file:
    almacen_data = json.load(file)
with open(r'C:\Users\34635\OneDrive\Escritorio\Porgramar\Programar\TRABAJO\farmacos-1.json', 'r') as file:
    farmacos_data = json.load(file)
with open(r'C:\\Users\\34635\\OneDrive\\Escritorio\\Porgramar\\Programar\\TRABAJO\\pedido-1.json', 'r') as file:
        pedido_data = json.load(file)


#INTERFAZ
# main.py
import json

ruta_almacen = r'C:\\Users\\34635\\OneDrive\\Escritorio\\Porgramar\\Programar\\TRABAJO\\almacen-1.json'
ruta_pedidos = r'C:\Users\34635\OneDrive\Escritorio\Porgramar\Programar\TRABAJO\pedido-1.json'
from Pedido_FF import print_pedidos_linea, procesar, restar_stock_por_pedido

def main():
    procesados = []
    ids_procesados = set()

    while True:
        print('====MAIN MENU=====:')
        print('1 - Información General.')
        print('2 - Estado del Almacén')
        print('3 - Pedidos.')
        print('4 - Informes Históricos')
        print('5 - Salir del programa')

        elegir = input('Elige: ').strip()

        if elegir == '1':
            print('INFO GENERAL')
            input("Presiona Enter para continuar...")

        elif elegir == '2':
            print('1 - Mostrar los módulos del almacén.')
            print('2 - Mostrar el estado de un módulo.')
            subsecc = input('Dime una subseccion ').strip()
            if subsecc == '1':
                with open(ruta_almacen, 'r', encoding='utf-8') as file:
                    almacen_data = json.load(file)
                modulos = almacen_data['almacen']
                print("Módulos disponibles:")
                for modulo in modulos.keys():
                    print(f" - {modulo}")
            elif subsecc == '2':
                from Almacen import mostrar_datos_modulo
                mostrar_datos_modulo(ruta_almacen)
            else:
                print("Sub-opción no válida.")

        elif elegir == '3':
            print('1 - Mostrar los pedidos sin procesar.')
            print('2 - Procesar pedido')
            print('3 - Mostrar los pedidos en marcha')
            print('B - Vuelve al menú anterior')
            sub_3 = input('Dime que quieres hacer con los pedidos: ').strip().upper()

            with open(ruta_pedidos, 'r', encoding='utf-8') as f:
                pedidos_data = json.load(f)   # SIEMPRE ESTE NOMBRE
            with open(ruta_almacen, 'r', encoding='utf-8') as f:
                almacen_data = json.load(f)

            if sub_3 == '1':
                print_pedidos_linea(pedidos_data)

            elif sub_3 == '2':
                pedido_id = input("Introduce el ID del pedido que quieres procesar: ").strip()
                restar_stock_por_pedido(pedido_id, pedidos_data,almacen_data,procesados)
                Mover = procesar(pedidos_data, procesados, ids_procesados, pedido_id)
                if Mover:
                    with open(ruta_almacen, 'w', encoding='utf-8') as f:
                        json.dump(almacen_data, f, indent=4, ensure_ascii=False)
                    print("Stock actualizado guardado en almacen-2.json")

            elif sub_3 == '3':
                print(f'Lista de Procesados: {procesados}')

            elif sub_3 == 'B':
                continue
            else:
                print("Sub-opción no válida.")

        elif elegir == '4':
            print('Informes históricos')
            input("Presiona Enter para continuar...")

        elif elegir == '5':
            print('Chao')
            break

        else:
            print('Opción no válida, por favor elige un número del 1 al 5.')
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()