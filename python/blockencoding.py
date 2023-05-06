import json
import cv2
import constants
from os import path

# Get average colour of a block
def __evaluate(img):
    SIZE = 16
    b, g, r = 0, 0, 0
    for i in range (SIZE):
        for j in range (SIZE):
            if img[i][j].size > 3 and img[i][j][3] == 0:  #if this image has tranparency dont include it
                return -1
            b += img[i][j][0]
            g += img[i][j][1]
            r += img[i][j][2]
    b = int(b / (SIZE * SIZE))
    g = int(g / (SIZE * SIZE))
    r = int(r / (SIZE * SIZE))
    return [b, g, r]

def getBlockData():
    # Load image file names
    with open("textures/_list.json") as file:
        data = json.load(file)

    # Get blocklist
    blocklist = data["files"]
    blockdata = []
    for block in blocklist:
        if path.splitext(block)[1] == ".png":
            img = cv2.imread("textures/" + block, cv2.IMREAD_UNCHANGED)
            colour = __evaluate(img)
            if (constants.reject_transparent and colour != -1):
                blockdata.append([colour, block])
            elif constants.show_rejected:
                print("Rejected " + block + " for transparency")
    
    return blockdata

def readAtlas():
    atlas = cv2.imread("textures/atlas.png")
    blockdata = []
    block_size = 16
    height, width, channels = atlas.shape
    for i in range(0, width, block_size):
        for j in range(0, height, block_size):

            #read each blocks colour and location and store it in the blockdata
            block = atlas[i:i+block_size, j:j+block_size]
            if (block.shape[0] != 0 and block.shape[1] != 0):
                colour = __evaluate(block)
                if (constants.reject_transparent and colour != -1):
                    blockdata.append([colour, [i, j]])
                elif constants.show_rejected:
                    print("Rejected " + block + " for transparency")
    #block = [colour, [index_x, index_y]]
    return blockdata