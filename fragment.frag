#version 330 core
uniform int map[144];
uniform float width;
out vec4 color;

void drawLines(vec2 coordinate);

void main() {
    vec2 coord = vec2(gl_FragCoord.x, gl_FragCoord.y);
    drawLines(coord);
}

void drawLines(vec2 coordinate){
    float xMod = mod(coordinate.x, 120);
    float yMod = mod(coordinate.y, 120);
    if (xMod < width || (120 - width) < xMod) {
        color = vec4(1, 1, 1, 1);
    }else if (yMod < width || (120 - width) < yMod) {
        color = vec4(1, 1, 1, 1);
    }else color = vec4(0, 0, 0, 0);
}