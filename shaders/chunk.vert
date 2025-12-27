
#version 330 core

/*
    Chunk Vertex Shader

    This shader processes voxel geometry for rendering. It handles:
    - Vertex position transformation using MVP matrices
    - Texture coordinate generation based on vertex ID and face orientation
    - Procedural voxel coloring using hash functions
    - Output of interpolated values to fragment shader
*/

layout (location = 0) in ivec3 in_position;
layout (location = 1) in int voxel_id;
layout (location = 2) in int face_id;

uniform mat4 m_projection;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 voxel_color;
out vec2 uv;

const vec2 uv_coords[4] = vec2[4](
    vec2(0.0, 0.0), vec2(0.0, 1.0),
    vec2(1.0, 0.0), vec2(1.0, 1.0)
);

const int uv_indices[12] = int[12](
    1, 0, 2, 1, 2, 3, // Texture coordinate indices for vertices of an *even* face.
    3, 0, 2, 3, 1, 0 // Texture coordinate indices for vertices of an *odd* face.
);

/*
    Procedural hash function for generating unique colors from voxel IDs
    Uses fractional operations to create pseudo-random but deterministic colors
*/
vec3 hash31(float p)
{
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1030, 0.0973));
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xxy + p3.yzz) * p3.zyx) + 0.05;
}

void main()
{
    // Calculate texture coordinates using the vertex ID
    // Different face orientations use different UV coordinate patterns
    int uv_index = gl_VertexID % 6 + (face_id & 1) * 6;
    uv = uv_coords[uv_indices[uv_index]];

    // Generate procedural color based on voxel ID
    voxel_color = hash31(voxel_id);

    // Transform vertex position using model-view-projection matrices
    gl_Position = m_projection * m_view * m_model * vec4(in_position, 1.0);
}
