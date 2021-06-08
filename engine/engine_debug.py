import os
import sys
import json
import datetime
import inspect

from PIL import Image
from engine.engine_base import EngineBase
from helpers.directory import DirectoryHelper as dh
from helpers.process import ProcessHelper as ph

from helpers.stop_watch import StopWatch
from helpers.stat import StatHelper

from engine.saver.saver_builder import SaverBuilder

from structs.rendered_object import RenderedObject
from structs.rendered_identifier import RenderedItentifier
from structs.rendered_material import RenderedMaterial
from structs.rendered_mask import RenderedMask


class Engine(EngineBase):

	# 1
	def __init__(self, ctx, args=False):
		self.ctx = ctx
		self.args = args
		self.saver_builder = SaverBuilder(ctx, args)
		self.folder = dh.get_root_folder(ctx.RENDERS_PATH, args)
		self.stat = StatHelper()
		self.timer = StopWatch()

	# 2
	def prepare(self):
		pass

	# 3
	def go(self):
		self.timer.watch_start()
		self.set_scene()
		self.process_elements()
		self.timer.watch_stop()
		self.timer.print_diff()
		self.stat.print_count()

	# 4
	def process_elements(self):
		# define details
		details = self.ctx.DETAILS.items()
		elements = self.filter_details(details)
		# extend details
		for k, d in elements:
			print('\r\n{0}\r\n'.format(k))
			self.process_details(d)

	# 5
	def filter_details(self, elements):
		if self.args and self.args.model is None:
			return elements

		details = dict()
		# Iterate over all the items in dictionary
		for (key, value) in elements:
			if key in self.args.model:
				details[key] = value

		return details.items()

	# 6
	def get_material(self, d):
		d['available_material'] = [
			e for e in self.ctx.MATERIALS
			if e['id'] in d['available_material_id']]

	# 7
	def process_details(self, d):
		d['variant'] = ''
		if len(d['variants']) > 0:
			for v in d['variants']:
				d['file_id'] = d['prefix'] + v + d['suffix']
				d['variant'] = v
				self.before_render(d)
				self.render_partial(d)
		else:
			d['file_id'] = d['prefix'] + d['suffix']
			self.before_render(d)
			self.render_partial(d)

		print("PROCESSING DETAIL: ", d['file_id'])

	def set_default(self):
		pass

	def set_catchers(self, ro):
		pass

	def preprocess_details(self, ro):
		pass

	def reset_catchers(self):
		pass

	def before_render(self, ro):
		self.set_default()
		self.preprocess_details(ro)

	def render_partial(self, d):
		self.before_render(d)

		p = d['file_id']
		sp = str.format("{0}", self.folder)
		mp = sp + "/" + d['prefix'] +  d["variant"]
		fp = mp  + "/" +  d["folder"]

		dh.make_folder_by_detail(sp)
		dh.make_folder_by_detail(mp)
		dh.make_folder_by_detail(fp)


		print("\r\n ---- ")
		print(d['prefix'] +  d["variant"] + "/" + d["folder"])


		
		dat_file = ph.read_dat_file(mp)

		# create image saver
		saver = self.saver_builder.get_saver(d['type'])

		for m in d['available_material']:
			continue
			m_id = m["id"]
			if m["id"] in dat_file:
				print(str.format("{0} skipped", m_id))
				continue

			# render image
			self.set_material(m, d)
			self.render_detail()

			# save SOLID image
			saver.set_paths_hierarchy([
				self.folder,
				d['prefix'],
				d['variant'],
				m["id"],
			])
			#saver.process()

			self.list_pop(mp, m_id)
			self.stat.increment()

	def set_material(self, material, detail):
		if detail['type'] == 'fabric':
			pass
		if detail['type'] == 'preset':
			pass
		if detail['type'] == 'plastic':
			pass
		if detail['type'] == 'label':
			pass
		if detail['type'] == 'buttons':
			pass

	def save_small(self, ns, r):
		ph.save_image(ns["b"], ns["s"], r["Big"])

	def check_list(self, ns, r):
		ph.save_image(ns["b"], ns["s"], r["Small"])

	def list_pop(self, path, entity):
		ph.write_stats(path, entity)

	def set_scene(self):
		s = self.ctx.SCENE
		r = s["Resolution"]
		l = r['Big']
		p = s["Percentage"]
		c = s["Compression"]

	def render_detail(self):
		pass
