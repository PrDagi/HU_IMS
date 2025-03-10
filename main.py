from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from src.Userlogin import Login
from src.Admin_menu import Admin
from src.User_menu import User

# MAIN WINDOW
class Main(Login,Admin,User):

    def __init__(self):
        Login.__init__(self)
        self.loginw.mainloop()
        self.loginw.state('withdraw')  # LOGIN WINDOW EXITS
        self.mainw = Toplevel(bg="#FFFFFF")
        width = 1366
        height = 640
        screen_width = self.mainw.winfo_screenwidth()
        screen_height = self.mainw.winfo_screenheight()
        # x = (screen_width / 2) - (width / 2)
        # y = (screen_height / 2) - (height / 2)
        self.mainw.geometry("%dx%d" % (width, height))
        self.mainw.title("Inventory")
        self.mainw.resizable(0,0)
        self.mainw.protocol('WM_DELETE_WINDOW', self.__Main_del__)
        self.getdetails()

    # OVERRIDING CLOSE BUTTON && DESTRUCTOR FOR CLASS LOGIN AND MAIN WINDOW
    def __Main_del__(self):
        if messagebox.askyesno("Quit", " Leave Inventory?") == True:
            self.loginw.quit()
            self.mainw.quit()
            exit(0)
        else:
            pass

    # FETCH USER DETAILS FROM PRODUCTS,USERS AND INVENTORY TABLE
    def getdetails(self):
        self.cur.execute("CREATE TABLE if not exists products(product_id varchar (20),product_name varchar (50) NOT NULL,product_desc varchar (50) NOT NULL,product_cat varchar (50),product_price INTEGER NOT NULL,stocks INTEGER NOT NULL,PRIMARY KEY(product_id));")
        self.cur.execute("CREATE TABLE if not exists sales (Trans_id	INTEGER,invoice	INTEGER NOT NULL,Product_id	varchar (20),Quantity INTEGER NOT NULL,Date	varchar (20),Time varchar (20),PRIMARY KEY(Trans_id));")
        self.cur.execute("select * from products ")
        self.products = self.cur.fetchall()
        capuser = self.username.get()
        capuser = capuser.upper()
        self.cur.execute("select account_type from users where username= ? ", (capuser,))
        l = self.cur.fetchall()
        self.account_type = l[0][0]
        self.buildmain()

    #  ADD WIDGETS TO TOP OF MAIN WINDOW
    def buildmain(self):
        if self.account_type == 'ADMIN':
            super(Admin).__init__()
            self.admin_mainmenu(8,8)
        else:
            super(User).__init__()
            self.user_mainmenu(8,8)
        self.logout.config(command=self.__Main_del__)
        self.changeuser.config(command=self.change_user)
        self.topframe=LabelFrame(self.mainw,width=1366,height=60,bg="#4267b2")
        self.topframe.place(x=0,y=0)
        self.store_name = 'HU'
        self.storelable=Label(self.topframe,text=self.store_name + " Sales & Inventory System",bg="#4267b2",anchor="center")
        self.storelable.config(font="Roboto 16 bold",fg="snow")
        self.storelable.place(x=360,y=16)
        mi = PhotoImage(file="images/myprofile.png")
        mi = mi.subsample(4,4)
        self.myprofile = ttk.Label(self.topframe,text=(self.username.get()).capitalize(),image=mi, compound=TOP)
        self.myprofile.image = mi
        self.myprofile.place(x=1300,y=15)
        ''''
        if self.account_type == 'ADMIN':
            self.adminlabel= Label(self.topframe,text="Admin",font="Roboto 10 bold",bg="#4267b2")
        else:
            self.adminlabel = Label(self.topframe, text=" User", font="Roboto 10 bold", bg="#4267b2")
        self.adminlabel.place(x=1300,y=80)
        '''
        # DATE TIME LABEL
        ''''
        now = datetime.datetime.now()
        self.datetimelabel= Label(self.topframe,text=str(now.day)+'/'+str(now.month)+'/'+str(now.year),font="Roboto 10 bold", bg="skyblue2")
        self.datetimelabel.place(x=1290,y=90)
        '''

    # METHODS FOR ITEMS AND CHANGE USER BUTTONS
    def change_user(self):
        if messagebox.askyesno("Alert!", "Do  you want to change user?") == True:
            self.base.commit()
            self.mainw.destroy()
            self.loginw.destroy()
            self.__init__()


if __name__ == '__main__':
    w = Main()
    w.base.commit()
    w.mainw.mainloop()
