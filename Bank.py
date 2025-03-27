import tkinter as tk
from tkinter import *
#from PIL import Image, ImageTk 
from tkinter import messagebox
import sqlite3
import random
import os
import math
import smtplib
from fpdf import FPDF
from pdf_mail import sendpdf
from datetime import datetime

window=tk.Tk()
window.config(bg='#004C8F')
# canvas = Canvas(window, width = 1000, height = 180,)
# canvas.place(x=0,y=30)
# img = ImageTk.PhotoImage(Image.open('D:\\\HDFC-Bank-Logo.png'))
# canvas.create_image(0, 0, anchor=NW, image=img)
# window.iconwindow('C:\Users\Incapp\Downloads\project1\HDFC-Bank-Logo.png')
window.title("HDFC Bank")
window.geometry('650x650')
user_label=tk.Label(window,text='Login ID',font=('BOLD',20),fg='white',bg='#004C8F')
user_label.place(x=100,y=50)
password_label=tk.Label(window,text='Password',font=('BOLD',20),fg='white',bg='#004C8F')
password_label.place(x=100,y=100)
user_entry=tk.Entry(window,font=('BOLD',15))
password_entry=tk.Entry(window,font=('BOLD',15))
user_entry.place(x=250,y=50)
password_entry.place(x=250,y=100)

def verify():
        a = int(e_otp.get())
        if a == otp:
            new_win=tk.Tk()
            new_win.title("Reset Password")
            new_win.geometry('450x200')
            new_win.configure(bg='#004C8F')
            new_label=tk.Label(new_win,text='Enter New Password',font=('BOLD',15))
            new_label.place(x=10,y=15)
            new_entry=tk.Entry(new_win,font=('BOLD',13))
            new_entry.place(x=250,y=15)
            def reset():
                new_pass=new_entry.get()
                conn = sqlite3.connect('HDFC.db')
                c = conn.cursor()
                c.execute("UPDATE users SET password=? WHERE email=?", (new_pass, entr_email.get()))
                conn.commit()
                c.close()
                conn.close()
                new_win.destroy()
                win1.destroy()
                messagebox.showinfo('success',"password changed successfully...")
                
            btn=tk.Button(new_win,text='conform',command=reset)
            btn.place(x=150,y=90)
        else:
            win1.destroy()
            messagebox.showerror('error ',"invalid otp")
def forget():
    global win1
    win1=tk.Tk()
    win1.title("Forget Password")
    win1.geometry('450x200')
    user_label=tk.Label(win1,text='Email',font=('BOLD',15))
    user_label.place(x=10,y=15)
    global entr_email
    entr_email=tk.Entry(win1,font=('BOLD',13))
    entr_email.place(x=120,y=15)

    user_lab=tk.Label(win1,text='verify otp',font=('BOLD',15))
    user_lab.place(x=10,y=100)
    global e_otp
    e_otp=tk.Entry(win1,font=('BOLD',13))
    e_otp.place(x=200,y=100)


    def send_otp():
        global otp
        otp=random.randint(1111,9999)
        # otp=1234
        msg=f"your otp is , {otp}"
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login('mohit10803@gmail.com', 'czen mhok nefe cjne')
        global emailid
        emailid = entr_email.get()
        s.sendmail('Your  otp for reset your password is ',emailid,msg)
        
        
        



    b1=tk.Button(win1,text='send otp',font=(10),command=send_otp)
    b1.place(x=80,y=60)
    btn=tk.Button(win1,text='conform',command=verify)
    btn.place(x=80,y=120)

    win1.mainloop()
def login_window():
    w2=tk.Tk()
    w2.title("Login")
    w2.geometry('650x650')
    try:
        global email
        email=user_entry.get()
        password=password_entry.get()
        conn = sqlite3.connect('HDFC.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        
        data=c.fetchall()
        c.close()
        conn.close()
        if data:
            print(data)
            u1=tk.Label(w2,text=F'WELCOME                   {data[0][1]}',font=('BOLD',15))
            u1.place(x=20,y=20)
            u2=tk.Label(w2,text=F'ACCOUNT NO              {data[0][-2]}',font=('BOLD',15))
            u2.place(x=20,y=70)
            u3=tk.Label(w2,text=F'BALANCE                   {data[0][-1]}',font=('BOLD',15))
            u3.place(x=20,y=120)
            global balance
            balance=data[0][-1]
            def send_money():
                ws=tk.Tk()
                ws.title('Send Money')
                u1=tk.Label(ws,text=F'Account No',font=('BOLD',15))
                u1.place(x=20,y=20)
                e1=tk.Entry(ws)
                e1.place(x=20,y=50)
                u3=tk.Label(ws,text=F'Amount',font=('BOLD',15))
                u3.place(x=20,y=120)
                e2=tk.Entry(ws)
                e2.place(x=20,y=150)
                def send_money_comform():
                    global amount
                    amount=int(e2.get())
                    global sender_account
                    sender_account=int(data[0][-2])
                    reciver_account=int(e1.get())
                    if int(amount)<=int(balance):
                        updated_values=int(balance)-int(amount)
                        conn = sqlite3.connect('HDFC.db')
                        c = conn.cursor()
                        # c.execute("SELECT * FROM users WHERE account=?",(int(e1.get()),))
                        # data=c.fetchall()
                        c.execute("UPDATE users SET balance=? WHERE account=?", (updated_values, sender_account))
                        conn.commit()
                        c.execute("SELECT * FROM users WHERE email=?", (email,))
                        global rem_amount
                        rem_amount=c.fetchall()
                        print(rem_amount[-1][-1])
                        # c.execute("INSERT INTO transactions (sender,receiver,amount) VALUES (?,?,?)",(email
                        c.close()
                        conn.close()

                        ws.destroy()
                        w2.destroy()
                        messagebox.showinfo('success','money send successfully')
                        generate_invoice()
                    else:
                        messagebox.showerror('error',f'insufficient balance in \n {data[0][-2]}')
        
                send_buttton=tk.Button(ws,text='confirm',font=('BOLD',13),command=send_money_comform)
                send_buttton.place(x=130,y=180)
                ws.mainloop()
            send_buttton=tk.Button(w2,text='send money',font=('BOLD',13),command=send_money)
            send_buttton.place(x=130,y=180)
            w2.mainloop()
        
        else:
            raise Exception('login id and password is not matched')
        
    except Exception as e:
        messagebox.showerror('error',e)
    w2.destroy()
    

"""=============================================================="""
def generate_invoice():
   
    # index=tree.selection()[0]
    # new=tree.item(index,'values')[0]
    # n=int(new[0])
    # conn=sqlite3.connect("ims.db")
    # cur=conn.cursor()
    # cur.execute("select * from records where id =?",(n,))
    # data=cur.fetchall()
    # print(data)
    # conn.commit()

    # if not data:
    #     messagebox.showwarning("Database Error", "No data found in the database.")
    #     return

    # Get current date and time
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Create a PDF instance
    pdf = FPDF()
    pdf.add_page()

    # Set title
    pdf.set_font("Arial", size=20,style="BU")
    pdf.cell(200, 10, txt="INVOICE", ln=True, align="C")

    # Add date and time
    pdf.set_font("Arial", size=10,style="BIU")
    pdf.cell(200, 10, txt=f"Date: {date_time}", ln=True, align="R")
    pdf.ln(10)

    # Add customer and invoice details
    pdf.cell(200, 10, txt=f"HDFC BANK", ln=True, align="L",)
    pdf.cell(200, 10, txt=f"ACCOUNT NUMBER: {sender_account}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"BALANCE: {rem_amount[-1][-1]}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Deduction: {amount}", ln=True, align="L")
    pdf.ln(10)

    # Add table headers (centered)
    pdf.set_font("Arial", size=10, style='BU')
    table_start_x = 46
    pdf.set_x(table_start_x)
    pdf.cell(30, 10, txt="ACCOUNT NUMBER", border=1, align="C")
    pdf.cell(30, 10, txt="BALANCE", border=1, align="C")
    pdf.cell(30, 10, txt="Deduction", border=1, align="C")
    pdf.ln()

    # Add table rows with data from the database (centered)
    pdf.set_font("Arial", size=10,style="I")
    
    pdf.set_x(table_start_x)
    pdf.cell(40, 10, txt=str(sender_account), border=1, align="C")
    pdf.cell(30, 10, txt=str(rem_amount[-1][-1]), border=1, align="C")
    pdf.cell(30, 10, txt=str(amount), border=1, align="C")
    pdf.ln()

    # Save the PDF
    pdf.output("D:\\invoice.pdf")
    messagebox.showinfo("SUCCESS", "Invoice Generated Successfully")
    send_invoice()
    
def send_invoice():
    try:
        sender_email = 'mohit10803@gmail.com'
        receiver_email = email
        sender_pass = 'czen mhok nefe cjne' 
        subject = "HEYYY THERE!!"
        body = "This is to inform you that balance has been deducted and sent to you.\n Please find your attached invoice"
        filepath='D:\\invoice.pdf'
        if not filepath:
            raise FileNotFoundError("No file has been selected.")
        
        file_name_with_ext = os.path.basename(filepath)
        file_name, _ = os.path.splitext(file_name_with_ext)
        location = os.path.dirname(filepath)

        send = sendpdf(sender_email, receiver_email, sender_pass, subject, body, file_name, location)
        send.email_send()
        messagebox.showinfo("SUCCESS", "File has been sent")
        

    except ValueError as ve:
        print(f"ValueError: {ve}")
        messagebox.showwarning("Input Error", str(ve))
    except FileNotFoundError as fnf_error:
        print(f"FileNotFoundError: {fnf_error}")
        messagebox.showerror("File Error", str(fnf_error))
    except Exception as e:
        print(f"Unexpected Error: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")




check_data=7593908468
def register_window():
    
    w3=tk.Tk()
    w3.title('Registration')
    w3.geometry('650x650')
    heading=tk.Label(w3,text='REGISTRATION FORM',font=('BOLD',20),fg='#004C8F')
    heading.place(x=220,y=30)
    reg_user_label=tk.Label(w3,text='USER NAME',font=('BOLD',15),fg='#004C8F')
    reg_user_label.place(x=200,y=100)
    reg_user_entry=tk.Entry(w3,font=('BOLD',15))
    reg_user_entry.place(x=350,y=100)

    email_user_label=tk.Label(w3,text='EMAIL',font=('BOLD',15),fg='#004C8F')
    email_user_label.place(x=200,y=150)
    email_user_entry=tk.Entry(w3,font=('BOLD',15))
    email_user_entry.place(x=350,y=150)

    password_user_label=tk.Label(w3,text='PASSWORD',font=('BOLD',15),fg='#004C8F')
    password_user_label.place(x=200,y=200)
    password_user_entry=tk.Entry(w3,font=('BOLD',15))
    password_user_entry.place(x=350,y=200)

    number_user_label=tk.Label(w3,text='MOBILE NO',font=('BOLD',15),fg='#004C8F')
    number_user_label.place(x=200,y=250)
    number_user_entry=tk.Entry(w3,font=('BOLD',15))
    number_user_entry.place(x=350,y=250)

    aadhar_user_label=tk.Label(w3,text='AADHAR',font=('BOLD',15),fg='#004C8F')
    aadhar_user_label.place(x=200,y=300)
    aadhar_user_entry=tk.Entry(w3,font=('BOLD',15))
    aadhar_user_entry.place(x=350,y=300)

    # otp_user_label=tk.Label(w3,text='OTP',font=('BOLD',15),fg='#004C8F')
    # otp_user_label.place(x=200,y=350)
    # otp_user_entry=tk.Entry(w3,font=('BOLD',15))
    # otp_user_entry.place(x=350,y=350)

    balance_user_label=tk.Label(w3,text='Balance',font=('BOLD',15),fg='#004C8F')
    balance_user_label.place(x=200,y=400)
    balance_user_entry=tk.Entry(w3,font=('BOLD',15))
    balance_user_entry.place(x=350,y=400)
    def save_record():
        
        try:
            conn = sqlite3.connect('HDFC.db')
            c = conn.cursor()
            c.execute("SELECT *  FROM users ")
            global check_data
            check_data=c.fetchall()
            print(check_data)
            conn.close()
            account=random.randint(1111111111,9999999999)
            
            user_name=reg_user_entry.get()
            email= email_user_entry.get()
            password= password_user_entry.get()
            number= number_user_entry.get()
            aadhar= aadhar_user_entry.get()
            otp= 12345
            conn=sqlite3.connect('hdfc.db')
            c=conn.cursor()
            c.execute('create table if not exists users(id integer primary key AUTOINCREMENT,user_name varchar(100),email varchar(90),password varchar(40),number int,aadhar int, otp int,account int,balance int)')
            c.execute("INSERT INTO users(user_name,email,password,number,aadhar,otp,account,balance) VALUES(?,?,?,?,?,?,?,?)",(user_name,email,password,number,aadhar,otp,valid_account,balance_user_entry))
            conn.commit()
            conn.close()
            w3.destroy()
        except Exception as e:
            valid_account=random.randint(1111111111,9999999999)
            user_name=reg_user_entry.get()
            email= email_user_entry.get()
            password= password_user_entry.get()
            number= number_user_entry.get()
            aadhar= aadhar_user_entry.get()
            otp= 12345
            conn=sqlite3.connect('hdfc.db')
            c=conn.cursor()
            c.execute('create table if not exists users(id integer primary key AUTOINCREMENT,user_name varchar(100),email varchar(90),password varchar(40),number int,aadhar int, otp int,account int,balance int)')
            c.execute("INSERT INTO users(user_name,email,password,number,aadhar,otp,account,balance) VALUES(?,?,?,?,?,?,?,?)",(user_name,email,password,number,aadhar,otp,valid_account,int(balance_user_entry.get())))
            conn.commit()
            conn.close()
            w3.destroy()
            print("form exception ,,,,,,,,,,,,")
        
    button_b1=tk.Button(w3,text='SUBMIT',font=('BOLD',13),command=save_record)
    button_b1.place(x=410,y=450)
    w3.mainloop()

login_button=tk.Button(window,text='Login',font=('BOLD',13),bg='light green',command=login_window)
login_button.place(x=230,y=150)
forget_button=tk.Button(window,text='Forget',font=('BOLD',13),bg='gray',command=forget)
forget_button.place(x=330,y=150)
registration_button=tk.Button(window,text='Registration',font=('BOLD',13),bg='light gray',command= register_window)
registration_button.place(x=260,y=200)
window.mainloop()