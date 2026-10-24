import pygame
import pytmx.util_pygame
selected = []
photoS = []
Uncopiable = [335,332 , 331,330]
def load_map(tmxdata, screen , map_cords):
    for layer in tmxdata.visible_layers:
        for x, y, image in layer.tiles():
            x_pixel = x * tmxdata.tilewidth
            y_pixel = y * tmxdata.tileheight

            if layer.name == "Tile Layer 2":
             continue

            screen.blit(image, (x_pixel, y_pixel))

def draw_layer2(tmxdata, screen, map_cords):
    for x, y, image in tmxdata.get_layer_by_name("Tile Layer 2").tiles():
        screen.blit(image, (x * tmxdata.tilewidth + map_cords.x,
                            y * tmxdata.tileheight + map_cords.y))


def Get_tile(tmxdata,player):#For player
    tile_layer = tmxdata.get_layer_by_name("Tile Layer 1")
    x_tile = int(player.pos.x // tmxdata.tilewidth)
    y_tile =  int(player.pos.y // tmxdata.tileheight)
    tile_internal_id = tile_layer.data[y_tile][x_tile] # gets  the tile that in the positon of x_tile and y_tile in the grid
    tile_id = tmxdata.tiledgidmap[tile_internal_id] # gets the image id of the tile in []
    return tile_id

def get_tile_cords(tmxdata, tileid):
    tile_layer = tmxdata.get_layer_by_name("Tile Layer 1")
    for y in range(tmxdata.height):
        for x in range(tmxdata.width):
            tile_id = tmxdata.tiledgidmap.get(tile_layer.data[y][x])
            if tile_id == tileid:
                pos = (x * tmxdata.tilewidth + tmxdata.tilewidth // 2, y * tmxdata.tileheight + tmxdata.tileheight // 2)
                return pos
    return None

def Get_CrossTile(tmxdata):
    tile_layer = tmxdata.get_layer_by_name("Tile Layer 1")
    mouse_x, mouse_y = pygame.mouse.get_pos()
    x_tile = mouse_x // tmxdata.tilewidth
    y_tile = mouse_y // tmxdata.tileheight

    values = []
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            values.append(tile_layer.data[y_tile + dy][x_tile + dx])

    # if ANY tile in the 3x3 is banned, refuse the whole photo
    if any(tmxdata.tiledgidmap.get(i) in Uncopiable for i in values):
        return None

    photoS.clear()
    photoS.extend(values)
    return photoS


def Select_CrossTile(tmxdata):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    x_tile = mouse_x // tmxdata.tilewidth
    y_tile = mouse_y // tmxdata.tileheight

    selected.clear()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            x = x_tile + dx
            y = y_tile + dy
            selected.append((x, y))
def draw_selected(tmxdata, screen , colour):
    for x, y in selected:
        pygame.draw.rect(screen, colour,
                 (x * tmxdata.tilewidth, y * tmxdata.tileheight,
                  tmxdata.tilewidth, tmxdata.tileheight), 2)

def place_photo(tmxdata , photo , lock):
    fire = tmxdata.register_gid(334)
    FinishR = tmxdata.register_gid(335)
    BlueTeleport = tmxdata.register_gid(330)
    RedTeleport = tmxdata.register_gid(331)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    tile_layer = tmxdata.get_layer_by_name("Tile Layer 1")
    x_tile = mouse_x // tmxdata.tilewidth
    y_tile =   mouse_y // tmxdata.tileheight
    for i, value in enumerate(photo):
        x = x_tile - 1 + i % 3   
        y = y_tile - 1 + i // 3   
        if tile_layer.data[y][x] == FinishR or tile_layer.data[y][x] == BlueTeleport or tile_layer.data[y][x] == RedTeleport:
         continue
        if tile_layer.data[y][x] == fire and lock == False:
          continue
        tile_layer.data[y][x] = value
    photoS.clear()
def get_tile_in_photo(tmxdata , photo):
    if photo is None:
        return False
    for value in photo:
            if tmxdata.tiledgidmap.get(value) == 329:
               print("aaa")
               return True
    return False


def update_strogae(tmxdata , photo):
    layer2 = tmxdata.get_layer_by_name("Tile Layer 2")
    x_tile =  1
    y_tile =   1
    for i, value in enumerate(photo):
        x = x_tile - 1 + i % 3   
        y = y_tile - 1 + i // 3   
        layer2.data[y][x] = value

def clear_strogae(tmxdata):
    layer2 = tmxdata.get_layer_by_name("Tile Layer 2")
    empty = tmxdata.register_gid(326)
    x_tile =  1
    y_tile =   1
    for i in range(9):
        x = x_tile - 1 + i % 3   
        y = y_tile - 1 + i // 3
        layer2.data[y][x] = empty

def trow_away(tmxdata):
    clear_strogae(tmxdata)
    photoS.clear()

def Blocked_photo(tmxdata):
    tile_layer = tmxdata.get_layer_by_name("Tile Layer 1")
    mouse_x , mouse_y = pygame.mouse.get_pos()
    x_tile = mouse_x // tmxdata.tilewidth
    y_tile = mouse_y // tmxdata.tileheight 
    for dy in (-1 , 0 ,1 ):
        for dx in (-1 , 0 , 1 ):
            y = y_tile + dy
            x = x_tile + dx
            if 0 <= y <tmxdata.height and 0 <=x < tmxdata.width:
                if tmxdata.tiledgidmap.get(tile_layer.data[y][x]) in Uncopiable:
                    return True

    
