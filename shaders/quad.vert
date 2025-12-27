
#version 330 core

/*
    Quad Vertex Shader

    Simple vertex shader for rendering colored 2D quads. Used primarily
    for debugging and testing purposes. Handles:
    - Vertex position transformation using MVP matrices
    - Color passing to fragment shader
*/

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_color;

uniform mat4 m_projection;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 color;

void main() {
    // Pass vertex color to fragment shader
    color = in_color;

    // Transform vertex position using model-view-projection matrices
    gl_Position = m_projection * m_view * m_model * vec4(in_position, 1.0);
}
