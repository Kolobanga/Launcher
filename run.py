import os
import subprocess


def run():
    variables = {'HSITE': 'H:\hsite',
                 'HOUDINI_DISABLE_CONSOLE': '1'}

    os.environ.update(variables)
    subprocess.run(r'S:\Houdini 16.5.588\bin\houdinifx.exe -n')


run()
