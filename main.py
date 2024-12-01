# pip install opencv-python
# pip install mediapipe
# pip install pyserial

import cv2
import mediapipe as mp
import serial
import time
import sys

# ตั้งค่าการใช้งาน MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# เชื่อมต่อกับ ESP32 ผ่าน Serial (เปลี่ยน 'COM3' ตามพอร์ตของ ESP32)
ser = serial.Serial('COM5', 115200)  # พอร์ตที่เชื่อมต่อ ESP32
time.sleep(2)  # รอการเชื่อมต่อ Serial

# เริ่มต้นการใช้งาน hands model
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# เปิดกล้อง
cap = cv2.VideoCapture(0)

# กำหนดชุดของจุดเชื่อมต่อนิ้วที่ต้องการแสดง (4 นิ้ว, ไม่รวม นิ้วโป้ง)
connections = [
    # นิ้วชี้
    (5, 6), (6, 7), (7, 8),
    # นิ้วกลาง
    (9, 10), (10, 11), (11, 12),
    # นิ้วนาง
    (13, 14), (14, 15), (15, 16),
    # นิ้วก้อย
    (17, 18), (18, 19), (19, 20)
]

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # แปลงภาพเป็น RGB เพราะ MediaPipe ใช้ RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # หากพบการตรวจจับมือ
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # วาดการเชื่อมต่อนิ้ว 4 นิ้ว (ไม่รวมการเชื่อมต่อนิ้วโป้ง)
                for connection in connections:
                    start_idx, end_idx = connection
                    start = hand_landmarks.landmark[start_idx]
                    end = hand_landmarks.landmark[end_idx]
                    # วาดเส้นเชื่อมต่อ
                    cv2.line(frame, 
                             (int(start.x * frame.shape[1]), int(start.y * frame.shape[0])), 
                             (int(end.x * frame.shape[1]), int(end.y * frame.shape[0])), 
                             (0, 255, 0), 2)

                # ตรวจสอบนิ้วที่ชู (นิ้วชี้, นิ้วกลาง, นิ้วนาง, นิ้วก้อย)
                fingers_raised = 0
                
                # นิ้วชี้
                tip_index = hand_landmarks.landmark[8]
                base_index = hand_landmarks.landmark[6]
                if tip_index.y < base_index.y:
                    fingers_raised += 1

                # นิ้วกลาง
                tip_middle = hand_landmarks.landmark[12]
                base_middle = hand_landmarks.landmark[10]
                if tip_middle.y < base_middle.y:
                    fingers_raised += 1

                # นิ้วนาง
                tip_ring = hand_landmarks.landmark[16]
                base_ring = hand_landmarks.landmark[14]
                if tip_ring.y < base_ring.y:
                    fingers_raised += 1

                # นิ้วก้อย
                tip_pinky = hand_landmarks.landmark[20]
                base_pinky = hand_landmarks.landmark[18]
                if tip_pinky.y < base_pinky.y:
                    fingers_raised += 1

                # แสดงจำนวนของนิ้วที่ชู
                cv2.putText(frame, f"Fingers Raised: {fingers_raised}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # ส่งคำสั่งควบคุมรีเลย์
                if fingers_raised == 1:
                    ser.write(b'1')  # เปิดรีเลย์ตัวที่ 1
                elif fingers_raised == 2:
                    ser.write(b'2')  # เปิดรีเลย์ตัวที่ 2
                elif fingers_raised == 3:
                    ser.write(b'3')  # เปิดรีเลย์ตัวที่ 3
                elif fingers_raised == 4:
                    ser.write(b'4')  # เปิดรีเลย์ตัวที่ 4
                else:
                    ser.write(b'0')
        # แสดงผลลัพธ์
        cv2.imshow("Hand Gesture Detection", frame)

        # กด 'q' เพื่อออกจากโปรแกรม
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("โปรแกรมถูกหยุดด้วยตนเอง")

finally:
    # ปิดการเชื่อมต่อ Serial
    ser.write(b'0')  # ส่งคำสั่งหยุดการทำงานให้ ESP32
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
    print("โปรแกรมเสร็จสมบูรณ์และปิดการเชื่อมต่อกับ ESP32")
