from Tkinter import *
import random
import tkMessageBox   
from PIL import ImageTk, Image

# set the board
root = Tk(className = "Pokemon 2048")
root.geometry("690x660")
mainframe = Frame(root,borderwidth = 10)

# a list the value shown on the board
Datalist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# a button list generated from the above list.
Buttonlist = [] 

# the next number is randomly chosen from this list.
Newnumlist = [2,4] 


# a dictionary of pictures: value in the list : picture for that list
Picturedic = {0:"1.png", 2:"2.png", 4:"4.png", 8:"8.jpg",16:"16.png", 32:"32.png",64:"64.jpg",128:"128.jpg",256:"256.png",512:"512.png",1024:"1024.jpg",2048:"2048.jpg"}

imagelist =[]
keylist = [0,2,4,8,16,32,64,128,256,512,1024,2048]
for a in keylist:
    imagelist.append(ImageTk.PhotoImage(Image.open(Picturedic[a]).resize((160, 150),Image.ANTIALIAS)))


# initialize the board.
for i in range(16):
    Buttonlist.append(Button(mainframe, width=160, height=150,image=imagelist[0]))
    Buttonlist[i].grid(row = i/4,column = i%4)

# check whether the board can move with the direction indicated by direction parameters
# when two neighbors has the same value or the next number is zero, the board can move.
def CheckMove(a, b, c, index):
    for w in range(1, 4):
        if Datalist[c*index + w*a +b] == Datalist[c*index + a*(w-1)+b]:
            return True
        if Datalist[c*index + w*a +b] != 0 and Datalist[c*index + a*(w-1)+b] == 0:
            return True
    return False

# remove extra space among numbers
def Exchange(a, b, c, index):
    for w in [3,2,1]:
        if Datalist[c*index + w*a +b] == 0:
            continue
        if Datalist[c*index + a*(w-1)+b] == 0:
            j = w
            while (j < 4):
                Datalist[c*index + a*(j-1)+b] = Datalist[c*index + j*a+b]
                Datalist[c*index + j*a+b] = 0
                j=j+1

# When two neighbors has the same value
def Combine(a, b, c, index):
    for w in [0,1,2]:
        if Datalist[c*index + w*a +b] == Datalist[c*index + (w+1)*a +b]:
            Datalist[c*index + w*a +b] = Datalist[c*index + w*a +b] * 2
            Datalist[c*index + (w+1)*a +b] = 0

# move the board
def OneMove(a, b, c, index):
    Exchange(a, b, c, index)
    Combine(a, b, c, index)
    Exchange(a, b, c, index)

# return list_a = [the index for the next input, value of the next input, length()of new space]
# index is randomly chosen from the available space and value is either 2 or 4
def NewImageStatus(Datalist):
    list_a = [0,0,0]
    available_space = []
    for i in range(16):
        if (Datalist[i] == 0):
            available_space.append(i)
    if (len(available_space) == 0):
        list_a = [0,0,0]
    else:
        list_a[0] = random.choice(available_space)
        list_a[1] = random.choice(Newnumlist)
        list_a[2] = len(available_space)     
    
    return list_a
        
        
# after board is changed, update the board        
def Update():
    for i in range(16):
        if (Datalist[i]==0):
            Buttonlist[i].configure(image=imagelist[0])

        if (Datalist[i]==2):
            Buttonlist[i].configure(image=imagelist[1])

        if (Datalist[i]==4):
            Buttonlist[i].configure(image=imagelist[2])

        if (Datalist[i]==8):
            Buttonlist[i].configure(image=imagelist[3])

        if (Datalist[i]==16):
            Buttonlist[i].configure(image=imagelist[4])

        if (Datalist[i]==32):
            Buttonlist[i].configure(image=imagelist[5])
            
        if (Datalist[i]==64):
            Buttonlist[i].configure(image=imagelist[6])
            
        if (Datalist[i]==128):
            Buttonlist[i].configure(image=imagelist[7])
        
        if (Datalist[i]==256):
            Buttonlist[i].configure(image=imagelist[8])

        if (Datalist[i]==512):
            Buttonlist[i].configure(image=imagelist[9])
            
        if (Datalist[i]==1024):
            Buttonlist[i].configure(image=imagelist[10])
            
        if (Datalist[i]==2048):
            Buttonlist[i].configure(image=imagelist[11])

# the game begins with key presses
# events are handled whenever there are key presses             
def UserInput(event):
    global Datalist
    # handle the direction parameters
    if event.keycode == 37:
        a = 1 #left
        b = 0
        c = 4
    if event.keycode == 39:
        a = -1 #right
        b = 3
        c = 4
    if event.keycode == 38:
        a = 4 # up
        b = 0
        c = 1
    if event.keycode == 40:
        a = -4 # down
        b = 12
        c = 1

    # if the board can move, move the board and update the board
    for i in range(4):
        if CheckMove(a, b, c, i):
            OneMove(a, b, c, i)

    # find the information of the current board  
    info_list = NewImageStatus(Datalist)
 
    # if the board is not full, add new number in the list and update the board.
    if info_list[2] is not 0:
        Datalist[info_list[0]] = info_list[1]
        Update()
    
    # check whether the board can move when the current board is full.
    # if not, game over. A message box will be generated.
    if info_list[2] is 0 or info_list[2] is 1:
        x = 0
        for i_index in range(4):
             if CheckMove(1, 0, 4, i_index) is False and CheckMove(-1, 3, 4, i_index) is False \
             and CheckMove(4, 0, 1, i_index) is False and CheckMove(-4, 12, 1, i_index) is False:
                x += 1
        if x is 4:
            tkMessageBox.showinfo('Game Over',"Try again! You will find out the most interesting image at the end.")
            Datalist=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            Update()
            
    # check whether the user is win          
    for i in range(16):
        if (Datalist[i] == 2048):
            tkMessageBox.showinfo("WIN!!!","You Win! You got Henry's image now!")
            Datalist=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            Update()


mainframe.bind('<KeyRelease>', UserInput)
mainframe.pack()
mainframe.focus_set()
root.mainloop()