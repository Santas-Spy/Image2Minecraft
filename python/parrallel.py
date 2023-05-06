import numba
from numba import njit
import numpy as np
import math
import cv2
import constants

#unused, but cool
@njit
def pixellate(img, width, height):
    for i in range (int(width/constants.compress)):         #iterate across blocks
        for j in range (int(height/constants.compress)):    #iterate down blocks
            g, b, r = 0, 0, 0
            for x in range (constants.compress):            #average subblocks
                for y in range (constants.compress):        #average subblocks
                    g += img[i*constants.compress+x][j*constants.compress+y][0]
                    b += img[i*constants.compress+x][j*constants.compress+y][1]
                    r += img[i*constants.compress+x][j*constants.compress+y][2]
            g = g / (constants.compress * constants.compress)
            b = b / (constants.compress * constants.compress)
            r = r / (constants.compress * constants.compress)

            for x in range (constants.compress):            #fill subblocks
                for y in range (constants.compress):        #fill subblocks
                    img[i*constants.compress+x][j*constants.compress+y][0] = g
                    img[i*constants.compress+x][j*constants.compress+y][1] = b
                    img[i*constants.compress+x][j*constants.compress+y][2] = r
    return img

@njit
def getSubBlocks(img, width, height):
    data = []
    for i in range (int(width/constants.compress)):         #iterate across blocks
        for j in range (int(height/constants.compress)):    #iterate down blocks
            g, b, r = 0, 0, 0
            for x in range (constants.compress):            #average subblocks
                for y in range (constants.compress):        #average subblocks
                    g += img[i*constants.compress+x][j*constants.compress+y][0]
                    b += img[i*constants.compress+x][j*constants.compress+y][1]
                    r += img[i*constants.compress+x][j*constants.compress+y][2]
            g = g / (constants.compress * constants.compress)
            b = b / (constants.compress * constants.compress)
            r = r / (constants.compress * constants.compress)
            data.append([i, j, g, b, r])
    return data

def assignSubBlocks(subBlocks, blockData):
    newBlocks = []
    numBlocks = len(subBlocks)
    counter = 0
    for subBlock in subBlocks:
        colour = [subBlock[2], subBlock[3], subBlock[4]]
        closestMatch = getClosestColour(blockData, colour)
        newBlocks.append([[int(subBlock[0]), int(subBlock[1])], closestMatch])
        counter += 1
        print("Finding Matching Blocks: {:.1f}% complete ({}/{})".format(100*counter/numBlocks, counter, numBlocks), end='\r', flush=True)
    print("")
    #block = [[img_x, img_y], [atlas_x, atlas_y]]
    return newBlocks

def getClosestColour(blockData, colour):
    #get closest matching block
    closest_distance = math.inf
    for vector in blockData:
        blockColour = vector[0]
        distance = math.sqrt(sum([(colour[i] - blockColour[i]) ** 2 for i in range(3)]))
        if distance < closest_distance:
            closest_distance = distance
            closest_vector = vector[1]
    return closest_vector

def paintSubBlocks(subBlocks, img):
    atlas = cv2.imread("textures/atlas.png")
    size = img.shape
    counter = 0
    numBlocks = len(subBlocks)
    if constants.visual:
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        cv2.setWindowProperty('Image', cv2.WND_PROP_TOPMOST, 1)
    
    for block in subBlocks:
        img = __paintBlock(atlas, block, size, img)
        counter += 1
        print("Painting: {:.1f}% complete ({}/{})".format(100*counter/numBlocks, counter, numBlocks), end='\r', flush=True)
        if constants.visual:
            cv2.imshow("Image", img)
            cv2.waitKey(1)
    print("")
    return img

def __paintBlock(atlas, block, size, img):
    #block = [[img_x, img_y], [atlas_x, atlas_y]]
    i = block[0][0]*constants.compress
    j = block[0][1]*constants.compress
    x = block[1][0]
    y = block[1][1]
    texture = atlas[x:x+16,y:y+16]
    for x in range (constants.compress):
        for y in range (constants.compress):
            if (x < size[0] and y < size[1]):
                img[x + i][y + j] = texture[x][y]
    return img

def __loadImages(subBlocks):
    blockList = [sublist[2] for sublist in subBlocks]
    blockList = set(blockList)
    textureList = {}
    for texture in blockList:
        img = cv2.imread("textures/" + texture)
        if (constants.compress != 16):
            img = img[:16, :16, :]
            img = cv2.resize(img, (constants.compress, constants.compress))
        textureList[texture] = img
    return textureList


