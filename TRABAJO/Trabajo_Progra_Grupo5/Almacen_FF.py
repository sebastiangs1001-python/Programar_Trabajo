#ALMACEN


import json
with open(r'C:\\Users\\34635\\OneDrive\\Escritorio\\Porgramar\\Programar\\TRABAJO\\almacen-1.json', 'r') as file:
    almacen_data = json.load(file)
ruta_almacen = r'C:\\Users\\34635\\OneDrive\\Escritorio\\Porgramar\\Programar\\TRABAJO\\almacen-1.json'

def mostrar_datos_modulo(ruta_almacen):
    with open(ruta_almacen, 'r') as file:
        almacen_data = json.load(file)

modulos = almacen_data['almacen']
print("Módulos disponibles:")
for modulo in modulos.keys():
    print(f" - {modulo}")

P_Alma = input ('A que Modulo quiere acceder:').strip()

if P_Alma in modulos:
    print(f'Datos Modulo {P_Alma}')
    print(json.dumps(modulos[P_Alma], indent=1, ensure_ascii=False))
else:
    print('NO EXISTE')

