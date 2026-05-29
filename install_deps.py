import subprocess
import sys

# Instalar reportlab se não estiver instalado
try:
    import reportlab
    print("✓ reportlab já está instalado")
except ImportError:
    print("Instalando reportlab...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
    print("✓ reportlab instalado com sucesso!")

# Verificar Flask
try:
    import flask
    print("✓ Flask já está instalado")
except ImportError:
    print("Instalando Flask...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    print("✓ Flask instalado com sucesso!")

print("\n✅ Todas as dependências estão instaladas!")
