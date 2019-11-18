import bpy
import os

d = { 
    'M-1': 'CuffM1',
    'M-2': 'CuffM2',
    'M-3': 'CuffM3',
    'M-4': 'CuffM4',
    'V-1': 'Mao',
    'V-2': 'Mandarin',
    'V-3': 'King'
}

for (k, v) in bpy.data.objects.items():
    with open('C:/scene.txt', mode="w") as f:
        f.write("{0}".format(k,v))

def pascalise(rawStr):
    for i in range(len(rawStr)):
        print(rawStr[i])
        

