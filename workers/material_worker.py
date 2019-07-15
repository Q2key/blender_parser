
import bpy


class MaterialWorker:

    @staticmethod
    def get_material_info(mat_name, cleanBefore):
        ''' get material, nodes and links for creating material '''
        # get material or create new with same name
        mat = (bpy.data.materials.get(mat_name) or
               bpy.data.materials.new(mat_name))

        # define using nodes
        mat.use_nodes = True

        # define nodes tree
        nt = mat.node_tree
        nt.name = 'ntg'
        nodes = nt.nodes
        links = nt.links

        # clear nodes
        if cleanBefore:
            nodes.clear()

        return {"mat": mat, "nodes": nodes, "links": links}
