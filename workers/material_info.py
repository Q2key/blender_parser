
import bpy


class MaterialInfo:

    @staticmethod
    def get_material_info(mat_name, clean_before):
        mat = (bpy.data.materials.get(mat_name) or
               bpy.data.materials.new(mat_name))

        mat.use_nodes = True

        nt = mat.node_tree

        nodes = nt.nodes
        links = nt.links

        # clear nodes
        if clean_before:
            nodes.clear()

        return {"mat": mat, "nodes": nodes, "links": links}
