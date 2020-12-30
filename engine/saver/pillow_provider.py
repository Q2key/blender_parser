from PIL import Image


class PillowProvider:

	@staticmethod
	def save_image(src, out, sizes, fmt="PNG", optimize=True):
		img = Image.open(src)
		img = img.resize((sizes["x"], sizes["y"]), Image.ANTIALIAS)
		img.save(out, fmt, optimize=optimize)

	@staticmethod
	def save_as_jpg(src, out, sizes):
		png = Image.open(src)

		png.load()
		png = png.resize((sizes["x"], sizes["y"]), Image.ANTIALIAS)

		background = Image.new("RGB", png.size, (255, 255, 255))
		background.paste(png, mask=png.split()[3])
		background.save(out, 'JPEG', progressive=True, optimize=True, quality=95)
