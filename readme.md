# Система автоматизации рендеринга изображений

### Как использовать
* `render.sh` for linux
* `render.bat` for windows

Пример использования с параметрами

`render.sh --model=collar --version=v1.0`

### Параметры

* version 

Это версия группы изображений. Каждая версия группы изображений будет лежать в папке с 
названием соответствующему переданному в качестве значения параметра.

    render.sh --model=my_folder


* model   

Это значимая часть рубашки. Например, основной воротник или внутренняя стойка воротника.
В случае если параметр не передается, то изображения будут созданы для всех деталей.
    
    `render.sh --model=bodyShirt`
    `render.sh --model=bodyShirt --model=collar`

Полный список моделей. Каждый из этого списка можно передать в качестве значения для 
параметра **model**. Каждый из этих элементов сконфигурирован в json файле с 
соответствующим названием.

    model list:
		
        bodyShirt
        bodyShirtButton
        bodyShirtInternal
        bodyShirtLogo
        collar
        collarButton
        collarExternalStand
        collarInternalStand
        cuffButton
        cuffExternal
        cuffInternal
        pocket
        presetBusiness
        presetBusinessCasual
        presetCasual
        presetFormal
        presetTuxedo

### Зависимости
* python 3.7
* blender 2.91
* OS windows \ linux

***

### Установка
* `.init.sh` for linux
* `init.bat` for windows

***
### Параметры конфигурационных файлов

Все конфигурационные файлы лежат в папке **config**.

* scene.json


    "Resolution": {                                 разрешение изображений
        "Big": {                                    данный формат используется для увеличенного изображения
            "x": 1600,                              кол-во точек по X
            "y": 2180,                              кол-во точек по Y
            "quality": 100                          качество сжатия изображения
        },
        "Small": {                                  данный формат используется в основном окне конструктора
            "x": 400,                               кол-во точек по X
            "y": 545,                               кол-во точек по Y
            "quality": 100                          качество сжатия изображения
        },
        "XSmall": {                                 данный формат используется в виджите корзины
            "x": 200,                               кол-во точек по X
            "y": 272,                               кол-во точек по Y
            "quality": 100                          качество сжатия изображения
        }
    },
    "Percentage": 100,                               чем ниже процент, тем ниже качество и размер
    "Compression": 100,                              чем ниже компрессия тем выше качество и размер
    "SamplesCount": 128,                             количество сэмплов. чем больше тем выше качество, от 0 до 512
    "TexturesFormat": ['.png', '.jpg'],              массив для допустимых форматов текстур
    "TempFile": "temp.png",                          временный файл необходимый для рендера,
    "RenderStorage": "/home/path/to/my/renders"      полный абсолютный путь до папки где будут лежать готове изображения

