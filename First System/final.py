import cv2
import pytesseract

def draw_rectangle(frame, top_left, bottom_right, color=(0, 255, 0), thickness=2):
    # Gambar kotak pada frame dengan koordinat sudut atas kiri dan sudut bawah kanan yang ditentukan
    cv2.rectangle(frame, top_left, bottom_right, color, thickness)

def recognize_characters(image):
    # Konversi gambar ke grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Lakukan pengenalan karakter menggunakan pytesseract
    recognized_text = pytesseract.image_to_string(gray_image)

    return recognized_text

def main():
    # Buka kamera (ganti 0 dengan indeks kamera yang sesuai jika Anda memiliki beberapa kamera)
    cap = cv2.VideoCapture(1)

    # Periksa apakah kamera terbuka
    if not cap.isOpened():
        print("Tidak dapat membuka kamera.")
        return

    # Tetapkan ukuran jendela tampilan
    cv2.namedWindow('Kamera', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Kamera', 800, 600)

    while True:
        # Baca frame dari kamera
        ret, frame = cap.read()

        if not ret:
            print("Tidak dapat menerima frame.")
            break

        # Tentukan ukuran frame dan posisi rectangle
        height, width, _ = frame.shape
        rectangle_width = 400
        rectangle_height = 150
        top_left = ((width - rectangle_width) // 2, (height - rectangle_height) // 2)
        bottom_right = (top_left[0] + rectangle_width, top_left[1] + rectangle_height)

        # Ambil bagian frame yang berada di dalam rectangle
        plate_area = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # Lakukan pengolahan citra pada bagian pelat (contoh: konversi ke grayscale)
        plate_gray = cv2.cvtColor(plate_area, cv2.COLOR_BGR2GRAY)

        # Contoh: Terapkan deteksi tepi Canny pada bagian pelat
        edges = cv2.Canny(plate_gray, 50, 150)

        # Tempatkan kembali bagian yang telah diolah ke dalam frame utama
        frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = cv2.merge((edges, edges, edges))

        # Gambar rectangle pada frame
        draw_rectangle(frame, top_left, bottom_right)

        # Tampilkan frame pada jendela tampilan
        cv2.imshow('Kamera', frame)

        # Tunggu 1 milidetik dan periksa tombol keyboard
        key = cv2.waitKey(1)

        # Jika tombol 'q' ditekan, keluar dari loop
        if key == ord('q'):
            break

        # Jika tombol 'c' ditekan, tangkap gambar dan lakukan pengenalan karakter
        if key == ord('c'):
            plate_filename = "captured_plate.png"
            cv2.imwrite(plate_filename, plate_area)
            print("Gambar pelat telah ditangkap dan disimpan sebagai", plate_filename)

            # Lakukan pengenalan karakter pada gambar yang telah ditangkap
            recognized_text = recognize_characters(plate_area)
            print("Hasil pengenalan karakter:")
            print(recognized_text)

    # Setelah loop selesai, beberhenti dan tutup jendela tampilan
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()