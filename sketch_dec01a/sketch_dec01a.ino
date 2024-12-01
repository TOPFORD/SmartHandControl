const int relay1Pin = 4;   // รีเลย์ตัวที่ 1 (GPIO 4)
const int relay2Pin = 23;  // รีเลย์ตัวที่ 2 (GPIO 23)
const int relay3Pin = 27;  // รีเลย์ตัวที่ 3 (GPIO 27)
const int relay4Pin = 13;  // รีเลย์ตัวที่ 4 (GPIO 13)

void setup() {
  Serial.begin(115200);  // เริ่มต้น Serial communication ที่ baud rate 115200
  pinMode(relay1Pin, OUTPUT);  // กำหนด GPIO สำหรับรีเลย์
  pinMode(relay2Pin, OUTPUT);
  pinMode(relay3Pin, OUTPUT);
  pinMode(relay4Pin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // อ่านคำสั่งจาก Serial

    // ตรวจสอบคำสั่งเพื่อเปิดหรือปิดรีเลย์ตามจำนวนของนิ้วที่ชู
    if (command == '1') {
      digitalWrite(relay1Pin, LOW);  // เปิดรีเลย์ตัวที่ 1
      digitalWrite(relay2Pin, HIGH);
      digitalWrite(relay3Pin, HIGH);
      digitalWrite(relay4Pin, HIGH);
    } else if (command == '2') {
      digitalWrite(relay2Pin, LOW);  // เปิดรีเลย์ตัวที่ 2
      digitalWrite(relay1Pin, HIGH);
      digitalWrite(relay3Pin, HIGH);
      digitalWrite(relay4Pin, HIGH);
    } else if (command == '3') {
      digitalWrite(relay3Pin, LOW);  // เปิดรีเลย์ตัวที่ 3
      digitalWrite(relay1Pin, HIGH);
      digitalWrite(relay2Pin, HIGH);
      digitalWrite(relay4Pin, HIGH);
    } else if (command == '4') {
      digitalWrite(relay4Pin, LOW);  // เปิดรีเลย์ตัวที่ 4
      digitalWrite(relay1Pin, HIGH);
      digitalWrite(relay2Pin, HIGH);
      digitalWrite(relay3Pin, HIGH);
    } else {
      digitalWrite(relay4Pin, HIGH);  // เปิดรีเลย์ตัวที่ 4
      digitalWrite(relay1Pin, HIGH);
      digitalWrite(relay2Pin, HIGH);
      digitalWrite(relay3Pin, HIGH);
      }
  }
}
