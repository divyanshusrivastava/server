#! /usr/bin/python3

## COMMENTS BY DIVYANSHU
# BASIC UI COMPONENTS ADDED
# FORMATTING PENDING
# Check real time

from bluetooth import BluetoothSocket, RFCOMM, PORT_ANY, SERIAL_PORT_CLASS, SERIAL_PORT_PROFILE, advertise_service
from pykeyboard import PyKeyboard
from time import sleep
import tkinter
import threading



class gui(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):

        #make my screen dimensions work
        w = 320 #The value of the width
        h = 240 #The value of the height of the window

        # get screen width and height
        ws = self.winfo_screenwidth()#This value is the width of the screen
        hs = self.winfo_screenheight()#This is the height of the screen

        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        #This is responsible for setting the dimensions of the screen and where it is
        #placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.grid_columnconfigure(0,weight=1)
        self.resizable(False,False)
        
        self.grid()

        ## Heading label
        self.labelVariable1 = tkinter.StringVar()
        label1 = tkinter.Label(self,textvariable=self.labelVariable1,anchor='s',font="Helvetica",fg='#FF6600')
        label1.grid(column=0,row=0)
        self.labelVariable1.set("REWAVE SERVER")


        ## Status Label
        self.labelVariable2 = tkinter.StringVar()
        label2 = tkinter.Label(self,textvariable=self.labelVariable2,font="Helvetica",fg='#FF6600')
        label2.grid(column=0,row=1)
        self.labelVariable2.set("Hit Start!")
        

        ## Controlling Button
        self.captionVariable1 = tkinter.StringVar()
        button = tkinter.Button(self,textvariable=self.captionVariable1,command=self.OnButtonClick)
        button.grid(column=0,row=2)
        self.captionVariable1.set("START")
        global flag
        flag=1

        ## Receved data display Label
        self.labelVariable3 = tkinter.StringVar()
        label3 = tkinter.Label(self,textvariable=self.labelVariable3,font="Helvetica",fg='#FF6600')
        label3.grid(column=0,row=3)
        self.labelVariable3.set("..")

    def OnButtonClick(self):
        global flag
        if (flag == 1):     # initially stopped
            self.labelVariable2.set("Service started.. Waiting for clients..")
            self.captionVariable1.set("STOP")
            t = threading.Thread(target=startApp)
            t.start()
            flag = 0;
        else:
            self.labelVariable2.set("Service stopped")
            self.captionVariable1.set("START")
            t=threading.Thread(target=stopApp)
            t.start()
            flag = 1;
                
        
        #print("Button Clicked!!")

    def printData(self, data):
        self.labelVariable3.set(data + "recieved")
        
        
config = {
    'backlog': 5,  # max unsuccesful connect attempts
    'uuid': 'a1a738e0-c3b3-11e3-9c1a-0800200c9a66'
}

k = PyKeyboard()

key_bindings = {
    'left' : k.left_key, 
    'right' : k.right_key,
    'up' : k.up_key,
    'down' : k.down_key
}

class BtServer(object):

    def __init__(self):
        super(BtServer, self).__init__()

        self.socket = BluetoothSocket(RFCOMM)
        self.client = {}

    def start(self):
        # empty host address means this machine
        self.socket.bind(("", PORT_ANY))
        self.socket.listen(config['backlog'])

        self.port = self.socket.getsockname()[1]
        uuid = config['uuid']

        advertise_service(
            self.socket,
            "Rewave Server",
            service_id=uuid,
            service_classes=[uuid, SERIAL_PORT_CLASS],
            profiles=[SERIAL_PORT_PROFILE]
        )

        print('Waiting for connection on RFCOMM channel %d' % self.port)
        self.client['socket'], self.client['info'] = self.socket.accept()
        print("Accepted connection from ", self.client['info'])

    def kill(self):
        self.socket.close()

    def close_connection(self):
        self.client['socket'].close()

    def close_socket(self):
        self.client['socket'] = ""
        self.kill()
        


        
 



##def main():
##
##    S = BtServer()
##    S.start()
##
##
##    while True:
##        try:
##            data = S.client['socket'].recv(2048).decode(encoding='UTF-8')
##
##            if data == "exit":
##                S.close_connection()
##                break
##
##            try:
##                k.tap_key(key_bindings[data])
##            except KeyError:
##                pass
##
##            print(data)
##            sleep(0.0006)
##
##        except IOError:
##            pass
##
##        except KeyboardInterrupt:
##            break
##
##    S.kill()


def startApp():
    global S
    S = BtServer()
    S.start()


    while True:
        try:
            data = S.client['socket'].recv(2048).decode(encoding='UTF-8')

            if data == "exit":
                S.close_connection()
                break

            try:
                # NO KEY-TAPPING RIGHT NOW
                # k.tap_key(key_bindings[data])
                gui.printData(data)
            except KeyError:
                pass

            print(data)
            sleep(0.0006)

        except IOError:
            pass

        except KeyboardInterrupt:
            break

def stopApp():
    global S
    S.close_socket()

if __name__ == '__main__':
    
    app = gui(None)
    app.title('REWAVE SERVER')
    app.mainloop()
    #main()
