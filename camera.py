
from settings import *

class Camera:
    """
    3D camera class that manages view projection and spatial orientation.

    The Camera class handles first-person view calculations including
    position, orientation (yaw/pitch), and movement in 3D space.
    It generates view and projection matrices for 3D rendering.
    """

    def __init__(self, position, yaw, pitch):
        """
        Initialize the camera with position and orientation.

        Args:
            position: Initial 3D position as a vector
            yaw: Initial horizontal rotation in degrees
            pitch: Initial vertical rotation in degrees
        """
        # Positional settings
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_projection = glm.perspective(FOV_VERTICAL, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

    def update(self):
        """
        Update camera orientation and view matrix.

        Recalculates camera vectors and updates the view matrix
        based on current position and orientation.
        """
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        """
        Recalculate the view matrix based on current camera state.

        Uses lookAt to create a view matrix that transforms world
        coordinates to camera space using current position and orientation.
        """
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        """
        Recalculate camera orientation vectors.

        Updates the forward, right, and up vectors based on current
        yaw and pitch angles. Ensures vectors remain orthogonal and normalized.
        """
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        """
        Rotate camera vertically around the X-axis.

        Args:
            delta_y: Amount to rotate in radians (positive = look up)

        Clamps pitch to prevent camera flipping at extremes.
        """
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        """
        Rotate camera horizontally around the Y-axis.

        Args:
            delta_x: Amount to rotate in radians (positive = look right)
        """
        self.yaw += delta_x

    def move_left(self, velocity):
        """
        Move camera left relative to current orientation.

        Args:
            velocity: Distance to move
        """
        self.position -= self.right * velocity

    def move_right(self, velocity):
        """
        Move camera right relative to current orientation.

        Args:
            velocity: Distance to move
        """
        self.position += self.right * velocity

    def move_up(self, velocity):
        """
        Move camera up relative to current orientation.

        Args:
            velocity: Distance to move
        """
        self.position += self.up * velocity

    def move_down(self, velocity):
        """
        Move camera down relative to current orientation.

        Args:
            velocity: Distance to move
        """
        self.position -= self.up * velocity

    def move_forward(self, velocity):
        """
        Move camera forward relative to current orientation.

        Args:
            velocity: Distance to move
        """
        self.position += self.forward * velocity

    def move_backward(self, velocity):
        """
        Move camera backward relative to current orientation.

        Args:
            velocity: Distance to move
        """
        self.position -= self.forward * velocity
