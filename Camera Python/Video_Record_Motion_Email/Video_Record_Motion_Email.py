from imutils.video import VideoStream
import argparse
import datetime
from time import time
import imutils
import time
import cv2
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

cap = cv2.VideoCapture(0)
img_counter = 0
vid_counter=0
previous= time.time()
delta=0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
vidname= "output{}".format(vid_counter)
out = cv2.VideoWriter('{}.avi'.format(vidname),fourcc, 150.0, (640,480))

email_user = 'PUT YOUR EMAIL"
email_password = 'PUT THE PASSWORD'
email_send = 'send to @'

subject = 'Motion detected!'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['Subject'] = subject

body = 'Hi there, these pictures are taken at your home!'
msg.attach(MIMEText(body,'plain'))


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
vs = VideoStream(src=0).start()

# otherwise, we are reading from a video file
else:
vs = cv2.VideoCapture(args["video"])

firstFrame = None

# loop over the frames of the video
while True:

  current=time.time()
  delta+=current-previous
  previous= current
  frame = vs.read()
  frame = frame if args.get("video", None) is None else frame[1]
  text = "Unoccupied"
  datet=str(datetime.datetime.now())
  font=cv2.FONT_HERSHEY_SIMPLEX

  if frame is None:
    break

  # resize the frame, convert it to grayscale, and blur it
  frame = imutils.resize(frame, width=500)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (21, 21), 0)

  # if the first frame is None, initialize it
  if firstFrame is None:
    firstFrame = gray
    continue

  # compute the absolute difference between the current frame and
  frameDelta = cv2.absdiff(firstFrame, gray)
  thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY)[1]

  # dilate the thresholded image to fill in holes, then find contours on thresholded image
  thresh = cv2.dilate(thresh, None, iterations=2)
  cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
  cnts = imutils.grab_contours(cnts)

  # loop over the contours
  for c in cnts:
    # if the contour is too small, ignore it
    if cv2.contourArea(c) < args["min_area"]:
      continue

    # compute the bounding box for the contour, draw it on the frame, and update the text
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    text = "Motion Detected! Record.."
    frame=vs.read()
    frame=cv2.putText(frame,datet,(10, 50),font,1,(0,255,255),2, cv2.LINE_AA)
    out.write(frame)
    if delta> 10:
            delta=0
            img_name = "opencv_frame_{}.png".format(img_counter)
            frame=cv2.putText(frame,datet,(10, 50),font,1,(0,255,255),2, cv2.LINE_AA)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            #space saves an image
            filename=img_name
            attachment=open(filename,'rb')
            part = MIMEBase('application','octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',"attachment; filename= "+filename)
            msg.attach(part)
            print(" \n Sent!")
            img_counter += 1
            

  cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
  cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

  cv2.imshow("Security Feed", frame)
  cv2.imshow("Thresh", thresh)
  cv2.imshow("Frame Delta", frameDelta)
  key = cv2.waitKey(1) & 0xFF

  if key%256 == 27:   #ESC stops the program
    break
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,email_password)
text = msg.as_string()
server.sendmail(email_user,email_send,text)

vs.stop() if args.get("video", None) is None else vs.release()
out.release()
cv2.destroyAllWindows()
server.quit()
