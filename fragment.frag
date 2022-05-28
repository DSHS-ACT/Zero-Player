#version 330 core
in vec2 frag_texCoord;
out vec4 color;

uniform float width;
uniform sampler2D tiles[32];
uniform int world[144];

void drawLines(vec2 coordinate);

void main() {
    vec2 coord = vec2(gl_FragCoord.x, gl_FragCoord.y);
    vec2 y_flipped = vec2(coord.x, 1080 - coord.y);
    vec2 world_position = vec2(floor(y_flipped.x / 120), floor(y_flipped.y / 120));
    int tile_index = int(floor(world_position.y * 16)) + int(floor(world_position.x));

    vec2 mapped_texCoord = vec2(frag_texCoord.x * 16, frag_texCoord.y * 9);

    color = texture(tiles[world[tile_index]], mapped_texCoord);
    drawLines(coord);
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