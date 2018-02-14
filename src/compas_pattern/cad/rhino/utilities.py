try:
    import rhinoscriptsyntax as rs

except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise

from compas.utilities import geometric_key

import compas_rhino as rhino

__author__     = ['Robin Oval']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'oval@arch.ethz.ch'


__all__ = [
    'is_point_on_curve',
    'surface_borders',
    'surface_border_kinks',
    'draw_mesh',
    'curve_discretisation',
]


def is_point_on_curve(curve_guid, point_xyz):
    geom_key = geometric_key(point_xyz)
    t = rs.CurveClosestPoint(curve_guid, point_xyz)
    pt_on_crv = rs.EvaluateCurve(curve_guid, t)
    geom_key_pt_on_crv = geometric_key(pt_on_crv)
    if geom_key == geom_key_pt_on_crv:
        return True
    else:
        return False

def surface_borders(surface, border_type = 0):
        border = rs.DuplicateSurfaceBorder(surface, border_type)
        curves = rs.ExplodeCurves(border, delete_input = True)
        return curves

def surface_border_kinks(surface_guid):
    kinks = []
    borders = surface_borders(surface_guid)
    for curve_guid in borders:
        start_tgt = rs.CurveTangent(curve_guid, rs.CurveParameter(curve_guid, 0))
        end_tgt = rs.CurveTangent(curve_guid, rs.CurveParameter(curve_guid, 1))
        if not rs.IsCurveClosed(curve_guid) or not rs.IsVectorParallelTo(start_tgt, end_tgt):
            start = rs.CurveStartPoint(curve_guid)
            end = rs.CurveEndPoint(curve_guid)
            if start not in kinks:
                kinks.append(start)
            if end not in kinks:
                kinks.append(end)

def draw_mesh(mesh):
    vertices = [mesh.vertex_coordinates(vkey) for vkey in mesh.vertices()]
    face_vertices = [mesh.face_vertices(fkey) for fkey in mesh.faces()]
    mesh_guid = rhino.utilities.drawing.xdraw_mesh(vertices, face_vertices, None, None)
    return mesh_guid

def curve_discretisation(curve_guid, discretisation_spacing):
    n = int(rs.CurveLength(curve_guid) / discretisation_spacing) + 1
    points = rs.DivideCurve(curve_guid, n)
    if rs.IsCurveClosed(curve_guid):
        points.append(points[0])
    return rs.AddPolyline(points)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas
