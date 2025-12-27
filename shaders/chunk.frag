
#version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inverse_gamma = 1.0 / gamma;

uniform sampler2D u_texture_0;

in vec3 voxel_color;
in vec2 uv;

void main()
{
    vec3 tex_color = texture(u_texture_0, uv).rgb;
    tex_color = pow(tex_color, gamma);
    tex_color *= voxel_color;
    tex_color = pow(tex_color, inverse_gamma);
    fragColor = vec4(vec3(tex_color), 1.0);
}
