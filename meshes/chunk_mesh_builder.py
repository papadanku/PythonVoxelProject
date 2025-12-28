
from settings import *
from numba import uint8

@njit
def get_ambient_occlusion(local_position, world_position, world_voxels, plane):
    """
    Calculate ambient occlusion values for a voxel face.

    Computes ambient occlusion by sampling neighboring voxel positions
    around a face to determine how much light should be blocked.
    Different sampling patterns are used depending on the face orientation
    (X, Y, or Z plane). Returns four AO values corresponding to the
    four corners of the face.

    :param local_position: Local coordinates within the chunk
    :param world_position: World coordinates of the face position
    :param world_voxels: Array containing all voxel data for the world
    :param plane: Face orientation ('X', 'Y', or 'Z')
    :return: Tuple of four ambient occlusion values for face corners
    :rtype: tuple
    """

    lx, ly, lz = local_position
    wx, wy, wz = world_position

    if plane == 'Y':
        a = is_void((lx,     ly, lz - 1), (wx,     wy, wz - 1), world_voxels)
        b = is_void((lx - 1, ly, lz - 1), (wx - 1, wy, wz - 1), world_voxels)
        c = is_void((lx - 1, ly, lz    ), (wx - 1, wy, wz    ), world_voxels)
        d = is_void((lx - 1, ly, lz + 1), (wx - 1, wy, wz + 1), world_voxels)
        e = is_void((lx,     ly, lz + 1), (wx,     wy, wz + 1), world_voxels)
        f = is_void((lx + 1, ly, lz + 1), (wx + 1, wy, wz + 1), world_voxels)
        g = is_void((lx + 1, ly, lz    ), (wx + 1, wy, wz    ), world_voxels)
        h = is_void((lx + 1, ly, lz - 1), (wx + 1, wy, wz - 1), world_voxels)

    if plane == 'X':
        a = is_void((lx, ly    , lz - 1), (wx, wy,     wz - 1), world_voxels)
        b = is_void((lx, ly - 1, lz - 1), (wx, wy - 1, wz - 1), world_voxels)
        c = is_void((lx, ly - 1, lz    ), (wx, wy - 1, wz    ), world_voxels)
        d = is_void((lx, ly - 1, lz + 1), (wx, wy - 1, wz + 1), world_voxels)
        e = is_void((lx, ly    , lz + 1), (wx, wy,     wz + 1), world_voxels)
        f = is_void((lx, ly + 1, lz + 1), (wx, wy + 1, wz + 1), world_voxels)
        g = is_void((lx, ly + 1, lz    ), (wx, wy + 1, wz    ), world_voxels)
        h = is_void((lx, ly + 1, lz - 1), (wx, wy + 1, wz - 1), world_voxels)

    if plane == 'Z':
        a = is_void((lx - 1, ly    , lz), (wx - 1, wy,     wz), world_voxels)
        b = is_void((lx - 1, ly - 1, lz), (wx - 1, wy - 1, wz), world_voxels)
        c = is_void((lx    , ly - 1, lz), (wx    , wy - 1, wz), world_voxels)
        d = is_void((lx + 1, ly - 1, lz), (wx + 1, wy - 1, wz), world_voxels)
        e = is_void((lx + 1, ly    , lz), (wx + 1, wy,     wz), world_voxels)
        f = is_void((lx + 1, ly + 1, lz), (wx + 1, wy + 1, wz), world_voxels)
        g = is_void((lx    , ly + 1, lz), (wx    , wy + 1, wz), world_voxels)
        h = is_void((lx - 1, ly + 1, lz), (wx - 1, wy + 1, wz), world_voxels)

    ambient_occlusion = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
    return ambient_occlusion

@njit
def to_uint8(x, y, z, voxel_id, face_id, ao_id, flip_id):
    """
    Convert vertex attributes to unsigned 8-bit integers.

    Converts vertex position coordinates and attribute values to uint8 format
    for efficient storage in vertex buffers. This function creates a tuple
    containing all vertex attributes needed for rendering.

    :param x: X coordinate of the vertex position
    :param y: Y coordinate of the vertex position
    :param z: Z coordinate of the vertex position
    :param voxel_id: ID of the voxel this vertex belongs to
    :param face_id: ID of the face this vertex belongs to (0-5)
    :param ao_id: Ambient occlusion value for this vertex
    :param flip_id: Vertex winding order flip flag (0 or 1)
    :return: Tuple of vertex attributes as uint8 values
    :rtype: tuple
    """
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id), uint8(ao_id), uint8(flip_id)

@njit
def get_chunk_index(world_voxel_position):
    """
    Calculate the chunk index for a given world voxel position.

    Converts world coordinates to chunk coordinates and calculates
    the linear index in the chunks array. Returns -1 for positions
    outside the valid world bounds.

    :param world_voxel_position: Tuple containing (x, y, z) world coordinates
    :return: Index of the chunk containing the voxel, or -1 if out of bounds
    :rtype: int
    """
    wx, wy, wz = world_voxel_position
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE

    if not ((0 <= cx < WORLD_WIDTH) and (0 <= cy < WORLD_HEIGHT) and (0 <= cz < WORLD_DEPTH)):
        return -1

    index = cx + WORLD_WIDTH * cz + WORLD_AREA * cy
    return index

@njit
def is_void(local_voxel_position, world_voxel_position, world_voxels):
    """
    Check if a voxel position is empty (void) or contains a solid voxel.

    Determines if a position should be considered empty for face culling.
    Returns True for empty positions (where faces should be rendered) and
    False for solid positions (where faces should be culled).

    :param local_voxel_position: Local coordinates within a chunk
    :param world_voxel_position: World coordinates of the voxel
    :param world_voxels: Array containing all voxel data for the world
    :return: True if the position is empty (void), False if it contains a voxel
    :rtype: bool
    """
    chunk_index = get_chunk_index(world_voxel_position)

    if chunk_index == -1:
        return False

    chunk_voxels = world_voxels[chunk_index]

    x, y, z = local_voxel_position
    voxel_index = x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA

    if chunk_voxels[voxel_index]:
        return False

    return True

@njit
def add_data(vertex_data, index, *vertices):
    """
    Add vertex attribute data to the vertex data array.

    Unpacks vertex attribute tuples and adds them sequentially to the
    vertex data array. Each vertex tuple contains position, voxel ID,
    and face ID attributes.

    :param vertex_data: Target array to receive vertex data
    :param index: Starting index in the target array
    :param *vertices: Variable number of vertex tuples to add
    :return: Updated index pointing to next available position in vertex_data
    :rtype: int
    """
    for vertex in vertices:
        for attribute in vertex:
            vertex_data[index] = attribute
            index += 1
    return index

@njit
def build_chunk_mesh(chunk_voxels, format_size, chunk_position, world_voxels):
    """
    Build optimized vertex data for rendering a voxel chunk.

    This function converts 3D voxel data into optimized geometry for rendering.
    It implements face culling to avoid rendering faces that are adjacent to
    other voxels, significantly reducing the number of triangles rendered.
    Each visible face is converted to two triangles (6 vertices) with appropriate
    vertex attributes including position, voxel ID, and face ID.

    :param chunk_voxels: Array containing voxel data for the chunk
    :param format_size: Size of each vertex in the output format
    :param chunk_position: Position of the chunk in world coordinates
    :param world_voxels: Array containing all voxel data for the world
    :return: Numpy array containing vertex data for all visible voxel faces
    :rtype: numpy.ndarray
    """
    vertex_data = np.empty(CHUNK_VOLUME * 18 * format_size, dtype='uint8')
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                if not voxel_id:
                    continue

                # Voxel world position
                cx, cy, cz = chunk_position
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE

                # Top face (vertex information for two triangles that form a face)
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):

                    # Get ambient occlusion values
                    ao = get_ambient_occlusion((x, y + 1, z), (wx, wy + 1, wz), world_voxels, plane='Y')

                    # Flip vertices to prevent ao anisotropy
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    # Attribute tuple format: (x, y, z voxel_id, face_id, ao_id, flip_id)
                    v0 = to_uint8(x,     y + 1, z,     voxel_id, 0, ao[0], flip_id)
                    v1 = to_uint8(x + 1, y + 1, z,     voxel_id, 0, ao[1], flip_id)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 0, ao[2], flip_id)
                    v3 = to_uint8(x,     y + 1, z + 1, voxel_id, 0, ao[3], flip_id)

                    # Add to the VBO
                    # Flip vertex order vertices based on orientation
                    if flip_id:
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # Do the same for the other faces of the voxel

                # Bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):

                    # Get ambient occlusion values
                    ao = get_ambient_occlusion((x, y - 1, z), (wx, wy - 1, wz), world_voxels, plane='Y')

                    # Flip vertices to prevent ao anisotropy
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    # Attribute tuple format: (x, y, z voxel_id, face_id, ao_id, flip_id)
                    v0 = to_uint8(x,     y, z,     voxel_id, 1, ao[0], flip_id)
                    v1 = to_uint8(x + 1, y, z,     voxel_id, 1, ao[1], flip_id)
                    v2 = to_uint8(x + 1, y, z + 1, voxel_id, 1, ao[2], flip_id)
                    v3 = to_uint8(x,     y, z + 1, voxel_id, 1, ao[3], flip_id)

                    # Add to the VBO
                    # Flip vertex order vertices based on orientation
                    if flip_id:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # Right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):

                    # Get ambient occlusion values
                    ao = get_ambient_occlusion((x + 1, y, z), (wx + 1, wy, wz), world_voxels, plane='X')

                    # Flip vertices to prevent ao anisotropy
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    # Attribute tuple format: (x, y, z voxel_id, face_id, ao_id, flip_id)
                    v0 = to_uint8(x + 1, y,     z,     voxel_id, 2, ao[0], flip_id)
                    v1 = to_uint8(x + 1, y + 1, z,     voxel_id, 2, ao[1], flip_id)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 2, ao[2], flip_id)
                    v3 = to_uint8(x + 1, y,     z + 1, voxel_id, 2, ao[3], flip_id)

                    # Add to the VBO
                    # Flip vertex order vertices based on orientation
                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):

                    # Get ambient occlusion values
                    ao = get_ambient_occlusion((x - 1, y, z), (wx - 1, wy, wz), world_voxels, plane='X')

                    # Flip vertices to prevent ao anisotropy
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    # Attribute tuple format: (x, y, z voxel_id, face_id, ao_id, flip_id)
                    v0 = to_uint8(x, y,     z,     voxel_id, 3, ao[0], flip_id)
                    v1 = to_uint8(x, y + 1, z,     voxel_id, 3, ao[1], flip_id)
                    v2 = to_uint8(x, y + 1, z + 1, voxel_id, 3, ao[2], flip_id)
                    v3 = to_uint8(x, y,     z + 1, voxel_id, 3, ao[3], flip_id)

                    # Add to the VBO
                    # Flip vertex order vertices based on orientation
                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):

                    # Get ambient occlusion values
                    ao = get_ambient_occlusion((x, y, z - 1), (wx, wy, wz - 1), world_voxels, plane='Z')

                    # Flip vertices to prevent ao anisotropy
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    # Attribute tuple format: (x, y, z voxel_id, face_id, ao_id, flip_id)
                    v0 = to_uint8(x,     y,     z, voxel_id, 4, ao[0], flip_id)
                    v1 = to_uint8(x,     y + 1, z, voxel_id, 4, ao[1], flip_id)
                    v2 = to_uint8(x + 1, y + 1, z, voxel_id, 4, ao[2], flip_id)
                    v3 = to_uint8(x + 1, y,     z, voxel_id, 4, ao[3], flip_id)

                    # Add to the VBO
                    # Flip vertex order vertices based on orientation
                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):

                    # Get ambient occlusion values
                    ao = get_ambient_occlusion((x, y, z + 1), (wx, wy, wz + 1), world_voxels, plane='Z')

                    # Flip vertices to prevent ao anisotropy
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    # Attribute tuple format: (x, y, z voxel_id, face_id, ao_id, flip_id)
                    v0 = to_uint8(x,     y,     z + 1, voxel_id, 5, ao[0], flip_id)
                    v1 = to_uint8(x,     y + 1, z + 1, voxel_id, 5, ao[1], flip_id)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 5, ao[2], flip_id)
                    v3 = to_uint8(x + 1, y    , z + 1, voxel_id, 5, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index + 1]
