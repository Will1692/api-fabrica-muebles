import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from com.fabrica.muebles.util.conexion_bd import ConexionBD


def main():
    print("=" * 60)
    print("PRUEBA DE CONEXIÓN A BASE DE DATOS")
    print("=" * 60)
    print()

    if ConexionBD.probar_conexion():
        print()
        print("=" * 60)
        print("PRUEBA EXITOSA - La conexión funciona correctamente")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("PRUEBA FALLIDA - Revisa la configuración")
        print("=" * 60)


if __name__ == "__main__":
    main()