from PIL import Image

class ImageHelper:

    def change_size(self,image,path,new_width,new_height,new_dpi=300):
        img = Image.open(image)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save(path)

    def analyse_image(self):
        pass