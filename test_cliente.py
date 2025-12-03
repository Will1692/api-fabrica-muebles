import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from com.fabrica.muebles.modelo.cliente import Cliente
from com.fabrica.muebles.dao.cliente_dao import ClienteDAO


def main():
    print("=" * 60)
    print("PRUEBA DE OPERACIONES CRUD - CLIENTES")
    print("=" * 60)

    dao = ClienteDAO()

    # 1. Insertar un cliente
    print("\n1. INSERTAR CLIENTE")
    cliente = Cliente(
        nombre="Juan Pérez",
        telefono="3001234567",
        direccion="Calle 123 #45-67",
        email="juan.perez@email.com"
    )

    if dao.insertar_cliente(cliente):
        print("✅ Cliente insertado exitosamente")

    # 2. Consultar todos
    print("\n2. CONSULTAR TODOS LOS CLIENTES")
    clientes = dao.consultar_todos()
    for c in clientes:
        print(f"  - {c}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()