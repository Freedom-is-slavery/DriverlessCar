import os
import shutil


WriteFold = 'D:\\picbase\\test\\capture'

if not(os.path.exists(WriteFold)):
    os.makedirs(WriteFold)
    print("Now the folder {} has been created".format(WriteFold))
else:
    print("The folder {} already exists".format(WriteFold))


clr = input("Would you like to clear the folder?y/n\n")
if (clr == "y"):
    shutil.rmtree(WriteFold)
    os.makedirs(WriteFold)