from compas.datastructures.mesh import Mesh
from compas_pattern.datastructures.quad_mesh import QuadMesh

from compas.utilities import geometric_key

__author__     = ['Robin Oval']
__copyright__  = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'oval@arch.ethz.ch'

__all__ = [

]

class PseudoQuadMesh(QuadMesh):

    def __init__(self):
        super(PseudoQuadMesh, self).__init__()

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face to the mesh object. Allow [a, b, c, c] faces.

        Parameters
        ----------
        vertices : list
            A list of vertex keys.
            For every vertex that does not yet exist, a new vertex is created.
        attr_dict : dict, optional
            Face attributes.
        kwattr : dict, optional
            Additional named face attributes.
            Named face attributes overwrite corresponding attributes in the
            attribute dict (``attr_dict``).

        Returns
        -------
        int
            The key of the face.
            The key is an integer, if no key was provided.
        hashable
            The key of the face.
            Any hashable object may be provided as identifier for the face.
            Provided keys are returned unchanged.

        Raises
        ------
        TypeError
            If the provided face key is of an unhashable type.

        Notes
        -----
        If no key is provided for the face, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        See Also
        --------
        * :meth:`add_vertex`
        * :meth:`add_edge`

        Examples
        --------
        >>>

        """
        attr = self._compile_fattr(attr_dict, kwattr)

        # remove clean vertices to allow [a, b, c, c] faces
        #self._clean_vertices(vertices)

        if len(vertices) < 3:
            return

        keys = []
        for key in vertices:
            if key not in self.vertex:
                key = self.add_vertex(key)
            keys.append(key)

        fkey = self._get_face_key(fkey)

        self.face[fkey] = keys
        self.facedata[fkey] = attr

        for u, v in self._cycle_keys(keys):
            self.halfedge[u][v] = fkey
            if u not in self.halfedge[v]:
                self.halfedge[v][u] = None

        return fkey

    def delete_face(self, fkey):
        """Delete a face from the mesh object. Valid for [a, b, c, c] faces.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Examples
        --------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.plotters import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            mesh.delete_face(12)

            plotter = MeshPlotter(mesh)
            plotter.draw_vertices()
            plotter.draw_faces()
            plotter.show()

        """

        for u, v in self.face_halfedges(fkey):
            if u != v:
                self.halfedge[u][v] = None
                if self.halfedge[v][u] is None:
                    del self.halfedge[u][v]
                    del self.halfedge[v][u]

        del self.face[fkey]

    def edges(self, data=False):
        """Iterate over the edges of the mesh.

        Parameters
        ----------
        data : bool, optional
            Return the edge data as well as the edge vertex keys.

        Yields
        ------
        2-tuple
            The next edge as a (u, v) tuple, if ``data`` is false.
        3-tuple
            The next edge as a (u, v, data) tuple, if ``data`` is true.

        Note
        ----
        Mesh edges have no topological meaning. They are only used to store data.
        Edges are not automatically created when vertices and faces are added to
        the mesh. Instead, they are created when data is stored on them, or when
        they are accessed using this method.

        This method yields the directed edges of the mesh.
        Unless edges were added explicitly using :meth:`add_edge` the order of
        edges is *as they come out*. However, as long as the toplogy remains
        unchanged, the order is consistent.

        Example
        -------
        .. code-block:: python

            import compas
            from compas.datastructures import Mesh
            from compas.plotters import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            for index, (u, v, attr) in enumerate(mesh.edges(True)):
                attr['index1'] = index

            for index, (u, v, attr) in enumerate(mesh.edges(True)):
                attr['index2'] = index

            plotter = MeshPlotter(mesh)

            text = {(u, v): '{}-{}'.format(a['index1'], a['index2']) for u, v, a in mesh.edges(True)}

            plotter.draw_vertices()
            plotter.draw_faces()
            plotter.draw_edges(text=text)
            plotter.show()

        """
        edges = set()

        for u in self.halfedge:
            for v in self.halfedge[u]:

                if (u, v) in edges or (v, u) in edges:
                    continue

                edges.add((u, v))
                edges.add((v, u))

                if (u, v) not in self.edgedata:
                    self.edgedata[u, v] = self.default_edge_attributes.copy()

                    if u != v:
                        if (v, u) in self.edgedata:
                            self.edgedata[u, v].update(self.edgedata[v, u])
                            del self.edgedata[v, u]

                        self.edgedata[v, u] = self.edgedata[u, v]

                if data:
                    yield u, v, self.edgedata[u, v]
                else:
                    yield u, v

    def to_mesh_2(self):
        vertices = [self.vertex_coordinates(vkey) for vkey in self.vertices()]
        face_vertices = []
        # remove consecutive duplicates in pseudo quad faces
        for fkey in self.faces():
            non_pseudo_face = []
            pseudo_face = self.face_vertices(fkey)
            for i, vkey in enumerate(pseudo_face):
                if vkey != pseudo_face[i - 1]:
                    non_pseudo_face.append(vkey)
            face_vertices.append(non_pseudo_face)
        mesh = Mesh.from_vertices_and_faces(vertices, face_vertices)
        return mesh

    def to_mesh(self):

        vertices = [self.vertex_coordinates(vkey) for vkey in self.vertices()]
        vertex_remap = list(self.vertices())
        faces = []
        for fkey in self.faces():
            face_vertices = []
            for vkey in self.face_vertices(fkey):
                vkey_idx = vertex_remap.index(vkey)
                if vkey_idx not in face_vertices:
                    face_vertices.append(vkey_idx)
            faces.append(face_vertices)

        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        return mesh

def pqm_from_mesh(mesh, poles):
    """Converts a mesh into a pseuod-quad mesh with poles inducing face of the type [a, b, c, c].

    Parameters
    ----------
    mesh : Mesh
        A mesh.
    poles: list
        List of pole coordinates.

    Returns
    -------
    vertices, new_face_vertices: list
        The vertices with the new face_vertices.

    Raises
    ------
    -

    """

    vertices = [mesh.vertex_coordinates(vkey) for vkey in mesh.vertices()]
    vertex_conversion = {vkey: i for i, vkey in enumerate(mesh.vertices())}
    new_face_vertices = []

    poles = [geometric_key(pole) for pole in poles]

    for fkey in mesh.faces():
        face_vertices = mesh.face_vertices(fkey)[:]
        if len(face_vertices) == 3:
            # find pole location
            pole = None
            for vkey in face_vertices:
                geom_key = geometric_key(mesh.vertex_coordinates(vkey))
                if geom_key in poles:
                    pole = vkey
                    break
            # modify face
            if pole is not None:
                idx = face_vertices.index(vkey)
                face_vertices.insert(idx, vkey)

        # store new face
        new_face_vertices.append([vertex_conversion[vkey] for vkey in face_vertices])

    return vertices, new_face_vertices

def is_face_pseudo_quad(mesh, fkey):

    if fkey is None or len(mesh.face_vertices(fkey)) != 4:
        return 'invalid'

    face_vertices = mesh.face_vertices(fkey)
    for vkey in face_vertices:
        if face_vertices.count(vkey) > 1:
            return True

    return False

def vertex_index(mesh, vkey):
    """Return the index of a vertex in a coarse quad mesh with potential poles stored in pseudo-quad faces.

    Parameters
    ----------
    mesh : Mesh
        A mesh.
    vkey: int
        Key of a vertex

    Returns
    -------
    index: float
        The index of the vertex.

    Raises
    ------
    -

    """

    if not mesh.is_quadmesh():
        return None
    if len(mesh.vertex_neighbors(vkey)) == 0:
        return None
        
    valency = float(len(mesh.vertex_neighbors(vkey)))
    boundary = mesh.is_vertex_on_boundary(vkey)
    if vkey in mesh.vertex_neighbors(vkey):
        pole = True
    else:
        pole = False
    #pole = True if vkey in mesh.vertex_neighbors(vkey) else False
    partial_pole = False
    #print valency, mesh.vertex_neighbors(vkey), boundary, pole, partial_pole
    #return 0
    # if pole:
    #     vertex_faces = mesh.vertex_faces(vkey)
    #     for fkey in vertex_faces:
    #         if fkey is not None and not is_face_pseudo_quad(mesh, fkey):
    #             partial_pole = True
    #             break
    #     if partial_pole:
    #         pseudo_valency = sum([1 - is_face_pseudo_quad(mesh, fkey) for fkey in vertex_faces])
    #         if boundary:
    #             pseudo_valency += 1

    if pole:
        if partial_pole:
            if not boundary:
                #print 'partial pole', 1. / 4. * (4. - pseudo_valency)
                return 1. / 4. * (4. - pseudo_valency)
            else:
                #print 'boundary partial pole', 1. / 4. * (3. - pseudo_valency)
                return 1. / 4. * (3. - pseudo_valency)
        else:
            if not boundary:
                #print 'pole', 1.
                return 1.
            else:
                #print 'boundary pole', 1. / 2.
                return 1. / 2.
    else:
        if not boundary:
            #print 'classic', 1. / 4. * (4. - valency)
            return 1. / 4. * (4. - valency)
        else:
            #print 'boundary classic', 1. / 4. * (3. - valency)
            return 1. / 4. * (3. - valency)

# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas
