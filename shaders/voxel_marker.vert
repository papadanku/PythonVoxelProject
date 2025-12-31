
#version 330 core

/*
    Voxel Marker Vertex Shader

    This shader handles the rendering of the voxel marker cube that indicates
    which voxel the player is currently targeting. It handles:
    - Vertex position transformation using MVP matrices
    - Texture coordinate passing to fragment shader
    - Color selection based on interaction mode
    - Slight size adjustment to prevent Z-fighting with voxel geometry
*/

layout (location = 0) in vec2 in_tex_coord_0;
layout (location = 1) in vec3 in_position;

uniform mat4 m_projection;
uniform mat4 m_view;
uniform mat4 m_model;
uniform uint mode_id;

// Color array for different interaction modes
// 0: Remove mode (red), 1: Add mode (blue)
const vec3 marker_colors[2] = vec3[2](vec3(1, 0, 0), vec3(0, 0, 1));

out vec3 marker_color;
out vec2 uv;

void main()
{
    // Pass texture coordinates to fragment shader
    uv = in_tex_coord_0;

    // Select color based on current interaction mode
    marker_color = marker_colors[mode_id];

    // We slightly increase the cube size to prevent Z-fighting.
    // This ensures the marker renders on top of the targeted voxel.
    gl_Position = m_projection * m_view * m_model * vec4((in_position - 0.5) * 1.01 + 0.5, 1.0);
}
