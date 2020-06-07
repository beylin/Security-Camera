import cv2
from twilio.rest import Client
account = input("account: ")
token = input("token: ")
from_ = input('from_: ')
to = input('to: ')
client = Client(account, token)
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('security.avi', fourcc, 60.0, (1280, 720))
frame1 = cap.read()[1]
frame2 = cap.read()[1]
counter = 0
while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)[1]
    dilated = cv2.dilate(thresh, None, iterations=3)
    image, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 900:
            pass
        else:
            counter += 1
            if counter == 1:
                message = client.messages.create(from_=from_, to=to, body='Alert!')
                print(message)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,
                        cv2.LINE_AA)
    cv2.imshow("feed", frame1)
    out.write(frame1)
    frame1 = frame2
    frame2 = cap.read()[1]
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
