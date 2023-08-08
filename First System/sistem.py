import cv2
import serial
import time
import mysql.connector
from mysql.connector import Error
import base64
import shutil

# Inisialisasi koneksi serial dengan Arduino
ser = serial.Serial('COM5', 9600)  # Ganti 'COM5' dengan port serial yang sesuai dengan Arduino Anda

# Inisialisasi kamera web
cap = cv2.VideoCapture(1)  # Gunakan nomor 0 jika hanya terhubung satu kamera web

# Koneksi ke database MySQL
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="sistemparkiruper"
        )
        print("Terkoneksi ke Database")
    except Error as e:
        print(f"Koneksi Error '{e}' occurred")

    return connection

# Mengubah gambar menjadi format base64
def encode_image(image_path):
    with open(image_path, "rb") as file:
        image_data = base64.b64encode(file.read())
    return image_data

# Menyimpan gambar ke dalam database
def save_image_to_database(connection, filename, image_data):
    query = "INSERT INTO images (filename, image_data) VALUES (%s, %s)"
    data = (filename, image_data)
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        print("Gambar berhasil disimpan ke Database")
    except Error as e:
        print(f"Error '{e}' occurred")
    
# Menyimpan gambar ke folder publik
def save_image_to_public(filename):
    public_folder = "../../htdocs/sistemParkir/sampel"  # Ganti dengan path ke folder publik yang sesuai
    shutil.move(filename, public_folder)
    print("Gambar berhasil disimpan ke file publik")


# Fungsi untuk menangkap gambar
def capture_image():
    ret, frame = cap.read()  # Membaca frame dari kamera web
    timestamp = int(time.time())  # Mendapatkan timestamp untuk nama file
    filename = f"capture_{timestamp}.png"  # Nama file untuk menyimpan gambar
    cv2.imwrite(filename, frame)  # Menyimpan gambar
    return filename

# Flag untuk menandakan apakah objek sedang terdeteksi
object_detected = False

# Contoh penggunaan
while True:
    # Menerima sinyal dari Arduino melalui koneksi serial
    if ser.in_waiting > 0:
        distance = int(ser.readline().decode().strip())
        
        if distance < 10 and not object_detected:  # Jarak ambang batas untuk mendeteksi objek
            # Menangkap gambar jika objek terdeteksi
            image_file = capture_image()
            print("Obbjek Terdeteksi. Pengambilan gambar objek:", image_file)
            
            # Menghubungkan ke database
            connection = create_connection()
            
            # Encode gambar menjadi format base64
            image_data = encode_image(image_file)
            
            # Menyimpan gambar ke database
            save_image_to_database(connection, image_file, image_data)
            
            
            # Menyimpan gambar ke folder publik
            save_image_to_public(image_file)

            # Tutup koneksi database
            connection.close()
            
            object_detected = True
            
            time.sleep(5)
        else:
            object_detected = False
    
    # Tampilkan frame kamera web
    ret, frame = cap.read()
    cv2.imshow("Frame Kamera", frame)
    
    # Mematikan tangkapan gambar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup koneksi serial dan kamera web
ser.close()
cap.release()
cv2.destroyAllWindows()