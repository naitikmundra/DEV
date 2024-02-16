// bloom_fragment_shader.glsl
#version 330 core

in vec2 TexCoord;

out vec4 FragColor;

uniform sampler2D screenTexture;

void main()
{
    // Sample screen texture
    vec4 texColor = texture(screenTexture, TexCoord);

    // Apply bloom effect (e.g., blur)

    // Output final color
    FragColor = texColor;
}
