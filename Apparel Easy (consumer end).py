from tkinter import *
import tkinter.messagebox as tmsg
import pandas as pd
import webbrowser as wb
from datetime import date
import numpy as np
import pyqrcode as qr
from sqlalchemy import create_engine

# ------------------------------------------------------------------
# Credentials for database
user = 'Priyanshu'
pwd = 'pass1234'
host = 'localhost'
db_name = 'mydb'

# Establishing connection
connection_string = f"mysql+pymysql://{user}:{pwd}@{host}/{db_name}"
engine = create_engine(connection_string)
engine.connect()
# ------------------------------------------------------------------

root = Tk()

win_width = 800
win_height = 550

root.geometry(f'{win_width}x{win_height}')
root.minsize(win_width-100,win_height-50)
root.maxsize(win_width+200,win_height+50)
root.title('Apparel Easy')

def drop():
    df = pd.read_csv('credentials.csv')
    name = input('Username : ')
    if name in df['Username'].values:
        user_data = df.loc[df['Username']==name]
        pword = user_data['Password'].values[0]
        no = user_data['Pno.'].values[0]
        pwd = input('Password : ')
        num = input('Enter your registered phone number : ')

        if (num == str(no)) and (pwd == str(pword)):
            user_data_index = user_data.index[0]
            df.drop(user_data_index,inplace=True)
            print('Account Removed!!')
            df.to_csv('credentials.csv',index=False)
            df.to_sql('credentials',engine,index=False,if_exists='replace')
        else:
            tmsg.showinfo("Account's Manager",'No such account exists')
    else:
        tmsg.showinfo("Account's Manager",'No such account exists')

M = Menu(root)
M.add_command(label='Delete my Account',
command=drop)
root.config(menu=M,bg='#e3bcca')

Label(root,
text='Apparel Easy',
font='bold 25',
bg='black',
fg='white').pack(fill=X, side=TOP)

Label(root,
text='LOGIN',
font='bold 20',
bg='#e3bcca').pack(pady=10)

df = pd.read_csv('credentials.csv')

def signup_page():
    i1 = input('Username : ')
    i2 = input('Password : ')
    i3 = input('Phone Number : ')
    l = [i1,i2,i3]
    df.loc[len(df)] = l
    df.to_csv('credentials.csv',index=False)
    df.to_sql('credentials',engine,index=False,if_exists='replace')
    print('Your account is created')

Button(root,
text='Create new account @appareleasy',
font='bold 15',
bg='black',
fg='white',
command=signup_page).pack(fill=X, padx=50, side=BOTTOM)

C1 = Canvas(root,
width=500,
height=50)
C1.pack(pady=8)

C1.create_rectangle([0,0],[500,50],
fill='#db2525')

F1 = Frame(root,
bg='#e3bcca')
F1.pack(pady=30,padx=50)

Label(F1,
text='Username : ',
font='bold 18',
bg='#e3bcca').grid(row=0,column=0,pady=10,padx=10)

v1 = StringVar()

Entry(F1,
textvariable=v1,
font='bold 18').grid(row=0,column=1,pady=10,padx=10)

Label(F1,
text='Password : ',
font='bold 18',
bg='#e3bcca').grid(row=1,column=0,pady=10,padx=10)

v2 = StringVar()

Entry(F1,
textvariable=v2,
font='bold 18',
show='*').grid(row=1,column=1,pady=10,padx=10)

saleDf = pd.read_csv('saleDetails.csv')

def login():
    data = pd.read_csv('credentials.csv')
    userlist = list(data['Username'])
    if v1.get() in userlist:
        uname = v1.get()
        pwdrow = data.loc[data['Username']==uname]
        pwd = pwdrow['Password'].values[0]
        if v2.get() == pwd:
            wb.open_new('catalogue.html')
            portal()
        else:
            tmsg.showerror('Password Manager','Invalid Password!!')
    else:
        tmsg.showinfo("Accounts' Manager",'Not a registered account')
        response = tmsg.askyesno('Apparel Easy','Create a new account')
        if response == YES:
            signup_page()
        else:
            pass
    v1.set('')
    v2.set('')

def portal():
    print(f'________________________Welcome {v1.get()}________________________')
    festive_season = range(9,13)
    end_of_season = range(2,8)

    if date.today().month in festive_season:
        event = 'FEST'
        print('--------------------------------------------')
        print('------------Festive Season sale-------------')
        print(' Mega 10 percent discount on every purchase ')
        print('--------------------------------------------')
        print('-------------Coupon Code : FEST-------------')
        print('--------------------------------------------')
        print()
    elif date.today().month in end_of_season:
        event = 'EOS'
        print('------------------------------------------')
        print('------------End of Season sale------------')
        print('Mega 15 percent discount on every purchase')
        print('------------------------------------------')
        print('-------------Coupon Code : EOS------------')
        print('------------------------------------------')
        print()
    else:
        event = 'nil'

    data = pd.read_csv('credentials.csv')
    custID = 'AE' + str(1+int(list(data['Username']).index(v1.get())))

    d1 = {'Shirt':900,'Denim':1500,'Trouser':1000,'Shoe':850}
    d2 = {'Kurta':2100,'T-shirt':550,'Pant':1000,'Skirt':700}

    while True:
        htp = input('1--> Shop\n2--> Leave\n:')
        if htp == '1':
            i1 = input('Category :\n1--> Men\n2--> Women\n:')
            if i1 == '1':
                print('---------------------------------------')
                print(pd.DataFrame(d1,index=['Price']))
                print('---------------------------------------')
                print()
                print('1--> Shirt')
                print('2--> Denim')
                print('3--> Trouser')
                print('4--> Shoe')
                i1m = input('Desired apparel : ')

                i1mq = int(input('Quantity : '))

                if int(i1m) == 1:
                    price = d1['Shirt']*i1mq
                elif int(i1m) == 2:
                    price = d1['Denim']*i1mq
                elif int(i1m) == 3:
                    price = d1['Trouser']*i1mq
                elif int(i1m) == 4:
                    price = d1['Shoe']*i1mq    
                else:
                    print('Choose apparel from given list')
                    portal()

                if event == 'FEST' or event == 'EOS':
                    c_code1 = input('Enter Coupon Code : ')
                elif event == 'nil':
                    c_code1 = 'nil'
                
                if event == 'FEST' and c_code1 == 'FEST':
                    act_price = price - (price/10)
                elif event == 'EOS' and c_code1 == 'EOS':
                    act_price = price - ((3*price)/20)
                else:
                    act_price = price

            elif i1 == '2':
                print('---------------------------------------')
                print(pd.DataFrame(d2,index=['Price']))
                print('---------------------------------------')
                print()
                print('1--> Kurta')
                print('2--> T-shirt')
                print('3--> Pant')
                print('4--> Skirt')
                i1w = input('Desired apparel : ')
                i1wq = int(input('Quantity : '))

                if int(i1w) == 1:
                    price = d2['Kurta']*i1wq
                elif int(i1w) == 2:
                    price = d2['T-shirt']*i1wq
                elif int(i1w) == 3:
                    price = d2['Pant']*i1wq
                elif int(i1w) == 4:
                    price = d2['Skirt']*i1wq
                else:
                    print('Choose apparel from given list')
                    portal()
                
                if event == 'FEST' or event == 'EOS':
                    c_code2 = input('Enter Coupon Code : ')
                elif event == 'nil':
                    c_code2 = 'nil'
                
                if event == 'FEST' and c_code2 == 'FEST':
                    act_price = price - (price/10)
                elif event == 'EOS' and c_code2 == 'EOS':
                    act_price = price - ((3*price)/20)
                else:
                    act_price = price
                
            else:
                pass
            
            address = input('Enter your address : ')

            def authentication():
                confirm = input('Proceed to Pay :\n1--> Yes\n2--> No\n:')
            
                if confirm == '1':
                    print('-------------------------------------')
                    print('------Two Factor Authentication------')
                    print('-------------------------------------')

                    pNo = data.loc[data['Username']==v1.get()]['Pno.'].values
                    phone = str(pNo[0])

                    def otp_gen():
                        otp = ''
                        for j in range(5):
                            otp += phone[int(((np.random.random())*len(phone))//1)]
                        return otp
                    otp = otp_gen()

                    i = input('Enter your registered phone number : ')
                    
                    try:
                        if int(i) == pNo[0]:
                            code = qr.create(otp)
                            code.png('QR.png',scale=5)
                    
                            window = Toplevel(root)
                            window.title('QR Code')
                            window.minsize(300,150)
                            window.maxsize(300,150)

                            img = PhotoImage(file='QR.png')

                            Label(window,
                            image=img).pack()

                            OTP = input('Enter OTP : ')

                            if OTP == otp:
                                print('------------------------')
                                print(f'Your bill is {act_price} Rupees')
                                print('------------------------')
                                print()
                                print('How you want to make payment ?')

                                i1mp = input('1--> COD\n2--> CrediCard\n3--> UPI\n: ')

                                if int(i1mp) == 1:
                                    paydetail = 'Cash On Delivery'
                                    print('Your apparel will be delivered :)')
                                    print(f'Latest by 5 days from {date.today()}')
                                elif int(i1mp) == 2:
                                    paydetail = input('Enter CVV {format"CVV"<number>} : ')
                                    print('Your apparel will be delivered :)')
                                    print(f'Latest by 5 days from {date.today()}')
                                elif int(i1mp) == 3:
                                    paydetail = input('Enter UPI {format"UPI"<number>} : ')
                                    print('Your apparel will be delivered :)')
                                    print(f'Latest by 5 days from {date.today()}')
                                elif type(i1mp) is not int:
                                    print('Choose one from given list')
                                    authentication()
                                else:
                                    print('Choose one from given list')
                                    authentication()

                                saleDf.loc[len(saleDf)] = [custID,address,paydetail,act_price,date.today()]

                                saleDf.to_csv('saleDetails.csv',index=False)
                                saleDf.to_sql('sales',engine,index=False,if_exists='replace')
                                print('Thank You')
                                print('------------------------------------')
                            else:
                                print('Incorrect OTP')
                                print('----------Try Again----------')
                                authentication()
                        
                        else:
                            print("Not your registered phone number")
                            print('----------Try Again----------')
                            authentication()
                    except:
                        print('Enter phone number correctly!!')
                        authentication()
                elif confirm == '2':
                    return
                else:
                    return
            
            authentication()

        elif htp == '2':
            print('Thank You')
            quit()
        else:
            quit()

Button(F1,
text='Login',
font='bold 15',
bg='black',
fg='white',
command=login).grid(row=2,column=2)

C2 = Canvas(root,
width=500,
height=50)
C2.pack()

C2.create_rectangle([0,0],[500,50],
fill='slategrey')

root.mainloop()