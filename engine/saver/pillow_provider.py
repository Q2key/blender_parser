from PIL import Image

class PillowProvider:

	@staticmethod
	def save_image(src, out, sizes):
		img = Image.open(src)
		img = img.resize((sizes["x"], sizes["y"]), Image.ANTIALIAS)
		img.save(out)
