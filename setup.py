from cx_Freeze import setup, Executable

executables = [
    Executable('src/index.py')
]

setup(name='GCF',
      version='0.1',
      description='copia y convierte archivos GCF a SAC',
      executables=executables
      )
