import cv2
import mysql.connector
from mysql.connector import errorcode
from time import sleep
import serial

# Obtain connection string information from the portal
config = {
  'host':'127.0.0.1',
  'user':'root',
  'password':'',
  'database':'sistemparkir'
}

try:
   conn = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

cur = conn.cursor()
cur.execute("CREATE TABLE if not exists sistemparkir (img BLOB);")
cam = cv2.VideoCapture(1)

# Check if the webcam is opened correctly
if not cam.isOpened():
    raise IOError("Cannot open webcam")

frame = cam.read()[1]
cur.execute("INSERT INTO sistemparkir (img) VALUES %s",frame)
cam.release()