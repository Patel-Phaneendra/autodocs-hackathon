# importing prerequisites
import item

# user class for storing user's info
class User :
    def __init__(self, name, password, contact, email):     # define the user as per his/her details
        self.name = name
        self.password = password
        self.contact = contact
        self.email = email
    def __str__(self):  # to print the user details
        return f"Name : {self.name} || Contact Number : {self.contact} || Email Id : {self.email}"

class Restaurant : 
    userList = []   # store user's details

    # to sign up 
    def signUp(self) :
        print("\n---Sign Up---") 
        name = input("\nEnter your Name : ")
        password = input("Enter your Password : ")
        contact = input("Enter your Contact Number : ")
        email = input("Enter Your Email Id : ")
        user = User(name, password, contact, email)
        self.userList.append(user)
        print("\nSign Up completed successfully...")
        print(user)      

    # user enter to the table
    def table(self, name) :
        bill = 0

        # store order
        userOrder = {}

        print(f"\nWelcome {name}...\nHow can I help you?\n")
        while True :
            print("1 -> View Menu")
            print("2 -> Order Something")
            print("3 -> View Bill")
            print("4 -> Back to Home")
            command = input("Enter command to proceed : ")

            if command == "1" :
                print("\n---Today's Menu---\n")
                for i in item.orderItem :
                    print(f"{i} : Rs {item.orderItem[i]}/-")
                print("\nWould you like to order something?\n")
            elif command == "2" :
                orderLoop = True
                while orderLoop : 
                    order = input("\nWhat would you like to take : ")
                    inOrderItem = order in item.orderItem
                    if inOrderItem == False : 
                        print("\nSorry, we can't serve this order.")
                        print("Please order something from our menu...")
                        continue
                    try : 
                        orderQty = int(input("How many plates would you like to take : "))
                    except ValueError : 
                        print("\nInvalid Input !\nPlease enter a number...")
                        print("\nOk, order again...")
                        continue
                    userOrder[order] = orderQty     # store the order for billing
                    bill += item.orderItem[order] * orderQty
                    if orderQty == 1 :
                        print(f'''\nYour order "{orderQty} plate of {order}" is successfully placed.''')
                    else : 
                        print(f'''\nYour order "{orderQty} plates of {order}" is successfully placed.''')
                    while True : 
                        anotherOrder = input("\nWould you like to take something else [yes/no] : ")
                        if anotherOrder == "no" : 
                            orderLoop = False
                            break
                        elif anotherOrder == "yes" :
                            break 
                        else : 
                            print("\nInvalid Input !\nPlease enter valid Input as shown...")
            elif command == "3" :
                print("\n---Your Order---\n")
                for i in userOrder :
                    print(f"{i} - {userOrder[i]} Plate : {item.orderItem[i]} x {userOrder[i]}")
                print(f"\nYour Total Bill = {bill}/-\n")
            elif command == "4" :
                break
            else :
                print("\nInvalid Input !\nPlease enter valid Input as shown...\n")

    # to log in
    def logIn(self) : 
        print("\n---Log In---")
        logInLoop = True
        while logInLoop : 
            name = input("\nEnter your Name : ")
            password = input("Enter your Password : ")

            found = False
            for user in self.userList :
                if user.name == name and user.password == password :
                    print("\nLog In completed successfully...")
                    found = True
                    self.table(name)
                    break
            if found :
                break
            else :
                print("\nName and Password doesn't match!\n")
                while True : 
                    print("1 -> Try again")
                    print("2 -> Go back")
                    command = input("Enter command to proceed : ")
                    if command == "1" : 
                        break
                    elif command == "2" :
                        logInLoop = False
                        break
                    else :
                        print("\nInvalid Input !\nPlease enter valid Input as shown...\n")

    # to see user's details
    def viewUser(self) : 
        print("\n---User's Details---\n")
        for i in self.userList :
            print(i)

    # starting restaurant
    def call(self) : 
        # welcome message
        print("\n---Welcome to our HIT Cafe---")
        while True :
            print("\n1 -> Sign Up")
            print("2 -> Log In")
            print("3 -> View Users")
            print("4 -> Bye")
            homeCommand = input("Enter command to proceed : ")

            # working depends on command
            if homeCommand == "1" :   # sign up
                self.signUp()
            elif homeCommand == "2" :     # log in
                self.logIn()
            elif homeCommand == "3" :     # view registered user
                self.viewUser()
            elif homeCommand == "4" :     # Bye
                print("\nThank You for visiting our restaurant.\nPlease visit again...\n")
                break
            else :  # for invalid input
                print("\nInvalid Input !\nPlease enter valid Input as shown...\n")


open = Restaurant()
open.call()
# open.table("Kingshuk")

