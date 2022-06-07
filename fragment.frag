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

    if (texture_number == 0) color = texture(tiles[0], transformed_coord);
    if (texture_number == 1) color = texture(tiles[1], transformed_coord);
    if (texture_number == 2) color = texture(tiles[2], transformed_coord);
    if (texture_number == 3) color = texture(tiles[3], transformed_coord);
    if (texture_number == 4) color = texture(tiles[4], transformed_coord);
    if (texture_number == 5) color = texture(tiles[5], transformed_coord);
    if (texture_number == 6) color = texture(tiles[6], transformed_coord);
    if (texture_number == 7) color = texture(tiles[7], transformed_coord);
    if (texture_number == 8) color = texture(tiles[8], transformed_coord);
    if (texture_number == 9) color = texture(tiles[9], transformed_coord);
    if (texture_number == 10) color = texture(tiles[10], transformed_coord);
    if (texture_number == 11) color = texture(tiles[11], transformed_coord);
    if (texture_number == 12) color = texture(tiles[12], transformed_coord);
    if (texture_number == 13) color = texture(tiles[13], transformed_coord);
    if (texture_number == 14) color = texture(tiles[14], transformed_coord);
    if (texture_number == 15) color = texture(tiles[15], transformed_coord);
    if (texture_number == 16) color = texture(tiles[16], transformed_coord);
    if (texture_number == 17) color = texture(tiles[17], transformed_coord);
    if (texture_number == 18) color = texture(tiles[18], transformed_coord);
    if (texture_number == 19) color = texture(tiles[19], transformed_coord);
    if (texture_number == 20) color = texture(tiles[20], transformed_coord);
    if (texture_number == 21) color = texture(tiles[21], transformed_coord);
    if (texture_number == 22) color = texture(tiles[22], transformed_coord);
    if (texture_number == 23) color = texture(tiles[23], transformed_coord);
    if (texture_number == 24) color = texture(tiles[24], transformed_coord);
    if (texture_number == 25) color = texture(tiles[25], transformed_coord);
    if (texture_number == 26) color = texture(tiles[26], transformed_coord);
    if (texture_number == 27) color = texture(tiles[27], transformed_coord);
    if (texture_number == 28) color = texture(tiles[28], transformed_coord);
    if (texture_number == 29) color = texture(tiles[29], transformed_coord);
    if (texture_number == 30) color = texture(tiles[30], transformed_coord);
    if (texture_number == 31) color = texture(tiles[31], transformed_coord);

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