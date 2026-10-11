import pygame
import pytmx.util_pygame
def load_map(tmxdata , screen):
    for layer in tmxdata:
        for tile in layer.tiles():
            #tile[0] is the x position 
            # tile[1] is the y position 
            # tile[2] is the image
            x_pixel = tile[0] * tmxdata.tilewidth
            y_pixel = tile[1] * tmxdata.tileheight
            screen.blit(tile[2] , (x_pixel , y_pixel))


def Get_tile(tmxdata,player):
    tile_layer = tmxdata.get_layer_by_name("Tile Layer 1")
    x_tile = int(player.pos.x // tmxdata.tilewidth)
    y_tile =  int(player.pos.y // tmxdata.tileheight)
    tile_internal_id = tile_layer.data[y_tile][x_tile]
    tile_id = tmxdata.tiledgidmap[tile_internal_id]
    return tile_id

def Get_CrossTile(tmxdata):
    mouse_x , mouse_y = pygame.mouse.get_pos()
    x_tile = mouse_x // tmxdata.tilewidth
    y_tile =   mouse_y // tmxdata.tileheight
    print(x_tile , y_tile)

    
