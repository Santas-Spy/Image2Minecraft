input_name = ""
compress = 16
max_frames_per_thread = 10
reject_transparent = True
show_rejected = False
show_at_end = False
visual = False

def setConstants():
    getImage()

    print("Are you ok with the default settings?")
    print("\tcompress = 16")
    print("\tvisual = False")
    print("\treject_transparent = True")
    print("\tshow_rejected = False")
    print("\tshow_at_end = False")
    useDefault = input("(y/n): ")
    if (useDefault == "n" or useDefault == "N" or useDefault == "no"):
        setCompress()
        setVisual()
        setReject()
        setShowReject()
        setShowEnd()
        print("")
        
def getImage():
    global input_name
    gotVal = False
    while (gotVal == False):
        input_name = input("Filename: ")
        extension = input_name.split('.')[1]
        if (extension == "png" or extension == "mp4"):
            try:
                open(input_name)
                gotVal = True
            except FileNotFoundError:
                print("That file did not exist. Please check the file name and try again")
        else:
            print("File format not accepted")

def setCompress():
    global compress
    gotVal = False
    while (gotVal == False):
        compressVal = input("\tcompress = ")
        try:
            compressVal = int(compressVal)
            if (compressVal > 0):
                compress = compressVal
                gotVal = True
            else:
                print("Compress must be greater than zero") 
            break
        except ValueError:
            print("Compress must be an int")

def setVisual():
    global visual
    gotVal = False
    while (gotVal == False):
        visual = input("\tvisual (t/f) = ")
        if (visual == "t" or visual == "T" or visual == "true"):
            visual = True
            gotVal = True
        elif (visual == "f" or visual == "F" or visual == "false"):
            visual = False
            gotVal = True
        else:
            print("Visual must be either true or false (t/f)")

def setReject():
    global reject_transparent
    gotVal = False
    while (gotVal == False):
        reject = input("\treject_transparent (t/f) = ")
        if (reject == "t" or reject == "T" or reject == "true"):
            reject_transparent = True
            gotVal = True
        elif (reject == "f" or reject == "F" or reject == "false"):
            reject_transparent = False
            gotVal = True
        else:
            print("Reject transparent must be either true or false (t/f)")

def setShowReject():
    global show_rejected
    gotVal = False
    while (gotVal == False):
        showReject = input("\tshow_rejected (t/f) = ")
        if (showReject == "t" or showReject == "T" or showReject == "true"):
            show_rejected = True
            gotVal = True
        elif (showReject == "f" or showReject == "F" or showReject == "false"):
            show_rejected = False
            gotVal = True
        else:
            print("Show rejected must be either true or false (t/f)")

def setShowEnd():
    global show_at_end
    gotVal = False
    while (gotVal == False):
        showReject = input("\tshow_at_end (t/f) = ")
        if (showReject == "t" or showReject == "T" or showReject == "true"):
            show_at_end = True
            gotVal = True
        elif (showReject == "f" or showReject == "F" or showReject == "false"):
            show_at_end = False
            gotVal = True
        else:
            print("Show at end must be either true or false (t/f)")

            