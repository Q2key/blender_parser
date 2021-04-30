import os
import sys
import json
import datetime
import bpy

from workers.fabric_worker import FabricWorker
from workers.plastic_worker import PlasticWorker
from workers.strings_worker import StringsWorker
from workers.label_worker import LabelWorker
from workers.holdout_worker import HoldoutWorker

from engine.engine_base import EngineBase
from engine.saver.saver_builder import SaverBuilder

from helpers.process import ProcessHelper as ph
from helpers.stop_watch import StopWatch
from helpers.stat import StatHelper
from helpers.directory import DirectoryHelper as dh


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
		self.save_details_state()
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
			print('\r\n:{0}\r\n'.format(k))
			self.process_details(d)

	# 5
	def filter_details(self, elements):
		if self.args and self.args.model:
			details = dict()
			# Iterate over all the items in dictionary
			for (key, value) in elements:
				if key in self.args.model:
					details[key] = value
			return details.items()
		return elements

	# 6
	def get_material(self, d):
		d['available_material'] = [
			e for e in self.ctx.MATERIALS
			if e['id'] in d['available_material_id']]

	# 7
	def process_details(self, d):
		d['variant'] = 'parent'



		if len(d['variants']) > 0:
			for v in d['variants']:
				d['file_id'] = d['prefix'] + v + d['suffix']
				d['variant'] = v
				self.before_render(d)
				self.render_partial(d)
				self.after_render(d)
		else:
			d['file_id'] = d['prefix'] + d['suffix']
			self.before_render(d)
			self.render_partial(d)
			self.after_render(d)

	def preprocess_details(self, d):

		d_name = d['file_id']
		v_name = d['variant']

		for obj in bpy.data.objects:
			n = obj.name
			is_included = bool(d['included']) and n in d['included'][v_name]

			is_target = (n == d_name)
			is_mask = bool(d['masks']) and n in d['masks'][v_name]
			is_light = bool(d['light'] and n in d['light'])

			if is_light:
				obj.hide_render = False

			if is_target:
				obj.hide_render = False

			if is_included:
				obj.hide_render = False

			if is_mask:
				obj.hide_render = False
				HoldoutWorker.create_holdout_material()
				HoldoutWorker.apply_holdout_material(obj)

	def set_default(self):
		for c in bpy.data.collections.values():
			c.hide_render = False

		for (k, v) in bpy.data.objects.items():
			v.hide_render = True

	def before_render(self, d):
		self.set_default()
		self.preprocess_details(d)

	def save_details_state(self):
		d = dict()
		for obj in bpy.data.objects:
			if str(type(obj.data)) == "<class 'bpy_types.Mesh'>":
				d[obj.name] = obj.data.materials[0].name
		
		ph.write_json(self.ctx.SCENE_STATE_PATH, d)

	def after_render(self, d):

		v_name = d['variant']
		m_name = d['type']

		for obj in bpy.data.objects:
			n = obj.name
			is_mask = bool(d['masks']) and n in d['masks'][v_name]

			if is_mask:
				obj.hide_render = False
				HoldoutWorker.restore_material(obj, n, self.ctx.SCENE_STATE_PATH)


	def render_partial(self, d):
		self.before_render(d)

		p = d['file_id']
		sp = str.format("{0}", self.folder)
		mp = sp + "/" + d['prefix'] + d["variant"]
		fp = mp + "/" + d["folder"]

		dh.make_folder_by_detail(sp)
		dh.make_folder_by_detail(mp)
		dh.make_folder_by_detail(fp)
		dat_file = ph.read_dat_file(fp)

		# create image saver
		saver = self.saver_builder.get_saver(d['type'])

		for m in d['available_material']:
			m_id = m["id"]
			if m["id"] in dat_file:
				print(str.format("{0} skipped", m_id))
				continue

			# render image
			self.set_material(m, d)
			self.render_detail()

			# clean orphans
			self.purge_oprhans_data()

			# save image
			saver.set_paths_hierarhy([
				self.folder,
				d['prefix'] + d["variant"],
				d["folder"],
				m["id"],
			])
			saver.process()

			self.list_pop(fp, m_id)
			self.stat.increment()

	def set_material(self, material, detail):
		v_name = detail['variant']
		scale = None
		if 'scale' in detail and v_name in detail['scale']:
			scale = detail['scale'][v_name]
		
		if detail['type'] == 'fabric':
			FabricWorker.create_fabric_multy_material(material, scale)
			FabricWorker.collar_seam_multy_material(material)
		if detail['type'] == 'preset':
			FabricWorker.create_fabric_multy_material(material, scale)
			FabricWorker.collar_seam_multy_material(material)
			PlasticWorker.create_img_button_material(detail['button_texture'])
			LabelWorker.label_seam_multy_material(detail['label_texture'])
		if detail['type'] == 'plastic':
			pass
		if detail['type'] == 'label':
			LabelWorker.label_seam_multy_material(material)
			pass
		if detail['type'] == 'buttons':
			PlasticWorker.create_img_button_material(material)

	def save_big(self, ns, r):
		ph.save_image(ns["b"], ns["s"], r["Big"])

	def save_small(self, ns, r):
		ph.save_image(ns["b"], ns["s"], r["Small"])

	def list_pop(self, path, entity):
		ph.write_stats(path, entity)

	def set_scene(self):
		s = self.ctx.SCENE
		r = s["Resolution"]
		l = r['Big']
		p = s["Percentage"]
		c = s["Compression"]

		bpy.data.scenes["Scene"].render.engine = 'BLENDER_EEVEE'
		bpy.data.scenes["Scene"].render.resolution_x = l["x"]
		bpy.data.scenes["Scene"].render.resolution_y = l["y"]
		bpy.data.scenes["Scene"].render.resolution_percentage = p
		bpy.data.scenes["Scene"].render.image_settings.compression = c

	def purge_oprhans_data(self):
		bpy.ops.outliner.orphans_purge()

	def render_detail(self):
		bpy.context.scene.render.filepath = self.ctx.SCENE["TempFile"]
		bpy.ops.render.render(write_still=True)