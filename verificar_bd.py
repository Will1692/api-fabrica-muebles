import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from com.fabrica.muebles.util.verificar_tablas import VerificarTablas

if __name__ == "__main__":
    VerificarTablas.ejecutar()