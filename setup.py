from cx_Freeze import setup, Executable

# Archivos adicionales (imágenes, iconos, etc.)
includefiles = [r"E:\MES_Abregu\assets\Elara-logo.ico",r"E:\MES_Abregu\assets\Elara logo.png",r"E:\MES_Abregu\assets\Logo_Mirgor.png",r"E:\MES_Abregu\setting.cfg"]

# Dependencias opcionales (si tienes módulos externos)
build_exe_options = {
    "packages": ["os"],  # Agrega otros módulos si los necesitas
    "includes": ["MESxLog", "serverSocket"],  # Asegura que incluya estos archivos
    "include_files": includefiles,
}

# Configuración del ejecutable
executables = [
    Executable(
        "Main.py",  # Archivo principal
        target_name="Elara.exe",  # Nombre del ejecutable
        icon="Elara-logo.ico",  # Ícono del ejecutable
    )
]

# Setup de instalación
setup(
    name="Elara",
    version="1.0",
    description="Aplicación Elara con cx_Freeze",
    options={"build_exe": build_exe_options},
    executables=executables,
)
