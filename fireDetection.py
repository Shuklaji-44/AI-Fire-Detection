import cv2         
import threading   
import playsound   
import smtplib     


fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml')
# "0" for laptop camera and "1" for USB attahed camera
# vid = cv2.VideoCapture(0)
vid = cv2.VideoCapture("videos\\fire2.mp4")
runOnce = False
alarm_status = False
fire_count = 0 



def play_alarm_sound_function(): 

    playsound.playsound('fire_alarm.mp3',True) 
    print("Fire alarm end") 


def send_mail_function(): 
    
    recipientmail = "66shankar27@gmail.com" 
    recipientmail = recipientmail.lower() 
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("66shankar27@gmail.com", 'gfjd vcpr dyix phxg') 
        server.sendmail('66shankar27@gmail.com', recipientmail, "Warning fire accident has been reported") 
        print("Alert mail sent sucesfully to {}".format(recipientmail))
        server.close()
        
    except Exception as e:
        print(e) 
		
while(True):
    Alarm_Status = False
    ret, frame = vid.read() 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) 

    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()  

        if runOnce == False:
            print("Mail send initiated")
            threading.Thread(target=send_mail_function).start() 
            runOnce = True
        if runOnce == True:
            print("Mail is already sent once")
            runOnce = True

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
