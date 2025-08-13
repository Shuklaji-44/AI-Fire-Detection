
import cv2
import threading
import playsound
import smtplib
import tkinter as tk
from tkinter import Label, ttk
from PIL import Image, ImageTk
import datetime

fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml')
# "0" for laptop camera and "1" for USB attahed camera
vid = cv2.VideoCapture(0)
# vid = cv2.VideoCapture("videos\\fire2.mp4")
runOnce = False
alarm_status = False
fire_count = 0 


def log_fire_event(event_type, count):
    with open("fire_log.txt", "a") as logfile:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logfile.write(f"[{timestamp}] Event: {event_type}, Fire Count: {count}\n")

root = tk.Tk()
root.title("🔥 AI-Powered Fire Detection System")
root.geometry("1100x750")
root.configure(bg="#1e1e2e")

style = ttk.Style()
style.theme_use("clam")
style.configure("Start.TButton", font=("Arial", 14, "bold"), padding=10, background="#28a745", foreground="white")
style.map("Start.TButton", background=[("active", "#218838")])
style.configure("Stop.TButton", font=("Arial", 14, "bold"), padding=10, background="#dc3545", foreground="white")
style.map("Stop.TButton", background=[("active", "#c82333")])

header_label = Label(root, text="🚨 AI-Based Fire Detection System 🚨", font=("Arial", 28, "bold"), fg="orange", bg="#1e1e2e")
header_label.pack(pady=20)

frame_container = tk.Frame(root, bg="#1e1e2e")
frame_container.pack()
frame_label = Label(frame_container, bg="#1e1e2e")
frame_label.pack()

status_label = Label(root, text="Status: 🔍 Scanning...", font=("Arial", 18, "bold"), fg="white", bg="#1e1e2e")
status_label.pack(pady=10)

fire_count_label = Label(root, text="🔥 Fire Count: 0", font=("Arial", 16, "bold"), fg="lightgreen", bg="#1e1e2e")
fire_count_label.pack(pady=5)

def play_alarm_sound_function():
    playsound.playsound('fire_alarm.mp3', True)
    print("Fire alarm stopped")

def send_mail_function(): 
    recipientmail = "66shankar27@gmail.com"
    recipientmail = recipientmail.lower()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("66shankar27@gmail.com", 'gfjd vcpr dyix phxg') 
        server.sendmail('66shankar27@gmail.com', recipientmail,
                        "We regret to inform you that a fire accident has been detected in the monitored area. Immediate action is required to prevent further damage and ensure safety.")
        print("Alert mail sent successfully to {}".format(recipientmail))
        server.close()
    except Exception as e:
        print(e)

def detect_fire():
    global runOnce, alarm_status, fire_count
    ret, frame = vid.read()
    if not ret:
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    if len(fire) > 0:
        fire_count += 1  
        fire_count_label.config(text=f"🔥 Fire Count: {fire_count}")
        log_fire_event("Fire Detected", fire_count)

    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 3)
        print("🔥 Fire Detected!")
        status_label.config(text="🚨 FIRE ALERT! FIRE DETECTED! 🚨", fg="red")

        if not alarm_status:
            threading.Thread(target=play_alarm_sound_function).start()
            alarm_status = True
        if not runOnce:
            threading.Thread(target=send_mail_function).start()
            runOnce = True

    if len(fire) == 0:
        status_label.config(text="✅ Status: No Fire Detected", fg="green")

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)
    frame_label.img = img
    frame_label.config(image=img)
    frame_label.after(10, detect_fire)

def start_detection():
    status_label.config(text="Status: 🔍 Scanning for Fire...", fg="yellow")
    detect_fire()

def stop_detection():
    vid.release()
    cv2.destroyAllWindows()
    root.quit()

button_frame = tk.Frame(root, bg="#1e1e2e")
button_frame.pack(pady=30)

start_btn = ttk.Button(button_frame, text="▶ Start Detection", command=start_detection, style="Start.TButton")
start_btn.grid(row=0, column=0, padx=20)

stop_btn = ttk.Button(button_frame, text="⏹ Stop Detection", command=stop_detection, style="Stop.TButton")
stop_btn.grid(row=0, column=1, padx=20)

footer_label = Label(root, text="🧠 Powered by AI | Stay Safe 🔥", font=("Arial", 14, "bold"), fg="orange", bg="#1e1e2e")
footer_label.pack(pady=10)

root.mainloop()

