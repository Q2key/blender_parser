set model=%1
set version=%2
call C:/blender29/blender scenes/__DEV29__.blend --background --python run.py -- -store -m=%model% -v=%version%