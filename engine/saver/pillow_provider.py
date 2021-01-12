from PIL import Image
import os
import shutil


class PillowProvider:

	@staticmethod
	def save_image(src, out, sizes, fmt="PNG", optimize=True, img_quality=95):
		cp_file = src + ".png"
		cp_img = shutil.copy(src, cp_file)

		img = Image.open(cp_img)
		img = img.resize((sizes["x"], sizes["y"]), Image.ANTIALIAS)
		img.save(out, fmt, optimize=optimize, quality=sizes["q"])
		img.close()

		os.remove(cp_file)

	@staticmethod
	def save_as_jpg(src, out, sizes):
		cp_file = src + ".png"
		cp_img = shutil.copy(src, cp_file)

		png = Image.open(cp_img)

		png.load()
		png = png.resize((sizes["x"], sizes["y"]), Image.ANTIALIAS)

		background = Image.new("RGB", png.size, (255, 255, 255))
		background.paste(png, mask=png.split()[3])
		background.save(out, 'JPEG', progressive=True, optimize=True, quality=sizes["q"])
		
		png.close()
		os.remove(cp_file)
