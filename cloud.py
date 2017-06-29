import swiftclient
import keystoneclient
import os
import pyDes
from flask import Flask, request, redirect, url_for
from Tkinter import Tk
from tkFileDialog import askopenfilename

print 'gunjan'
auth_url = "https://identity.open.softlayer.com"+ '/v3'
password = "sN(7N3E3{mn*GLf5"
project_id = "3ba375f9ce3b4f55a0f66b84942beade"
user_id = "aa8e8dbe976347b4b3ffe8abb50a810d"
region_name = "dallas"
conn = swiftclient.Connection(key=password,
                              authurl=auth_url,
                              auth_version='3',
                              os_options={"project_id": project_id,
                                          "user_id": user_id,
                                          "region_name": region_name})
cont_name = "assn1"
conn.put_container(cont_name)

while 1:

    print("Choose an option by entering the appropriate number:")

    print("Options:\n1.Upload a file\n2.List the files\n3.Download the file\n4.Delete the file\n5.Read the file")

    print
    "Enter a number:",

    input = raw_input()

    if input == "1":

        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

        filepath = askopenfilename()  # show an "Open" dialog box and return the path to the selected file

        print(filepath)

        head, tail = os.path.split(filepath)

        file_name = tail

        with open(filepath, 'r') as upload_file:
            my_file = open(file_name)
            file_contents = my_file.read()
            # data = file_name


            k = pyDes.des("DESCRYPT", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

            d = k.encrypt(file_contents)

            print
            "Encrypted: %r" % d

            my_file.close()

            my_file = open(file_name, "w")

            my_file.write(d)

            conn.put_object(cont_name, file_name, contents=upload_file.read())

        print("file uploaded")
        '''print("enter username:")
        input=raw_input()
        var1="file_name"
        var2="input"
        file_name=var1+var2'''

    elif input == "2":
        '''print("enter size in KB:")
        input1=raw_input()'''

        print("nObject List:")

        for container in conn.get_account()[1]:

            for data in conn.get_container(container['name'])[1]:
                # if data['bytes']>"input1":


                print
                'file: {0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])

    elif input == "3":

        print
        "Enter a filename:",

        file_name = raw_input()

        obj = conn.get_object(cont_name, file_name)

        with open(file_name, 'w+') as my_example:

            my_example.write(obj[1])

            print
            "File %s downloaded successfully." % file_name

    elif input == "4":

        print
        "Enter a filename:",

        file_name = raw_input()
        # extension=os.path.splittext(file_name)


        conn.delete_object(cont_name, file_name)

        print
        "File %s deleted successfully." % file_name




    elif input == "5":

        print("enter file name:")

        file_name = raw_input()

        obj1 = conn.get_object(cont_name, file_name)

        with open(file_name, 'w+') as my_example:

            my_example.write(obj1[1])

            print
            "Reading the file %s...." % file_name

        if os.path.exists(file_name):

            with open(file_name, 'r') as f:

                print(f.read())

        else:

            print("file doesnt exist on the cloud")
