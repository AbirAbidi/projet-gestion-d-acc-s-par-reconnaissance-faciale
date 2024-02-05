import os
import cv2
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, storage
import time

text = "Person"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.0
color = (255, 255, 255)
thickness = 2

# Initialize Firebase
#cred = credentials.Certificate('C:/Users/hp/Downloads/raspberrypi-1ece3-firebase-adminsdk-zsme5-ee2a725f3c.json')
#firebase_admin.initialize_app(cred, {'storageBucket': 'gs://raspberrypi-1ece3.appspot.com'})
#bucket = storage.bucket()


class OpenCamera:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.vid = cv2.VideoCapture(0)  # open webcam
        self.haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        output_folder = 'detected_faces'
        
        time.sleep(5)
        self.capture_image = True

        self.capture_loop()

    def capture_loop(self):
        messagebox.showinfo(title="info", message='When ready click OK to take picture !')

        while True:
            ret, frame = self.vid.read()
            if not ret:
                break

            finalFrame = cv2.flip(frame, 1)
            gray_img = cv2.cvtColor(finalFrame, cv2.COLOR_BGR2GRAY)
            faces_rect = self.haar_cascade.detectMultiScale(gray_img, 1.1, 9)
            output_folder = 'detected_faces'
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            # Get the index of the last saved face image
            existing_images = [filename for filename in os.listdir(output_folder) if filename.startswith('face_')]
            last_index = max([int(filename.split('_')[1].split('.')[0]) for filename in existing_images], default=-1)

            for i, (x, y, w, h) in enumerate(faces_rect):
                #last_index +=1
                face = finalFrame[y:y+h, x:x+w]
                face_filename = os.path.join(output_folder, f'{self.employee_id}.jpg')
                cv2.imwrite(face_filename, face)
                 
                face = cv2.rectangle(finalFrame, (x, y +20), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img=finalFrame,text = text,org=(x,y),fontFace = font, fontScale = font_scale, color = color, thickness = thickness)
                #identify person and push time to database
            self.vid.release()  # Release the webcam
            cv2.destroyAllWindows()  # Close any open windows
            messagebox.showinfo(title="info", message='Image is Taken !')
                #return
            cv2.imshow('frame', finalFrame)

            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
                self.vid.release()
                break

    def upload_image_to_storage(self, image_filename):
        try:
            bucket = storage.bucket()
            blob = bucket.blob(f"avatars/{self.employee_id}.jpg")
            blob.upload_from_filename(image_filename)
            print(f"Image {image_filename} uploaded to storage.")
        except Exception as e:
            print(f"Error uploading image to storage: {e}")


if __name__ == "__main__":
    emp_id = "12345"  # Replace with the actual employee ID
    app = OpenCamera(emp_id)
    cv2.destroyAllWindows() 
