#version 330 core
in vec2 frag_texCoord;
out vec4 color;

uniform float u_Width;
uniform sampler2D u_Texture;

void drawLines(vec2 coordinate);

void main() {
    vec2 coord = vec2(gl_FragCoord.x, gl_FragCoord.y);
    vec4 texColor = texture(u_Texture, frag_texCoord);
    color = texColor;
    drawLines(coord);
}

void drawLines(vec2 coordinate){
    float xMod = mod(coordinate.x, 120);
    float yMod = mod(coordinate.y, 120);
    if (xMod < u_Width || (120 - u_Width) < xMod) {
        color = vec4(1, 1, 1, 1);
    }else if (yMod < u_Width || (120 - u_Width) < yMod) {
        color = vec4(1, 1, 1, 1);
    }
}