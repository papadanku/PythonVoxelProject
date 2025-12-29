
#version 330 core

/*
    Chunk Vertex Shader

    This shader processes voxel geometry for rendering. It handles:
    - Vertex position transformation using MVP matrices
    - Texture coordinate generation based on vertex ID and face orientation
    - Procedural voxel coloring using hash functions
    - Output of interpolated values to fragment shader
*/

// Get the packed data
layout (location = 0) in uint packed_data;

int x, y, z;
int voxel_id;
int face_id;
int ao_id;
int flip_id;

uniform mat4 m_projection;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 voxel_color;
out vec2 uv;
out float shading;

const float ao_values[4] = float[4](0.1, 0.25, 0.5, 1.0);

const float face_shading[6] = float[6](
    1.0, 0.5, // Top, Bottom
    0.5, 0.8, // Right, Left
    0.5, 0.8 // Front, Back
);

const vec2 uv_coords[4] = vec2[4](
    vec2(0.0, 0.0), vec2(0.0, 1.0),
    vec2(1.0, 0.0), vec2(1.0, 1.0)
);

const int uv_indices[24] = int[24](
    1, 0, 2, 1, 2, 3, // Texture coordinate indices for vertices of an *even* face.
    3, 0, 2, 3, 1, 0, // Texture coordinate indices for vertices of an *odd* face.
    3, 1, 0, 3, 0, 2, // FLIPPED: Texture coordinate indices for vertices of an *even* face.
    1, 2, 3, 1, 0, 2 // FLIPPED: Texture coordinate indices for vertices of an *odd* face.
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

void unpack_vertex_data(uint packed_data)
{
    // a, b, c, d, e, f, g = x, y, z, voxel_id, face_id, ao_id, flip_id
    uint b_bit = 6u, c_bit = 6u, d_bit = 8u, e_bit = 3u, f_bit = 2u, g_bit = 1u;
    uint b_mask = 63u, c_mask = 63u, d_mask = 255u, e_mask = 7u, f_mask = 3u, g_mask = 1u;

    // Bit additions
    uint fg_bit = f_bit + g_bit;
    uint efg_bit = e_bit + fg_bit;
    uint defg_bit = d_bit + efg_bit;
    uint cdefg_bit = c_bit + defg_bit;
    uint bcdefg_bit = b_bit + cdefg_bit;

    // Unpack vertex data
    x = int(packed_data >> bcdefg_bit);
    y = int((packed_data >> cdefg_bit) & b_mask);
    z = int((packed_data >> defg_bit) & c_mask);

    voxel_id = int((packed_data >> efg_bit) & d_mask);
    face_id = int((packed_data >> fg_bit) & e_mask);
    ao_id = int((packed_data >> g_bit) & f_mask);
    flip_id = int(packed_data & g_mask);
}

void main()
{
    unpack_vertex_data(packed_data);
    vec3 in_position = vec3(x, y, z);

    // Calculate texture coordinates using the vertex ID
    // Different face orientations use different UV coordinate patterns
    int uv_index = gl_VertexID % 6 + ((face_id & 1) + flip_id * 2) * 6;
    uv = uv_coords[uv_indices[uv_index]];

    // Generate procedural color based on voxel ID
    voxel_color = hash31(voxel_id);

    // Shading value based on the face ID
    shading = face_shading[face_id] * ao_values[ao_id];

    // Transform vertex position using model-view-projection matrices
    gl_Position = m_projection * m_view * m_model * vec4(in_position, 1.0);
}
