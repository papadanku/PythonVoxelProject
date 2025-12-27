
from settings import *

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
                    # Attribute tuple format: (x, y, z voxel_id, face_id)
                    v0 = (x,     y + 1, z,     voxel_id, 0)
                    v1 = (x + 1, y + 1, z,     voxel_id, 0)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = (x,     y + 1, z + 1, voxel_id, 0)

                    # Add in counter-clockwise order
                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # Do the same for the other faces of the voxel

                # Bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    v0 = (x,     y, z,     voxel_id, 1)
                    v1 = (x + 1, y, z,     voxel_id, 1)
                    v2 = (x + 1, y, z + 1, voxel_id, 1)
                    v3 = (x,     y, z + 1, voxel_id, 1)

                    # Add in counter-clockwise order
                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # Right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    v0 = (x + 1, y,     z,     voxel_id, 2)
                    v1 = (x + 1, y + 1, z,     voxel_id, 2)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = (x + 1, y,     z + 1, voxel_id, 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    v0 = (x, y,     z,     voxel_id, 3)
                    v1 = (x, y + 1, z,     voxel_id, 3)
                    v2 = (x, y + 1, z + 1, voxel_id, 3)
                    v3 = (x, y,     z + 1, voxel_id, 3)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    v0 = (x,     y,     z, voxel_id, 4)
                    v1 = (x,     y + 1, z, voxel_id, 4)
                    v2 = (x + 1, y + 1, z, voxel_id, 4)
                    v3 = (x + 1, y,     z, voxel_id, 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    v0 = (x,     y,     z + 1, voxel_id, 5)
                    v1 = (x,     y + 1, z + 1, voxel_id, 5)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = (x + 1, y    , z + 1, voxel_id, 5)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index + 1]