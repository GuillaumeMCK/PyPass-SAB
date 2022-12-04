from cx_Freeze import setup, Executable

target = Executable(
    base="Win32GUI",
    script="./main.py",
)

output_dir = "./build"

setup(
    name='PyPass-SAB',
    version='0.1',
    description='Patcher for StartAllBack',
    executables=[target],
    author='GuillaumeMCK',
    options={
        'build_exe': {
            'include_msvcr': True,
            'build_exe': output_dir
        },
    },
)
