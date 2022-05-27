#version 330 core
uniform int map[144];
uniform float width;
out vec4 color;
in vec2 texture_coord;

void drawLines(vec2 coordinate);
uniform sampler2D input_texture;

void main() {
    //vec2 coord = vec2(gl_FragCoord.x, gl_FragCoord.y);
    //vec2 world_coord = coord / 120;
    //world_coord = floor(world_coord);
    color = vec4(1, 1, 1, 1);//texture(input_texture, texture_coord);
    //drawLines(coord);
}

void drawLines(vec2 coordinate){
    float xMod = mod(coordinate.x, 120);
    float yMod = mod(coordinate.y, 120);
    if (xMod < width || (120 - width) < xMod) {
        color = vec4(1, 1, 1, 1);
    }else if (yMod < width || (120 - width) < yMod) {
        color = vec4(1, 1, 1, 1);
    }
}