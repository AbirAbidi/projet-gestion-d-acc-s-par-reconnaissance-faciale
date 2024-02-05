# main.py
from tkinter import Tk

from adminDashboard import AdminLoginApp
import firebase_admin
from    firebase_admin import credentials, firestore
# Initialize Firebase (call this only once)
cred = credentials.Certificate('C:/Users/hp/Downloads/raspberrypi-1ece3-firebase-adminsdk-zsme5-ee2a725f3c.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

if __name__ == "__main__":  
    #root = Tk()        
    app = AdminLoginApp(db) 
    #root.mainloop()
