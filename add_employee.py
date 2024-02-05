from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
from openCamera import OpenCamera
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('C:/Users/hp/Downloads/raspberrypi-1ece3-firebase-adminsdk-zsme5-ee2a725f3c.json')
#firebase_admin.initialize_app(cred)
#db = firestore.client()

class AddEmployeeApp:   
    def __init__(self,db):
        self.db = db
        self.window = Tk()
        self.window.title('Add Employee')
        self.window.geometry("600x600+700+50")
        #p1 = PhotoImage(file='face-recognition.png')
        #self.window.iconphoto(False, p1)
        self.visible = False

        self.setup_gui()

    def setup_gui(self):
        self.addEmployeeText = Label(self.window, text="Add Employee", fg='blue')

        self.firstNameText = Label(self.window, text="1st name", fg='blue')
        self.firstNameInput = Entry(self.window, bd=1, width=30)
        self.lastNameText = Label(self.window, text="Last name", fg='blue')
        self.lastNameInput = Entry(self.window, bd=1, width=30)

        self.dateText = Label(self.window, text="Date of integration", fg='blue')
        self.dateInput = DateEntry(self.window, selectmode='day')

        self.okButton = Button(text="NEXT", bg='blue', fg='white', command=self.open_camera)

        self.window.bind("<Configure>", lambda event: self.center_widgets())  # Recenter widgets on window resize

        self.firstNameText.pack()
        self.firstNameInput.pack()
        self.lastNameText.pack()
        self.lastNameInput.pack()
        self.dateText.pack()
        self.dateInput.pack()
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
        self.dateText.place(x=window_width/2, y=window_height/2 + 80, anchor='center')
        self.dateInput.place(x=window_width/2, y=window_height/2 + 120, anchor='center')
        self.okButton.place(x=window_width/2, y=window_height/2 + 170, anchor='center')

    def open_camera(self):
        first_name = self.firstNameInput.get()
        last_name = self.lastNameInput.get()
        date_of_integration = self.dateInput.get()
        if first_name == "" or last_name == "" or date_of_integration == "":
            messagebox.showerror(title='error', message='A field is empty!')
        else:
            # Push data to Firebase
            employee_data = {
                'first_name': first_name,
                'last_name': last_name,
                'date_of_integration': date_of_integration,
            }
            doc_ref, doc_id = self.db.collection('employee').add(employee_data)
            #doc_id = doc_ref.id 
            self.window.destroy()
            OpenCamera(str(doc_id.id))

if __name__ == "__main__":
    #root = Tk()
    db = firestore.client()
    app = AddEmployeeApp(db)
    #root.mainloop()
