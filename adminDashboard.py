from tkinter import *
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from add_employee import AddEmployeeApp

class AdminLoginApp:
    def __init__(self,db):
        self.db = db
        if not firebase_admin._apps:
        # Initialize Firebase
            cred = credentials.Certificate('C:/Users/hp/Downloads/raspberrypi-1ece3-firebase-adminsdk-zsme5-ee2a725f3c.json')
            firebase_admin.initialize_app(cred)

        self.visible = False

        self.window = Tk()
        self.window.title('Smart attendance system')
        self.p1 = PhotoImage(file='face-recognition.png')
        self.window.iconphoto(False, self.p1)
        self.window.geometry("600x600+700+50")
        

        # Title
        self.login = Label(self.window, text="Administration Login", fg='blue')
        # ID label and entry
        self.identifier = Label(self.window, text="ID", fg='blue')
        self.identifier.pack()
        self.txtfld1 = Entry(self.window, bd=1, width=30)
        self.txtfld1.pack()

        self.window.bind("<Configure>", lambda event: self.center_widgets())  # Recenter widgets on window resize

        # Password label, entry, and toggle button
        self.mp = Label(self.window, text="Password", fg='blue')
        self.mp.pack()
        self.txtfld2 = Entry(self.window, bd=1, show='*', width=30)
        self.txtfld2.pack()

        self.photo = PhotoImage(file="view.png")
        self.photoimage = self.photo.subsample(20, 20)
        self.button1 = Button(self.window, image=self.photoimage, compound='right', border=1, command=self.hide)
        self.button1.pack()

        # Login button
        self.button = Button(text="NEXT", bg='blue', fg='white', command=self.authenticate)
        self.button.pack()

        self.window.mainloop()

    def center_widgets(self):
        self.window.update_idletasks()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        self.login.place(x=window_width / 2, y=window_height / 2 - 150, anchor=CENTER)
        self.identifier.place(x=window_width / 2, y=window_height / 2 - 100, anchor='center')
        self.txtfld1.place(x=window_width / 2, y=window_height / 2 - 60, anchor='center')
        self.mp.place(x=window_width / 2, y=window_height / 2 - 10, anchor='center')
        self.txtfld2.place(x=window_width / 2, y=window_height / 2 + 30, anchor='center')
        self.button.place(x=window_width / 2, y=window_height / 2 + 90, anchor='center')
        self.button1.place(x=window_width / 2 + 120, y=window_height / 2 + 30, anchor='center')

    def hide(self):
        self.visible = not self.visible
        if self.visible:
            photo = PhotoImage(file="hide.png")
            self.photoimage = photo.subsample(20, 20)
            self.button1.config(image=self.photoimage)
            self.txtfld2.config(show='')
        else:
            photo = PhotoImage(file="view.png")
            self.photoimage = photo.subsample(20, 20)
            self.button1.config(image=self.photoimage)
            self.txtfld2.config(show='*')

    def authenticate(self):
        #return False
        admin_id = self.txtfld1.get()
        admin_password = self.txtfld2.get()
        #check_internet_connection()
        if admin_id == "" or admin_password == "":
            messagebox.showerror(title='error', message='A field is empty!')
        else:
            admin_ref = self.db.collection('admin').document("13ApkKxSZ36sg8iTxhar")
            admin_data = admin_ref.get()
            if admin_data.exists and admin_data.to_dict()['password'] == admin_password and admin_data.to_dict()['id'] == admin_id:
                # Authentication successful
                self.window.destroy()  # Close the current window or perform any other actions
                self.open_add_employee_app()
            else:
                messagebox.showerror(title='error', message='Invalid credentials')

    def open_add_employee_app(self):
        #root = Tk()
        db=firestore.client()
        add_employee_app = AddEmployeeApp(db)
        #root.mainloop()
    


if __name__ == "__main__":
    db = firestore.client()
    app = AdminLoginApp(db)
