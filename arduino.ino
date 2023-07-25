#define trigPin 2
#define echoPin 3
#define ledPinRed 4
#define ledPinGreen 5

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPinRed, OUTPUT);
  pinMode(ledPinGreen, OUTPUT);
}

void loop() {
  long duration, distance;
  
  // Mengirim sinyal ultrasonik
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Menerima echo dan menghitung jarak
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  
  // Mengirim jarak ke komputer melalui koneksi serial
  Serial.println(distance);
  
  // Mengendalikan LED berdasarkan deteksi objek
  if (distance < 10) {  // Jarak ambang batas untuk mendeteksi objek
    digitalWrite(ledPinRed, LOW);  // LED merah menyala
    digitalWrite(ledPinGreen, HIGH);  // LED hijau mati
  } else {
    digitalWrite(ledPinRed, HIGH);  // LED merah mati
    digitalWrite(ledPinGreen, LOW);  // LED hijau menyala
  }
  
  delay(1000);  // Delay sebelum pengukuran berikutnya
}
