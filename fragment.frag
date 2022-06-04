#version 330 core
in vec2 frag_texCoord;
out vec4 color;

uniform float width;
uniform sampler2D tiles[32];
uniform int world[144];

void drawLines(vec2 coordinate);

int UP = 0;
int RIGHT = 1;
int DOWN = 2;
int LEFT = 3;

void main() {
    vec2 coord = vec2(gl_FragCoord.x, gl_FragCoord.y);
    vec2 y_flipped = vec2(coord.x, 1080 - coord.y);
    vec2 world_position = vec2(floor(y_flipped.x / 120), floor(y_flipped.y / 120));
    int tile_index = int(floor(world_position.y * 16)) + int(floor(world_position.x));

    vec2 mapped_texCoord = vec2(frag_texCoord.x * 16, frag_texCoord.y * 9);

    int texture_number = 31 & world[tile_index];
    int direction = 3 & (world[tile_index] >> 5);

    vec2 transformed_coord;
    if (direction == UP) {
        transformed_coord = mapped_texCoord;
    } else if (direction == RIGHT) {
        transformed_coord = vec2(-mapped_texCoord.y, mapped_texCoord.x);
    } else if (direction == DOWN) {
        transformed_coord = vec2(mapped_texCoord.x, -mapped_texCoord.y);
    } else if (direction == LEFT) {
        transformed_coord = vec2(mapped_texCoord.y, -mapped_texCoord.x);
    }

    color = texture(tiles[texture_number], transformed_coord);
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