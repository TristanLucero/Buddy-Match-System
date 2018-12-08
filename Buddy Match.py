import random
import json
import os

#Loads data from json file, or if none exists creates ones
def loadData():
  db = {}
  if not os.path.isfile("db.json"):
    with open("db.json", "w") as f:
      json.dump(db, f)
  else:
    with open("db.json", "r") as f:
      db = json.load(f)
  return db
  
#Creates users info for account, to later save in json file
def createAccount():
  user = {}
  user["id"] = random.randint(10001, 99999)
  user["firstName"] = input("First name:").title().strip()
  user["lastName"] = input("Last name:").title().strip()
  user["age"] = input("Age:").strip()
  user["gender"] = input("Gender (m/f):").strip()
  user["hobby"] = input("Interest / Hobby:").title().strip()
  user["location"] = input("Location (na/eu/other):").lower().strip()
  user["contact"] = input("Phone number:").strip()
  user["pin"] = int(input("Pin number:").strip())
  global db
  while 1:
    found = 0
    for dbID, dbUser in db.items():
      if dbUser["pin"] == user["pin"]:
        user["pin"] = input("Please enter another pin, that's ones taken!:")
        found = 1 
        break
    if not found:
      break
    
  return user

#Makes sure pin is valid, and authenticates user if so 
def auth(db):
  pinLogin = int(input("Please enter your pin to login:"))
  temp_uid = "-1"
  for dbID, dbUser in db.items():
    if dbUser["pin"] == pinLogin:
      temp_uid = str(dbID)
      break
  return int(temp_uid)

def mainMenu():
  #uid serves to tell if the user is logged in or not
  uid = -1
  global db
  while 1:
    #While user is not logged in this if will execute
    if uid == -1:
      print("Welcome to the buddy matching system!")
      print("1. Login")
      print("2. Create account")
      print("3. Exit")
      try:
        #Selection serves as users selection for menu
        selection = int(input("Enter selection:"))
      except:
        continue
      if selection == 1:
        while uid == -1:
          try:
            uid = auth(db)
          except KeyboardInterrupt:
            break
          if uid == -1:
            print("Wrong pin, try again:")

      elif selection == 2:
        try:
          user = createAccount()
        except KeyboardInterrupt:
          continue
        i = 0
        while 1:
          if not str(i) in db:
            db[str(i)] = user
            break
          i += 1
      #If user decides to exit program, it will save all info to json file in json dump with formatting
      elif selection == 3:
        with open("db.json", "w") as f:
          json.dump(db, f, sort_keys=True, indent=4, separators=(',', ': '))
        exit("Exitting...")
    #Once user logs in this else will execute    
    else:
      user = db[str(uid)]
      print("Welcome to the buddy matching system!")
      print("1. Match by location")
      print("2. Match by Hobby")
      print("3. Logout")
      print("4. Exit")
      try:  
       selection = int(input("Enter selection:"))
      except:
        continue

      if selection == 1:
        print("Other users at your location:")
        for dbID, dbUser in db.items():
          if uid == int(dbID):
            pass
          elif dbUser["location"] == user["location"]:
            print(dbUser["firstName"], dbUser["lastName"])
      elif selection == 2:
        print("Other users with your hobbies:")
        for dbID, dbUser in db.items():
          if uid == int(dbID):
            pass
          elif dbUser["hobby"] == user["hobby"]:
            print(dbUser["firstName"], dbUser["lastName"])
      elif selection == 3:
        uid = -1
      else:
        with open("db.json", "w") as f:
          json.dump(db, f, sort_keys=True, indent=4, separators=(',', ': '))
        exit("Exitting...")

#calls to functions to start them
#db is the database, and will either be created here or loaded if already created
db = loadData()
mainMenu()