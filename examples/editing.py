import rhinoscriptsyntax as rs

import compas_rhino as rhino

from compas.datastructures.mesh import Mesh

from compas_pattern.cad.rhino.utilities import draw_mesh
from compas_pattern.datastructures.pseudo_quad_mesh import PseudoQuadMesh

#from compas_pattern.topology.face_strip_operations import face_strip_collapse
#from compas_pattern.topology.face_strip_operations import face_strip_subdivide
#from compas_pattern.topology.face_strip_operations import face_strips_merge

#from compas_pattern.topology.grammar_primitive import primitive_1
#from compas_pattern.topology.grammar_primitive import primitive_2
#from compas_pattern.topology.grammar_primitive import primitive_3
#from compas_pattern.topology.grammar_primitive import primitive_4
#from compas_pattern.topology.grammar_primitive import primitive_5

#from compas_pattern.topology.grammar_extended import extended_21 #6
#from compas_pattern.topology.grammar_extended import extended_21443 #7
#from compas_pattern.topology.grammar_extended import extended_212144321443 #8
#from compas_pattern.topology.grammar_extended import extended_22122333 #9

from compas_pattern.topology.grammar import face_pole
from compas_pattern.topology.grammar import edge_pole
from compas_pattern.topology.grammar import vertex_pole
from compas_pattern.topology.grammar import face_opening
from compas_pattern.topology.grammar import flat_corner_2
from compas_pattern.topology.grammar import flat_corner_3
from compas_pattern.topology.grammar import flat_corner_33

# mesh selection
guid = rs.GetObject('get mesh')
mesh = rhino.mesh_from_guid(PseudoQuadMesh, guid)

rule = rs.GetString('rule?')

if rule == 'face_pole':
    artist = rhino.MeshArtist(mesh, layer='mesh_artist')
    artist.clear_layer()
    
    artist.draw_facelabels()
    artist.redraw()
    fkey = rhino.mesh_select_face(mesh, message = 'fkey')
    artist.clear_layer()
    artist.redraw()
    
    rs.DeleteLayer('mesh_artist')
    
    face_pole(mesh, fkey)

if rule == 'edge_pole':
    artist = rhino.MeshArtist(mesh, layer='mesh_artist')
    artist.clear_layer()
    
    artist.draw_facelabels()
    artist.redraw()
    fkey = rhino.mesh_select_face(mesh, message = 'fkey')
    artist.clear_layer()
    artist.redraw()
    
    artist.draw_edgelabels()
    artist.redraw()
    edge = rhino.mesh_select_edge(mesh, message = 'edge')
    artist.clear_layer()
    artist.redraw()
    
    rs.DeleteLayer('mesh_artist')
    
    edge_pole(mesh, fkey, edge)

if rule == 'vertex_pole':
    artist = rhino.MeshArtist(mesh, layer='mesh_artist')
    artist.clear_layer()
    
    artist.draw_facelabels()
    artist.redraw()
    fkey = rhino.mesh_select_face(mesh, message = 'fkey')
    artist.clear_layer()
    artist.redraw()
    
    artist.draw_vertices()
    artist.redraw()
    pole = rhino.mesh_select_vertex(mesh, message = 'pole')
    artist.clear_layer()
    artist.redraw()
    
    rs.DeleteLayer('mesh_artist')
    
    vertex_pole(mesh, fkey, pole)

if rule == 'face_opening':
    artist = rhino.MeshArtist(mesh, layer='mesh_artist')
    artist.clear_layer()
    
    artist.draw_facelabels()
    artist.redraw()
    fkey = rhino.mesh_select_face(mesh, message = 'fkey')
    artist.clear_layer()
    artist.redraw()
    
    rs.DeleteLayer('mesh_artist')
    
    face_opening(mesh, fkey, pole)

if rule == 'flat_corner_2':
    artist = rhino.MeshArtist(mesh, layer='mesh_artist')
    artist.clear_layer()
    
    artist.draw_facelabels()
    artist.redraw()
    fkey = rhino.mesh_select_face(mesh, message = 'fkey')
    artist.clear_layer()
    artist.redraw()
    
    artist.draw_vertices()
    artist.redraw()
    corner = rhino.mesh_select_vertex(mesh, message = 'corner')
    artist.clear_layer()
    artist.redraw()
    
    rs.DeleteLayer('mesh_artist')
    
    flat_corner_2(mesh, fkey, corner)

if rule == 'flat_corner_3':
    artist = rhino.MeshArtist(mesh, layer='mesh_artist')
    artist.clear_layer()
    
    artist.draw_facelabels()
    artist.redraw()
    fkey = rhino.mesh_select_face(mesh, message = 'fkey')
    artist.clear_layer()
    artist.redraw()
    
    artist.draw_vertices()
    artist.redraw()
    corner = rhino.mesh_select_vertex(mesh, message = 'corner')
    artist.clear_layer()
    artist.redraw()
    
    rs.DeleteLayer('mesh_artist')
    
    flat_corner_3(mesh, fkey, corner)

if rule == 'flat_corner_33':
    artist = rhino.MeshArtist(mesh, layer='mesh_artist')
    artist.clear_layer()
    
    artist.draw_facelabels()
    artist.redraw()
    fkey = rhino.mesh_select_face(mesh, message = 'fkey')
    artist.clear_layer()
    artist.redraw()
    
    artist.draw_vertices()
    artist.redraw()
    corner = rhino.mesh_select_vertex(mesh, message = 'corner')
    artist.clear_layer()
    artist.redraw()
    
    rs.DeleteLayer('mesh_artist')
    
    flat_corner_33(mesh, fkey, corner)

mesh = mesh.to_mesh()

#mesh = face_strip_collapse(Mesh, mesh, ukey, vkey)

#mesh = face_strip_subdivide(Mesh, mesh, ukey, vkey)

#e = quad_mix_1(mesh, fkey, vkey, ukey)
#
### conforming: propagate T-junctions
## propagate until boundary or closed loop
#is_loop = False
#wkey = e
#count = mesh.number_of_faces()
#while count > 0:
#    count -= 1
#    next_fkey = mesh.halfedge[vkey][wkey]
#    ukey = mesh.face_vertex_descendant(next_fkey, wkey)
#    if wkey in mesh.halfedge[ukey] and mesh.halfedge[ukey][wkey] is not None:
#        next_fkey = mesh.halfedge[ukey][wkey]
#        if len(mesh.face_vertices(next_fkey)) == 5:
#            vkey = wkey
#            wkey = penta_quad_1(mesh, next_fkey, wkey)
#            # add to faces along feature to check
#            continue
#        if len(mesh.face_vertices(next_fkey)) == 6:
#            vkey = wkey
#            wkey = hexa_quad_1(mesh, next_fkey, wkey)
#            #if wkey == e2:
#            #    is_loop = True
#            # add to faces along feature to check
#            break
#    break
# # if not loop, propaget in other direction
# if not is_loop:
#     vkey = v
#     wkey = e2
#     count = mesh.number_of_faces()
#     while count > 0:
#         count -= 1
#         next_fkey = mesh.halfedge[vkey][wkey]
#         ukey = mesh.face_vertex_descendant(next_fkey, wkey)
#         if wkey in mesh.halfedge[ukey] and mesh.halfedge[ukey][wkey] is not None:
#             next_fkey = mesh.halfedge[ukey][wkey]
#             if len(mesh.face_vertices(next_fkey)) == 5:
#                 vkey = wkey
#                 wkey = penta_quad_1(mesh, next_fkey, wkey)
#                 # add to faces along feature to check
#                 continue
#             if len(mesh.face_vertices(next_fkey)) == 6:
#                 vkey = wkey
#                 wkey = hexa_quad_1(mesh, next_fkey, wkey)
#                 if wkey == e2:
#                     is_loop = True
#                 # add to faces along feature to check
#                 break
#         break

#print mesh
#for u, v in mesh.edges():
#    u_xyz = mesh.vertex_coordinates(u)
#    v_xyz = mesh.vertex_coordinates(v)
#    if u_xyz == v_xyz:
#        print u_xyz, v_xyz
#    rs.AddLine(u_xyz, v_xyz)
#for fkey in mesh.faces():
#    print mesh.face_vertices(fkey)

# draw mesh
mesh_guid = draw_mesh(mesh)

#rs.AddLayer('edited_mesh')
#rs.ObjectLayer(mesh_guid, layer = 'edited_mesh')