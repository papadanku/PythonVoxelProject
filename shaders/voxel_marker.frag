
#version 330 core

/*
    Voxel Marker Fragment Shader

    This shader handles the final pixel coloring for the voxel marker. It:
    - Samples the base texture for the marker cube
    - Adds the interaction mode color to create visual distinction
    - Controls transparency to create a semi-transparent effect
    - Outputs the final marker color with appropriate alpha
*/

layout (location = 0) out vec4 fragColor;

in vec3 marker_color;
in vec2 uv;

uniform sampler2D u_texture_0;

void main()
{
    // Sample the base texture
    fragColor = texture(u_texture_0, uv);

    // Add the interaction mode color to create visual distinction
    fragColor.rgb += marker_color;

    // Control transparency: make transparent if red+blue channels are strong
    // This creates a semi-transparent effect for the marker
    fragColor.a = (fragColor.r + fragColor.b > 1.0) ? 0.0 : 1.0;
}
