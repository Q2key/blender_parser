call C:/blender29/blender scenes/__DEV29__.blend --background --python run.py -- -store --model=presetCasual --version=presets
call C:/blender29/blender scenes/__DEV29__.blend --background --python run.py -- -store --model=presetBusinessCasual --version=presets
call C:/blender29/blender scenes/__DEV29__.blend --background --python run.py -- -store --model=presetTuxedo --version=presets
call C:/blender29/blender scenes/__DEV29__.blend --background --python run.py -- -store --model=presetBusiness --version=presets
call C:/blender29/blender scenes/__DEV29__.blend --background --python run.py -- -store --model=presetFormal --version=presets

call optimize-images -ca renders/presets/