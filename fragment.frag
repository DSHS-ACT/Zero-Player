#version 330 core
in vec2 frag_texCoord;
out vec4 color;

uniform float width;
uniform sampler2D tiles[32];
uniform int world[32 * 18];
uniform int holding;
uniform vec2 mouse_pos;

void drawLines(vec2 coordinate);
void draw_texture(int slot, vec2 coordinate, bool is_fixed);
void draw_holding(int slot, vec2 mouse_pos, vec2 texture_coordinate, vec2 screen_coordinate, vec2 mapped_texCoord);
vec2 rotate_vec2(int direction, vec2 to_rotate);

int UP = 0;
int RIGHT = 1;
int DOWN = 2;
int LEFT = 3;

void main() {
    vec2 coord = vec2(gl_FragCoord.x, gl_FragCoord.y);
    vec2 y_flipped = vec2(coord.x, 1080 - coord.y);
    vec2 world_position = vec2(floor(y_flipped.x / 60), floor(y_flipped.y / 60));
    int tile_index = int(floor(world_position.y * 32)) + int(floor(world_position.x));

    vec2 mapped_texCoord = vec2(frag_texCoord.x * 32, frag_texCoord.y * 18);

    int texture_number = 31 & world[tile_index]; //5
    int direction = 3 & (world[tile_index] >> 5); //2
    bool is_fixed = 1 == (1 & (world[tile_index] >> 7)); //1

    vec2 transformed_coord = rotate_vec2(direction, mapped_texCoord);

    draw_texture(texture_number, transformed_coord, is_fixed);

    drawLines(coord);

    if (holding != -1){
        draw_holding(holding, mouse_pos, frag_texCoord, y_flipped, mapped_texCoord);
    }
}

vec2 rotate_vec2(int direction, vec2 to_rotate) {
    if (direction == UP) {
        return to_rotate;
    } else if (direction == RIGHT) {
        return vec2(-to_rotate.y, to_rotate.x);
    } else if (direction == DOWN) {
        return vec2(to_rotate.x, -to_rotate.y);
    } else if (direction == LEFT) {
        return vec2(to_rotate.y, -to_rotate.x);
    }
    return vec2(0, 0);
}

void draw_texture(int slot, vec2 coordinate, bool is_fixed) {
    if (slot == 0) color = texture(tiles[0], coordinate);
    if (slot == 1) color = texture(tiles[1], coordinate);
    if (slot == 2) color = texture(tiles[2], coordinate);
    if (slot == 3) color = texture(tiles[3], coordinate);
    if (slot == 4) color = texture(tiles[4], coordinate);
    if (slot == 5) color = texture(tiles[5], coordinate);
    if (slot == 6) color = texture(tiles[6], coordinate);
    if (slot == 7) color = texture(tiles[7], coordinate);
    if (slot == 8) color = texture(tiles[8], coordinate);
    if (slot == 9) color = texture(tiles[9], coordinate);
    if (slot == 10) color = texture(tiles[10], coordinate);
    if (slot == 11) color = texture(tiles[11], coordinate);
    if (slot == 12) color = texture(tiles[12], coordinate);
    if (slot == 13) color = texture(tiles[13], coordinate);
    if (slot == 14) color = texture(tiles[14], coordinate);
    if (slot == 15) color = texture(tiles[15], coordinate);
    if (slot == 16) color = texture(tiles[16], coordinate);
    if (slot == 17) color = texture(tiles[17], coordinate);
    if (slot == 18) color = texture(tiles[18], coordinate);
    if (slot == 19) color = texture(tiles[19], coordinate);
    if (slot == 20) color = texture(tiles[20], coordinate);
    if (slot == 21) color = texture(tiles[21], coordinate);
    if (slot == 22) color = texture(tiles[22], coordinate);
    if (slot == 23) color = texture(tiles[23], coordinate);
    if (slot == 24) color = texture(tiles[24], coordinate);
    if (slot == 25) color = texture(tiles[25], coordinate);
    if (slot == 26) color = texture(tiles[26], coordinate);
    if (slot == 27) color = texture(tiles[27], coordinate);
    if (slot == 28) color = texture(tiles[28], coordinate);
    if (slot == 29) color = texture(tiles[29], coordinate);
    if (slot == 30) color = texture(tiles[30], coordinate);
    if (slot == 31) color = texture(tiles[31], coordinate);

    if (is_fixed) {
        color = color * 0.4;
    }
}

void drawLines(vec2 coordinate){
    float xMod = mod(coordinate.x, 60);
    float yMod = mod(coordinate.y, 60);
    if (xMod < width || (60 - width) < xMod) {
        color = vec4(1, 1, 1, 1);
    }else if (yMod < width || (60 - width) < yMod) {
        color = vec4(1, 1, 1, 1);
    }
}

void draw_holding(int holding, vec2 mouse_pos, vec2 texture_coordinate, vec2 screen_coordinate, vec2 mapped_texCoord) {
    vec2 difference = screen_coordinate - mouse_pos + vec2(30, 30);
    if (difference.x < 0 || difference.x > 60) return;
    if (difference.y < 0 || difference.y > 60) return;

    int texture_number = 31 & holding;
    int direction = 3 & (holding >> 5);
    bool is_fixed = 1 == (1 & (holding >> 7));

    vec2 mouse_transformed_coordinate =
        vec2(mapped_texCoord.x - (mouse_pos.x / 60), mapped_texCoord.y + (mouse_pos.y / 60));
    vec2 transformed_coordinate = rotate_vec2(direction, mouse_transformed_coordinate);
    draw_texture(texture_number, transformed_coordinate + vec2(0.5, 0.5), is_fixed);
}