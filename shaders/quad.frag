
#version 330 core

/*
    Quad Fragment Shader

    Simple fragment shader for rendering colored quads. Used primarily
    for debugging and testing purposes. Simply outputs the interpolated
    vertex color with full opacity.
*/

layout (location = 0) out vec4 fragColor;

in vec3 color;

void main() {
    // Output the interpolated color with full opacity
    fragColor = vec4(color, 1.0);
}
