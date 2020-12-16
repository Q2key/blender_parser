set model_arg=%1
set version_arg=%2
start C:/blender/blender scenes/main/__MAIN__.blend --background --python run.py -- -store -m=%model_arg% -version=%version_arg%