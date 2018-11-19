#!/usr/bin/python
import os, sys
import getpass
import random
import cv2
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def encrypt(key, filename):
	chunksize = 64*1024
	outputFile = "(e)"+filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = ''

	for i in range(16):
		IV += chr(random.randint(0,0xFF))

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:
		with open(outputFile, 'wb') as outfile:
			outfile.write(filesize)
			outfile.write(IV)
                        os.remove(filename)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += ' ' * (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename[3:]

	with open(filename, 'rb') as infile:
		filesize = long(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key,AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(filesize)


def getKey(password):
	hasher = SHA256.new(password)
	return hasher.digest()

def Main():
	choice = raw_input("Would you like to Encrypt File(EF) or Encrypt Directory(ED) or Decrypt File(DF) or Decrypt Directory(DD) ?: ")
        choice1 = raw_input("Would you like to encrypt-decrypt using (P)assword or (I)mage or (B)oth ?: ") 

	if choice == 'EF' and choice1 == 'I':
		filename = raw_input("File to encrypt: ")
		img = raw_input("Image Password: ")
                password = cv2.imread(img,0)
                cv2.imshow("Gray", password)
                encrypt(getKey(str(password)), filename)
		print filename+" is encrypted"
	
        elif choice == 'DF' and choice1 == 'I':
		filename = raw_input("File to decrypt: ")
                img = raw_input("Image Password: ")
                password = cv2.imread(img,0)
                cv2.imshow("Gray", password)
                decrypt(getKey(str(password)), filename)
                print filename+" is decrypted"
        
        elif choice == 'EF' and choice1 == 'P':
                filename = raw_input("File to encrypt: ")
                password = getpass.getpass("Text Password: ")
                encrypt(getKey(str(password)), filename)
                print filename+" is encrypted"
        
        elif choice == 'DF' and choice1 == 'P':
                filename = raw_input("File to decrypt: ")
                password = getpass.getpass("Text Password: ")
                decrypt(getKey(str(password)), filename)
                print filename+" is decrypted"
        
        elif choice == 'EF' and choice1 == 'B':
                filename = raw_input("File to encrypt: ")
                password1 = getpass.getpass("Text Password: ")
                img = raw_input("Image Password:")
                password2 = cv2.imread(img,0)
                cv2.imshow("Gray", password2)
                password = str(password1)+str(password2)
                encrypt(getKey(str(password)), filename)
                print filename+" is encrypted"

        elif choice == 'DF' and choice1 == 'B':
                filename = raw_input("File to encrypt: ")
                password1 = getpass.getpass("Text Password: ")
                img = raw_input("Image Password:")
                password2 = cv2.imread(img,0)
                cv2.imshow("Gray", password2)
                password = str(password1)+str(password2)
                decrypt(getKey(str(password)), filename)
                print filename+" is decrypted"
        
        elif choice == 'ED' and choice1 == 'P':
                filename2 = raw_input("Directory to encrypt: ")
                s1='tar -czf '+filename2+'.tar.gz '+filename2
                os.system(s1)
                filename = filename2+'.tar.gz'
                password = getpass.getpass("Text Password: ")
                encrypt(getKey(str(password)), filename)
                print filename+" is encrypted"
                os.system('rm -rf '+filename2)
                os.system('rm -rf '+filename2+'.tar.gz')
        
        elif choice == 'DD' and choice1 == 'P':
                filename = raw_input("Directory to decrypt: ")
                password = getpass.getpass("Text Password: ")
                decrypt(getKey(str(password)), filename)
                print filename+" is decrypted"
                s1 = 'tar -xzf '+filename[3:]
                os.system(s1)
                s2 = 'rm -rf \''+filename+'\''
                os.system(s2)
                os.system('rm -rf '+filename[3:])

        elif choice == 'ED' and choice1 == 'I':
                filename2 = raw_input("Directory to encrypt: ")
                s1='tar -czf '+filename2+'.tar.gz '+filename2
                os.system(s1)
                filename = filename2+'.tar.gz'
                password1 = raw_input("Image Password: ")
                password = cv2.imread(password1,0)
                cv2.imshow("Gray",password)
                encrypt(getKey(str(password)), filename)
                print filename+" is encrypted"
                os.system('rm -rf '+filename2)
                os.system('rm -rf '+filename2+'.tar.gz')

        elif choice == 'DD' and choice1 == 'I':
                filename = raw_input("Directory to decrypt: ")
                img = raw_input("Image Password: ")
                password = cv2.imread(img,0)
                cv2.imshow("Gray", password)
                decrypt(getKey(str(password)), filename)
                print filename+" is decrypted"
                s1 = 'tar -xzf '+filename[3:]
                os.system(s1)
                s2 = 'rm -rf \''+filename+'\''
                os.system(s2)
                os.system('rm -rf '+filename[3:])
        
        elif choice == 'ED' and choice1 == 'B':
                filename2 = raw_input("Directory to encrypt: ")
                s1='tar -czf '+filename2+'.tar.gz '+filename2
                os.system(s1)
                filename = filename2+'.tar.gz'
                password1 = getpass.getpass("Text Password: ")
                img = raw_input("Image Password: ")
                password2 = cv2.imread(img,0)
                cv2.imshow("Gray",password2)
                password = str(password1)+str(password2)
                encrypt(getKey(str(password)), filename)
                print filename+" is encrypted"
                os.system('rm -rf '+filename2)
                os.system('rm -rf '+filename2+'.tar.gz')

        elif choice == 'DD' and choice1 == 'B':
                filename = raw_input("Directory to decrypt: ")
                password1 = getpass.getpass("Text Password: ")
                img = raw_input("Image Password: ")
                password2 = cv2.imread(img,0)
                cv2.imshow("Gray", password2)
                password = str(password1)+str(password2)
                decrypt(getKey(str(password)), filename)
                print filename+" is decrypted"
                s1 = 'tar -xzf '+filename[3:]
                os.system(s1)
                s2 = 'rm -rf \''+filename+'\''
                os.system(s2)
                os.system('rm -rf '+filename[3:])
        
        else:
		print "No option selected, closing ....."

if __name__ == '__main__':
    try:	
        Main()
    except:
        print('Please give valid input')
