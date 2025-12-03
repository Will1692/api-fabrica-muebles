import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent / "src"))

from com.fabrica.muebles.modelo.cliente import Cliente
from com.fabrica.muebles.modelo.proveedor import Proveedor
from com.fabrica.muebles.modelo.produccion import Produccion
from com.fabrica.muebles.dao.cliente_dao import ClienteDAO
from com.fabrica.muebles.dao.proveedor_dao import ProveedorDAO
from com.fabrica.muebles.dao.produccion_dao import ProduccionDAO


def test_clientes():
    print("\nPRUEBA COMPLETA - MODULO CLIENTES\n")

    dao = ClienteDAO()

    print("1. INSERTAR cliente de prueba...")
    cliente = Cliente(
        nombre="Pedro Prueba",
        telefono="3111111111",
        direccion="Calle Prueba 123",
        email="pedro.prueba@test.com"
    )
    if dao.insertar_cliente(cliente):
        print("Cliente insertado")

    print("\n2. CONSULTAR todos los clientes...")
    clientes = dao.consultar_todos()
    print(f"Total de clientes: {len(clientes)}")

    if clientes:
        ultimo_id = clientes[0].id_cliente
        print(f"\n3. CONSULTAR cliente por ID: {ultimo_id}")
        cliente_encontrado = dao.consultar_por_id(ultimo_id)
        if cliente_encontrado:
            print(f"Cliente encontrado: {cliente_encontrado.nombre}")

        print(f"\n4. ACTUALIZAR cliente ID: {ultimo_id}")
        cliente_encontrado.telefono = "3999999999"
        if dao.actualizar_cliente(cliente_encontrado):
            print("Cliente actualizado")


def test_proveedores():
    print("\n\nPRUEBA COMPLETA - MODULO PROVEEDORES\n")

    dao = ProveedorDAO()

    print("1. AGREGAR proveedor de prueba...")
    proveedor = Proveedor(
        nombre="Proveedor Test S.A.",
        contacto="Ana Contacto",
        telefono="3222222222",
        direccion="Av Prueba 456",
        correo="contacto@proveedortest.com"
    )
    if dao.agregar(proveedor):
        print("Proveedor agregado")

    print("\n2. LISTAR todos los proveedores...")
    proveedores = dao.listar()
    print(f"Total de proveedores: {len(proveedores)}")

    if proveedores:
        ultimo_id = proveedores[-1].id
        print(f"\n3. BUSCAR proveedor por ID: {ultimo_id}")
        proveedor_encontrado = dao.buscar(ultimo_id)
        if proveedor_encontrado:
            print(f"Proveedor encontrado: {proveedor_encontrado.nombre}")

        print(f"\n4. ACTUALIZAR proveedor ID: {ultimo_id}")
        proveedor_encontrado.telefono = "3888888888"
        if dao.actualizar(proveedor_encontrado):
            print("Proveedor actualizado")


def test_produccion():
    print("\n\nPRUEBA COMPLETA - MODULO PRODUCCION\n")

    dao = ProduccionDAO()

    print("1. INSERTAR produccion de prueba...")
    produccion = Produccion(
        nombre_producto="Silla Ejecutiva",
        cantidad=50,
        fecha_inicio=date.today(),
        estado="En Proceso"
    )
    if dao.insertar_produccion(produccion):
        print("Produccion insertada")

    print("\n2. CONSULTAR todas las producciones...")
    producciones = dao.consultar_todos()
    print(f"Total de producciones: {len(producciones)}")

    if producciones:
        ultimo_id = producciones[0].id
        print(f"\n3. CONSULTAR produccion por ID: {ultimo_id}")
        prod_encontrada = dao.consultar_por_id(ultimo_id)
        if prod_encontrada:
            print(f"Produccion encontrada: {prod_encontrada.nombre_producto}")

        print(f"\n4. FINALIZAR produccion ID: {ultimo_id}")
        if dao.finalizar_produccion(ultimo_id):
            print("Produccion finalizada")


def main():
    print("\nSUITE DE PRUEBAS COMPLETA")
    print("Sistema de Gestion Fabrica de Muebles\n")

    try:
        test_clientes()
        test_proveedores()
        test_produccion()

        print("\n\nTODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE\n")

    except Exception as e:
        print(f"\nERROR EN LAS PRUEBAS: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()