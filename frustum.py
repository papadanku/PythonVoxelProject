
from settings import *

class Frustum:
    """
    Frustum culling class for optimizing chunk rendering.

    The Frustum class implements sphere-based frustum culling to determine which chunks are visible from the camera's perspective. It calculates frustum planes and checks if chunk bounding spheres intersect with the view frustum, allowing the engine to skip rendering chunks that are outside the visible area.

    :var camera: Reference to the Camera instance for view information
    :var factor_y: Y-axis scaling factor for frustum calculations
    :var tan_y: Tangent of half the vertical field of view
    :var factor_x: X-axis scaling factor for frustum calculations
    :var tan_x: Tangent of half the horizontal field of view
    """

    def __init__(self, camera):
        """
        Initialize the frustum with camera reference and calculate frustum parameters.

        :param camera: Reference to the Camera instance providing view information
        """
        self.camera: Camera = camera

        # Calculate Y-axis frustum parameters
        self.factor_y = 1.0 / math.cos(half_y := FOV_VERTICAL * 0.5)
        self.tan_y = math.tan(half_y)

        # Calculate X-axis frustum parameters
        self.factor_x = 1.0 / math.cos(half_x := FOV_HORIZONTAL * 0.5)
        self.tan_x = math.tan(half_x)
    
    def is_on_frustum(self, chunk):
        """
        Check if a chunk is visible within the camera's view frustum.

        Performs sphere-based frustum culling by checking if the chunk's bounding sphere intersects with the view frustum. The chunk is represented as a sphere centered at its geometric center with a radius equal to half the chunk size.

        :param chunk: Chunk object to check for visibility
        :return: True if the chunk is visible, False if it should be culled
        :rtype: bool
        """
        # Calculate vector from camera to chunk center
        sphere_vector = chunk.center - self.camera.position

        # Check if chunk is within near and far clipping planes
        sz = glm.dot(sphere_vector, self.camera.forward)
        if not ((NEAR - CHUNK_SPHERE_RADIUS) <= sz <= (FAR + CHUNK_SPHERE_RADIUS)):
            return False

        # Check if chunk is within top and bottom frustum planes
        sy = glm.dot(sphere_vector, self.camera.up)
        distance = self.factor_y * CHUNK_SPHERE_RADIUS + sz * self.tan_y
        if not (-distance <= sy <= distance):
            return False

        # Check if chunk is within left and right frustum planes
        sx = glm.dot(sphere_vector, self.camera.right)
        distance = self.factor_x * CHUNK_SPHERE_RADIUS + sz * self.tan_x
        if not (-distance <= sx <= distance):
            return False

        # Chunk is visible if all checks pass
        return True
