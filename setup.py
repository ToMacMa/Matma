from cx_Freeze import setup, Executable

setup(

name="Matma",

version="1.0",

description="Matma.",
executables=[Executable("main.py")],

)