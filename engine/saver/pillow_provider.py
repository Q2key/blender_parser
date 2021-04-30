from PIL import Image
import os
import shutil


class PillowProvider:

	@staticmethod
	def save_image(
		src,
		out,
		sizes,
		fmt="PNG",
		optimize=True,
		img_quality=95
		):
		cp_file = src + ".png"
		cp_img = shutil.copy(src, cp_file)

		img = Image.open(cp_img)
		img = img.resize(
				(
					sizes["x"],
					sizes["y"]
				),
				Image.ANTIALIAS
			)
		img.save(
			out,
			fmt,
			optimize=optimize,
			quality=sizes["quality"]
		)
		img.close()

		os.remove(cp_file)

	@staticmethod
	def save_as_jpg(
		src,
		out,
		sizes
		):
		cp_file = src + ".png"
		cp_img = shutil.copy(src, cp_file)

		png = Image.open(cp_img)

		png_white = Image.new("RGB", png.size, "WHITE")
		png_white.paste(png, (0, 0), png) 
		png_white = png_white.resize(
			(
				sizes["x"],
				sizes["y"]
			), 
			Image.ANTIALIAS
		)
		png_white.save(
			out,
			'JPEG',
			quality=sizes["quality"]
			)
		
		png.close()
		os.remove(cp_file)
