
#version 330 core

/*
    Chunk Fragment Shader

    This shader handles the final pixel coloring for voxel rendering. It:
    - Samples texture data and applies gamma correction
    - Combines texture colors with procedural voxel colors
    - Applies inverse gamma correction for final output
    - Outputs the final fragment color
*/

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inverse_gamma = 1.0 / gamma;

uniform sampler2DArray u_texture_array_0;

in vec3 voxel_color;
in vec2 uv;
in float shading;

flat in int voxel_id;
flat in int face_id;

void main()
{
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    // Sample texture color and apply gamma correction
    vec3 tex_color = texture(u_texture_array_0, vec3(face_uv, voxel_id)).rgb;
    tex_color = pow(tex_color, gamma);

    // Combine texture color with procedural voxel color
    tex_color *= voxel_color;

    // Multiply by the face id.
    tex_color *= shading;

    // Apply inverse gamma correction for final output
    tex_color = pow(tex_color, inverse_gamma);

    // Output final color with full opacity
    fragColor = vec4(vec3(tex_color), 1.0);
}
