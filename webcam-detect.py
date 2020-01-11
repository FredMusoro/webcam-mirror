import cv2, sys

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)
img_counter = 0
padding = 20

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
genderList = ['Male', 'Female']
ageList = ['(0 - 2)', '(4 - 6)', '(8 - 12)', '(15 - 20)', '(25 - 32)', '(38 - 43)', '(48 - 53)', '(60 - 100)']

ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"

genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"

showEdge = 1
while (video_capture.isOpened()):

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    k = cv2.waitKeyEx(1)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=7,
        minSize=(30, 30)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:

        face = frame[y:y+h, x:x+w]

        ageNet = cv2.dnn.readNet(ageModel, ageProto)
        genderNet = cv2.dnn.readNet(genderModel, genderProto)

        blob = cv2.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        # print("Gender Output : {}".format(genderPreds))
        # print("Gender : {}".format(gender))

        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        # print("Age Output : {}".format(agePreds))
        # print("Age : {}".format(age))


        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(grayscale, 75, 125)


        if showEdge:

            cv2.rectangle(edge, (x, y), (x+w, y+h), (255, 64, 64), 2)
            cv2.putText(edge, "Location: 11201",(x+w+30, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,64,64),2, cv2.LINE_AA)
            cv2.putText(edge, "Most Likely 311 Complaint: Sidewalk",(x+w+30, int(y + h*0.25)),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,64,64),2, cv2.LINE_AA)
            cv2.putText(edge, "Voter Status: Not Registered in New York",(x+w+30, int(y + h*0.5)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,64,64),2, cv2.LINE_AA)
            cv2.putText(edge, "Tax Bracket: ?",(x+w+30, int(y + h*0.75)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,64,64),2, cv2.LINE_AA)

            # Display the resulting frame
            cv2.imshow('FaceDetection', edge)

        else:
            cv2.rectangle(grayscale, (x, y), (x+w, y+h), (255, 64, 64), 2)
            cv2.putText(grayscale, "Gender Prediction:" + str(gender),(x-w, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,155,255),2, cv2.LINE_AA)
            cv2.putText(grayscale, "Age Estimation:" + str(age),(x-w, int(y + h*0.5)),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,155,255),2, cv2.LINE_AA)

            cv2.putText(grayscale, "Friend Peer Group: Starting Adult Life",(x+w+30, int(y + h*0.25)),cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,155,255),2, cv2.LINE_AA)
            cv2.putText(grayscale, "Ad Interests: Espresso machine",(x+w+30, int(y + h*0.5)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,155,255),2, cv2.LINE_AA)
            cv2.putText(grayscale, "Clicked Ads: PubPass",(x+w+30, int(y + h*0.75)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,155,255),2, cv2.LINE_AA)

            # Display the resulting frame
            cv2.imshow('FaceDetection', grayscale)

    #ESC Pressed
    if k== 27:
        break
    #SPACE pressed
    elif k== 32:
        img_name = "facedetect_webcam_{}.png".format(img_counter)
        cv2.imwrite(img_name, edge)
        print("{} written!".format(img_name))
        img_counter += 1


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()