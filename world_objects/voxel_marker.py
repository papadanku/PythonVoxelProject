
from settings import *
from meshes.cube_mesh import CubeMesh

class VoxelMarker:
    """
    Visual marker for indicating targeted voxels in the 3D world.

    The VoxelMarker class provides a visual indicator that shows which voxel the player is currently targeting. It displays a small cube that changes color based on the interaction mode (red for removal, blue for addition).

    The marker helps players understand which voxel will be affected by their next action.

    :var engine: Reference to the main VoxelEngine instance
    :var handler: Reference to the VoxelHandler for targeting information
    :var position: Current world position of the marker
    :var m_model: Model matrix for marker transformation
    :var mesh: CubeMesh object for rendering the marker
    """

    def __init__(self, voxel_handler):
        """
        Initialize the voxel marker with voxel handler reference.

        :param voxel_handler: Reference to the VoxelHandler providing targeting data
        """
        self.engine = voxel_handler.engine
        self.handler = voxel_handler
        self.position = glm.vec3(0)
        self.m_model = self.get_model_matrix()
        self.mesh = CubeMesh(self.engine)

    def update(self):
        """
        Update the marker position based on current voxel targeting.

        Positions the marker at the targeted voxel location. In add mode, the marker appears adjacent to the targeted voxel face. In remove mode, the marker appears at the center of the targeted voxel.
        """
        if self.handler.voxel_id:
            if self.handler.interaction_mode:
                self.position = self.handler.voxel_world_position + self.handler.voxel_normal
            else:
                self.position = self.handler.voxel_world_position

    def set_uniform(self):
        """
        Update shader uniforms for marker rendering.

        Sets the interaction mode uniform to control marker color and updates the model matrix to position the marker correctly.
        """
        self.mesh.program['mode_id'] = self.handler.interaction_mode
        self.mesh.program['m_model'].write(self.get_model_matrix())

    def get_model_matrix(self):
        """
        Calculate the model matrix for the marker.

        Creates a transformation matrix that positions the marker cube at the current marker position in world space.

        :return: Model matrix for marker transformation
        :rtype: mat4
        """
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position))
        return m_model

    def render(self):
        """
        Render the voxel marker if a voxel is currently targeted.

        Only renders the marker when a valid voxel is targeted by the ray-casting system. Updates uniforms and delegates rendering to the cube mesh.
        """
        if self.handler.voxel_id:
            self.set_uniform()
            self.mesh.render()
