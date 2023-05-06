import cv2
import blockencoding
import constants
import mediaProcessor

#load constants
constants.setConstants()

#load the image
print("Scanning Minecraft Blocks")
blockData = blockencoding.readAtlas()
print("Done Scanning Minecraft Blocks\n")

if (constants.input_name.split('.')[1] == "png"):
    img = cv2.imread(constants.input_name)
    img = mediaProcessor.processImage(img, blockData)
    print("Done!")
    mediaProcessor.finishImage(img)
elif (constants.input_name.split('.')[1] == "mp4"):
    img = cv2.VideoCapture(constants.input_name)
    img = mediaProcessor.convertVideo(img, blockData)
    print("Done!")
else:
    print("File format not accepted")

print("Goodbye")
