import cv2, parrallel, constants, threading
from os import system

#thread for processing a small chunk of a video
def videoThread(startFrame, numFrames, blockData, video, videoWriter, writerLock, videoLock):
    print("Starting thread " + str(startFrame))
    for j in range(numFrames):
        with videoLock:
            print("Setting frame " + str(startFrame + j))
            video.set(cv2.CAP_PROP_POS_FRAMES, startFrame+j)
            gotFrame, frame = video.read()
            if not gotFrame:
                print("Error reading next frame. Video may have ended. Frame: " + str(startFrame + j))
        print("Working on frame " + str(startFrame + j))
        frame = processImage(frame, blockData)
        with writerLock:
            videoWriter.write(frame)
    print("Video thread starting at " + str(startFrame) + " finished")

def convertVideo(video, blockData):
    numFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    videoWriter = cv2.VideoWriter('../output' + constants.input_name.split('.')[0] + '_processed.mp4', cv2.VideoWriter_fourcc(*'mp4v'), video.get(cv2.CAP_PROP_FPS), (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    for i in range(numFrames):
        system('cls')
        print("Video Processing: {:.1f}% complete (Frame {}/{})".format(100*i/numFrames, i, int(numFrames)), flush=True)
        gotFrame, frame = video.read()
        if not gotFrame:
            print("Error reading next frame. Video may have ended. Frame: " + i)
        frame = processImage(frame, blockData)
        videoWriter.write(frame)
    video.release()
    videoWriter.release()

def processImage(img, blockData):
    width, height, channels = img.shape
    #combine all pixels into an array of colour values to be converted to an image
    print("Building subblocks")
    subBlocks = parrallel.getSubBlocks(img, width, height)
    print("Done building subblocks\n")

    #find the closest minecraft block
    newBlocks = parrallel.assignSubBlocks(subBlocks, blockData)
    print("Done Finding Matching Blocks\n")

    #place that block at this pixels location
    img = parrallel.paintSubBlocks(newBlocks, img)
    print("Done Painting")
    return img

def convertVideoThreaded(video, blockData):
    numFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    videoWriter = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), video.get(cv2.CAP_PROP_FPS), (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    numThreads = int(numFrames/constants.max_frames_per_thread)
    writerLock = threading.Lock()
    videoLock = threading.Lock()

    threads = []
    for i in range(numThreads):
        args = (i*constants.max_frames_per_thread, constants.max_frames_per_thread, blockData, video, videoWriter, writerLock, videoLock)
        t = threading.Thread(target=videoThread, args=args)
        threads.append(t)
    
    videoWriter.release()

    for t in threads:
        t.start()
    
    #video.release()

def finishImage(img):
    #display image
    saving = True
    if constants.show_at_end:
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        save = input("Save? (y/n): ")
        if (save == "n" or save == "N" or save == "no"):
            saving = False

    if (saving):
        filename = '../output/' + constants.input_name.split('.')[0] + "_processed.png"
        cv2.imwrite(filename, img)
        print("Saved " + filename)