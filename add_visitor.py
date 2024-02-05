import datetime
from tkinter import *
from tkinter import messagebox
import cv2
from tkcalendar import DateEntry
from openCamera import OpenCamera
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('C:/Users/hp/Downloads/raspberrypi-1ece3-firebase-adminsdk-zsme5-ee2a725f3c.json')
firebase_admin.initialize_app(cred)
#db = firestore.client()

class AddVisitor:   
    def __init__(self,db):
        #cv2.destroyAllWindows()
        print("passed")
        self.db = db
        self.window = Tk()
        self.window.title('Add Visitor')
        self.window.geometry("600x600+700+50")
        #img_path = "C:/Users/hp/Desktop/face recognition/face-recognition.png"
        #p1 = PhotoImage(file=img_path)
        #self.window.iconphoto(False, p1)
        self.visible = False

        self.setup_gui()
        self.window.mainloop()
    def setup_gui(self):
        self.addEmployeeText = Label(self.window, text="Add Visitor", fg='blue')

        self.firstNameText = Label(self.window, text="1st name", fg='blue')
        self.firstNameInput = Entry(self.window, bd=1, width=30)
        self.lastNameText = Label(self.window, text="Last name", fg='blue')
        self.lastNameInput = Entry(self.window, bd=1, width=30)
        self.reasonText = Label(self.window, text="Reason of visit", fg='blue')
        self.reason = Entry(self.window,  bd=1, width=30)

        self.okButton = Button(text="NEXT", bg='blue', fg='white', command=self.pushTodb)

        self.window.bind("<Configure>", lambda event: self.center_widgets())  # Recenter widgets on window resize

        self.firstNameText.pack()
        self.firstNameInput.pack()
        self.lastNameText.pack()
        self.lastNameInput.pack()
        self.reasonText.pack()
        self.reason.pack()
        self.okButton.pack()

    def center_widgets(self):
        self.window.update_idletasks()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        self.addEmployeeText.place(x=window_width/2, y=window_height/2 - 150, anchor=CENTER)
        
        self.firstNameText.place(x=window_width/2, y=window_height/2 - 100, anchor='center')
        self.firstNameInput.place(x=window_width/2, y=window_height/2 - 60, anchor='center')
        
        self.lastNameText.place(x=window_width/2, y=window_height/2 - 10, anchor='center')
        self.lastNameInput.place(x=window_width/2, y=window_height/2 + 30, anchor='center')
        
        self.reasonText.place(x=window_width/2, y=window_height/2 + 80, anchor='center')
        self.reason.place(x=window_width/2, y=window_height/2 + 120, anchor='center')
        
        self.okButton.place(x=window_width/2, y=window_height/2 + 170, anchor='center')

    def pushTodb(self):
        first_name = self.firstNameInput.get()
        last_name = self.lastNameInput.get()
        reason_of_visit = self.reason.get()
        if first_name == "" or last_name == "" or reason_of_visit == "":
            messagebox.showerror(title='error', message='A field is empty!')
        else:
            # Push data to Firebase
            visitor_data = {
                'first_name': first_name,
                'last_name': last_name,
                'reason_of_visit': reason_of_visit,
                'date_of_visit':datetime.datetime.now()
            }
            doc_ref, doc_id = self.db.collection('visitor').add(visitor_data)
            #doc_id = doc_ref.id 
            self.window.destroy()
            
            #OpenCamera(str(doc_id.id))
db = firestore.client()
AddVisitor(db)
#if __name__ == "__main__":
    #root = Tk()
    #db = firestore.client()
    #app = AddVisitor(db)
    #root.mainloop()
