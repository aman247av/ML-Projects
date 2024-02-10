import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage

cred = credentials.Certificate("db-key.json")
firebase_admin.initialize_app(cred,{
    "databaseURL" : "https://face-attendance-system-e4038-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket" : "face-attendance-system-e4038.appspot.com"
})

ref = db.reference('Employees')

data = {
    "210101" : {
        "name" : "Aman Verma",
        "designation" : "SDE",
        "starting_year" : 2023,
        "total_attendance" : 6,
        "last_login" : "2023-10-25 20:11:30",
        "profile_pic" : "https://firebasestorage.googleapis.com/v0/b/face-attendance-system-e4038.appspot.com/o/Images%2F210101.png?alt=media&token=58458c29-4d37-4d41-b976-33be01d31eaa"
    },
    "321654" : {
        "name" : "Mortaza Hamad",
        "designation" : "SDE",
        "starting_year" : 2022,
        "total_attendance" : 2,
        "last_login" : "2023-10-25 20:11:30",
        "profile_pic" : "https://firebasestorage.googleapis.com/v0/b/face-attendance-system-e4038.appspot.com/o/Images%2F321654.png?alt=media&token=5dfcc0b6-b976-4547-852e-46eaa3e0ae16"
    },
    "852741" : {
        "name" : "Emily Blunt",
        "designation" : "SDE Intern",
        "starting_year" : 2021,
        "total_attendance" : 0,
        "last_login" : "2023-10-25 20:11:30",
        "profile_pic" : "https://firebasestorage.googleapis.com/v0/b/face-attendance-system-e4038.appspot.com/o/Images%2F852741.png?alt=media&token=8b747eb0-5579-4166-8f5d-09eff9ee7874"
    },
    "963852" : {
        "name" : "Elon Musk",
        "designation" : "Director",
        "starting_year" : 2020,
        "total_attendance" : 183,
        "last_login" : "2023-10-25 20:11:30",
        "profile_pic" : "https://firebasestorage.googleapis.com/v0/b/face-attendance-system-e4038.appspot.com/o/Images%2F963852.png?alt=media&token=578e5db3-8f2e-4a14-9630-aac416c5e272"
    }
}


for key, value in data.items():
    ref.child(key).set(value)

