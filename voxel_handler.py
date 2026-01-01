
from settings import *
from meshes.chunk_mesh_builder import get_chunk_index

class VoxelHandler:
    """
    Voxel interaction and ray-casting handler for the voxel engine.

    The VoxelHandler class manages voxel manipulation through ray-casting from the player's perspective. It handles voxel addition, removal, and interaction mode switching. The class performs ray-casting to determine which voxel the player is looking at and provides methods for modifying the voxel world.

    :var engine: Reference to the main VoxelEngine instance
    :var chunks: Array of all chunks in the world
    :var chunk: Current chunk containing the targeted voxel
    :var voxel_id: ID of the voxel currently targeted by ray-casting
    :var voxel_index: Index of the targeted voxel within its chunk
    :var voxel_local_position: Local coordinates of the targeted voxel within its chunk
    :var voxel_world_position: World coordinates of the targeted voxel
    :var voxel_normal: Normal vector of the targeted voxel face
    :var interaction_mode: Current interaction mode (0 = remove, 1 = add)
    :var new_voxel_id: ID to use when adding new voxels
    """

    def __init__(self, world):
        """
        Initialize the voxel handler with world reference.

        :param world: Reference to the parent World instance
        """
        self.engine = world.engine
        self.chunks = world.chunks

        # Store ray-casting results for targeted voxel
        self.chunk = None
        self.voxel_id = None
        self.voxel_index = None
        self.voxel_local_position = None
        self.voxel_world_position = None
        self.voxel_normal = None

        # Set interaction mode: 0 removes voxels, 1 adds voxels
        self.interaction_mode = 0
        self.new_voxel_id = 1

    def add_voxel(self):
        """
        Add a new voxel at the position adjacent to the targeted voxel face.

        Checks if the position adjacent to the targeted voxel face is empty. If empty, places a new voxel with the current new_voxel_id and updates the chunk's mesh. Also handles empty chunk activation.
        """
        if self.voxel_id:
            # Check if the adjacent position is empty
            result = self.get_voxel_id(self.voxel_world_position + self.voxel_normal)

            # Place voxel if the adjacent position is empty
            if not result[0]:

                # Extract voxel data from result
                voxel_index = result[1]
                chunk = result[3]

                # Add the new voxel
                chunk.voxels[voxel_index] = self.new_voxel_id
                chunk.mesh.rebuild()

                # Activate chunk if it was previously empty
                if chunk.is_empty:
                    chunk.is_empty = False

    def rebuild_adjacent_chunk(self, adjacent_voxel_position):
        """
        Rebuild the mesh for a single adjacent chunk.

        :param adjacent_voxel_position: World coordinates of the voxel position to check

        Checks if the position belongs to a valid chunk and rebuilds that chunk's mesh if it exists. Used when voxel changes affect neighboring chunks.
        """
        index = get_chunk_index(adjacent_voxel_position)

        # Only do this for valid chunks
        if index != -1:
            self.chunks[index].mesh.rebuild()

    def rebuild_adjacent_chunks(self):
        """
        Rebuild meshes for all adjacent chunks that may be affected by voxel changes.

        Checks if the modified voxel is at the border of its chunk and rebuilds the meshes of all adjacent chunks that share faces with the modified voxel.

        This ensures that face culling remains correct when voxels are added or removed at chunk boundaries.
        """
        lx, ly, lz = self.voxel_local_position
        wx, wy, wz = self.voxel_world_position

        # Check if voxel is at chunk borders and rebuild adjacent chunks
        if lx == 0:
            self.rebuild_adjacent_chunk((wx - 1, wy, wz))
        elif lx == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx + 1, wy, wz))

        if ly == 0:
            self.rebuild_adjacent_chunk((wx, wy - 1, wz))
        elif ly == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx, wy + 1, wz))

        if lz == 0:
            self.rebuild_adjacent_chunk((wx, wy, wz - 1))
        elif lz == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx, wy, wz + 1))

    def remove_voxel(self):
        """
        Remove the currently targeted voxel.

        Sets the targeted voxel's ID to 0 (empty), rebuilds the chunk's mesh, and triggers rebuilding of adjacent chunks if the removed voxel was at a chunk boundary. This ensures proper face culling after removal.
        """
        if self.voxel_id:
            # Remove voxel by setting its ID to 0
            self.chunk.voxels[self.voxel_index] = 0

            # Update chunk mesh to reflect the removal
            self.chunk.mesh.rebuild()

            # Update adjacent chunks if we removed a border voxel
            self.rebuild_adjacent_chunks()

    def set_voxel(self):
        """
        Add or remove a voxel based on the current interaction mode.

        Calls add_voxel() if in add mode (interaction_mode = 1) or remove_voxel() if in remove mode (interaction_mode = 0).
        """
        if self.interaction_mode:
            self.add_voxel()
        else:
            self.remove_voxel()

    def switch_mode(self):
        """
        Toggle between voxel addition and removal modes.

        Switches between add mode (interaction_mode = 1) and remove mode (interaction_mode = 0) when the player presses the right mouse button.
        """
        self.interaction_mode = not self.interaction_mode

    def update(self):
        """
        Update the voxel handler by performing ray-casting.

        Called every frame to update the targeted voxel based on the player's current position and view direction.
        """
        self.cast_ray()

    def cast_ray(self):
        """
        Perform ray-casting from the player's position to determine targeted voxel.

        Implements a 3D Digital Differential Analyzer (DDA) algorithm to cast a ray from the player's camera position in the direction they are looking. The ray marches through the voxel grid until it hits a solid voxel or exceeds the maximum ray distance. Updates voxel targeting information including position, normal vector, and chunk reference.

        :return: True if a voxel was hit, False if no voxel was hit within range
        :rtype: bool
        """
        # Start ray-casting from camera position
        x1, y1, z1 = self.engine.player.position

        # Calculate ray end point using player's view direction
        x2, y2, z2 = self.engine.player.position + self.engine.player.forward * MAX_RAY_DISTANCE

        # Initialize ray-casting variables
        current_voxel_position = glm.ivec3(x1, y1, z1)
        self.voxel_id = 0
        self.voxel_normal = glm.ivec3(0)

        # Track which axis we stepped along (0: X, 1: Y, 2: Z)
        step_direction = -1

        dx = glm.sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        # March along the ray until we exceed maximum distance
        # Check each voxel position to determine if it contains a solid voxel
        while not ((max_x > 1.0) and (max_y > 1.0) and (max_z > 1.0)):
            # Check if current voxel position contains a solid voxel
            result = self.get_voxel_id(voxel_world_position=current_voxel_position)

            if result[0]:

                # Extract voxel data from result
                self.voxel_id = result[0]
                self.voxel_index = result[1]
                self.voxel_local_position = result[2]
                self.chunk = result[3]
                self.voxel_world_position = current_voxel_position

                # Determine which face of the voxel was hit based on step direction
                if step_direction == 0:
                    self.voxel_normal.x = -dx
                elif step_direction == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return True

            # Advance to the next voxel along the ray path
            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_position.x += dx
                    max_x += delta_x
                    step_direction = 0
                else:
                    current_voxel_position.z += dz
                    max_z += delta_z
                    step_direction = 2
            else:
                if max_y < max_z:
                    current_voxel_position.y += dy
                    max_y += delta_y
                    step_direction = 1
                else:
                    current_voxel_position.z += dz
                    max_z += delta_z
                    step_direction = 2

        # Return False if no voxel was hit within maximum range
        return False

    def get_voxel_id(self, voxel_world_position):
        """
        Get voxel information at a specific world position.

        :param voxel_world_position: World coordinates to check for voxel data
        :return: Tuple containing (voxel_id, voxel_index, voxel_local_position, chunk)
        :rtype: tuple

        Converts world coordinates to chunk coordinates and calculates the voxel index within that chunk. Returns voxel data if the position is within valid world bounds, or zeros if out of bounds.
        """
        cx, cy, cz = chunk_position = voxel_world_position / CHUNK_SIZE

        # Check if chunk position is within valid world bounds
        if (0 <= cx < WORLD_WIDTH) and (0 <= cy < WORLD_HEIGHT) and (0 <= cz < WORLD_DEPTH):

            # Get the chunk and its index
            chunk_index = cx + WORLD_WIDTH * cz + WORLD_AREA * cy
            chunk = self.chunks[chunk_index]

            lx, ly, lz = voxel_local_position = voxel_world_position - chunk_position * CHUNK_SIZE

            # Get the voxel and its index
            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            voxel_id = chunk.voxels[voxel_index]

            # Return voxel data
            return voxel_id, voxel_index, voxel_local_position, chunk

        return 0, 0, 0, 0
