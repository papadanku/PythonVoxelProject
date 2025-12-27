
from settings import *


def is_void(voxel_pos, chunk_voxels):
    """
    Check if a position in the chunk is empty (void).

    Args:
        voxel_pos: Tuple containing (x, y, z) position to check
        chunk_voxels: Array containing voxel data for the chunk

    Returns:
        True if the position is empty or out of bounds, False if occupied

    This function determines if a voxel face should be rendered by checking
    if the adjacent position is empty. Used for face culling optimization.
    """
    x, y, z = voxel_pos

    if (0 <= x < CHUNK_SIZE) and (0 <= y < CHUNK_SIZE) and (0 <= z < CHUNK_SIZE):
        if chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]:
            return False
    return True


def add_data(vertex_data, index, *vertices):
    """
    Add vertex attribute data to the vertex data array.

    Args:
        vertex_data: Target array to receive vertex data
        index: Starting index in the target array
        *vertices: Variable number of vertex tuples to add

    Returns:
        Updated index pointing to next available position in vertex_data

    Unpacks vertex attribute tuples and adds them sequentially to the
    vertex data array. Each vertex tuple contains position, voxel ID,
    and face ID attributes.
    """
    for vertex in vertices:
        for attribute in vertex:
            vertex_data[index] = attribute
            index += 1
    return index


def build_chunk_mesh(chunk_voxels, format_size):
    """
    Build optimized vertex data for rendering a voxel chunk.

    Args:
        chunk_voxels: Array containing voxel data for the chunk
        format_size: Size of each vertex in the output format

    Returns:
        numpy array containing vertex data for all visible voxel faces

    This function converts 3D voxel data into optimized geometry for rendering.
    It implements face culling to avoid rendering faces that are adjacent to
    other voxels, significantly reducing the number of triangles rendered.
    Each visible face is converted to two triangles (6 vertices) with appropriate
    vertex attributes including position, voxel ID, and face ID.
    """
    vertex_data = np.empty(CHUNK_VOLUME * 18 * format_size, dtype='uint8')
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                if not voxel_id:
                    continue

                # Top face (vertex information for two triangles that form a face)
                if is_void((x, y + 1, z), chunk_voxels):
                    # Attribute tuple format: (x, y, z voxel_id, face_id)
                    v0 = (x,     y + 1, z,     voxel_id, 0)
                    v1 = (x + 1, y + 1, z,     voxel_id, 0)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = (x,     y + 1, z + 1, voxel_id, 0)

                    # Add in counter-clockwise order
                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # Do the same for the other faces of the voxel

                # Bottom face
                if is_void((x, y - 1, z), chunk_voxels):
                    v0 = (x,     y, z,     voxel_id, 1)
                    v1 = (x + 1, y, z,     voxel_id, 1)
                    v2 = (x + 1, y, z + 1, voxel_id, 1)
                    v3 = (x,     y, z + 1, voxel_id, 1)

                    # Add in counter-clockwise order
                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # Right face
                if is_void((x + 1, y, z), chunk_voxels):
                    v0 = (x + 1, y,     z,     voxel_id, 2)
                    v1 = (x + 1, y + 1, z,     voxel_id, 2)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = (x + 1, y,     z + 1, voxel_id, 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Left face
                if is_void((x - 1, y, z), chunk_voxels):
                    v0 = (x, y,     z,     voxel_id, 3)
                    v1 = (x, y + 1, z,     voxel_id, 3)
                    v2 = (x, y + 1, z + 1, voxel_id, 3)
                    v3 = (x, y,     z + 1, voxel_id, 3)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Back face
                if is_void((x, y, z - 1), chunk_voxels):
                    v0 = (x,     y,     z, voxel_id, 4)
                    v1 = (x,     y + 1, z, voxel_id, 4)
                    v2 = (x + 1, y + 1, z, voxel_id, 4)
                    v3 = (x + 1, y,     z, voxel_id, 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Front face
                if is_void((x, y, z + 1), chunk_voxels):
                    v0 = (x,     y,     z + 1, voxel_id, 5)
                    v1 = (x,     y + 1, z + 1, voxel_id, 5)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = (x + 1, y    , z + 1, voxel_id, 5)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index + 1]