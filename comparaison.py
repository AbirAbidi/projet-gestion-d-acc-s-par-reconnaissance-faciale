import cv2
import face_recognition
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import time 
from firebase_admin import credentials, firestore, initialize_app
from add_employee import AddEmployeeApp
from add_visitor import AddVisitor

cred = credentials.Certificate('C:/Users/hp/Downloads/raspberrypi-1ece3-firebase-adminsdk-zsme5-ee2a725f3c.json')
#firebase_app = initialize_app(cred)

class Comparaison:
    def __init__(self, db):
        self.db = db
        self.vid = cv2.VideoCapture(0)  # open webcam
        self.detected_faces_path = 'detected_faces'
        self.known_face_encodings, self.known_face_labels = self.load_detected_faces()

        self.visitor_answer = None  # Variable to store the visitor's answer
        self.root = None  # Variable to store the Tkinter root window

        while True:
            ret, frame = self.vid.read()
            if not ret:
                break

            finalFrame = cv2.flip(frame, 1)
            gray_img = cv2.cvtColor(finalFrame, cv2.COLOR_BGR2GRAY)

            face_locations = face_recognition.face_locations(finalFrame)
            face_encodings = face_recognition.face_encodings(finalFrame, face_locations)

            if not face_locations:
                # No faces detected
                cv2.putText(finalFrame, "No faces detected.", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            else:
                recognized = False

                for i, (top, right, bottom, left) in enumerate(face_locations):
                    cv2.rectangle(finalFrame, (left, top), (right, bottom), (0, 255, 0), 2)

                    # Perform face recognition
                    distances = face_recognition.face_distance(self.known_face_encodings, face_encodings[i])
                    min_distance = min(distances)
                    threshold = 0.6  # Set your threshold value

                    if min_distance <= threshold:
                        index = distances.argmin()
                        name = f"Person ID: {self.known_face_labels[index]}"
                        cv2.putText(finalFrame, f"Success! {name} recognized.", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        recognized = True
                    else:
                        cv2.putText(finalFrame, "Error! Person not recognized.", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                if not recognized and self.visitor_answer is None:
                    # Wait for 1 second before prompting for visitor status
                    time.sleep(1)
                    # Prompt for visitor status
                    self.visitor_answer = self.ask_yes_no_question("Are you a visitor?")
                    if self.visitor_answer:
                        print('hey')
                        #AddVisitor(db)

            cv2.imshow('Comparaison', finalFrame)

            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Comparaison', cv2.WND_PROP_VISIBLE) < 1:
                self.vid.release()  # Release the camera before closing the application
                break

        cv2.destroyAllWindows()

    def load_detected_faces(self):
        known_face_encodings = []
        known_face_labels = []

        for file_name in os.listdir(self.detected_faces_path):
            path = os.path.join(self.detected_faces_path, file_name)
            label = file_name.split('.')[0]  # Extract the person ID from the file name
            image = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_labels.append(label)

        return known_face_encodings, known_face_labels

    def ask_yes_no_question(self, question):
        self.root = tk.Tk()
        self.root.withdraw()
        answer = messagebox.askyesno("Question", question)
        return answer

if __name__ == "__main__":
    db = firestore.client()
    Comparaison(db)
