import time
import threading
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
from PIL import ImageTk,Image

class GUI(threading.Thread):
    def __init__(self):
        self.root = tk.Tk() #set the root to place widgets in
        self.root.state("zoomed") #set window to full screen

        threading.Thread.__init__(self) #define threading
        
        self.key = get_random_bytes(32) #generate the random 32 bit key
        self.plaintext = "HelloWorld" #field for the plaintext (default is HelloWorld)
        self.padding = "" #field for padded version of the plaintext
        self.ciphertext = "" #field for the ciphertext
        self.blocks = [] #field for list of blocks

        self.Page1() #make page 1
        self.root.mainloop() #run

    def Page1(self):
        def GetPlaintext(): #method to get plaintext from input box
            if (entry.get() != ""): #if the user doesnt input any text use the default HelloWorld
                self.plaintext = entry.get()

        def Destroy(): #destroy all widgets on page
            titleLabel.destroy()
            enterLabel.destroy()
            entry.destroy()
            nextButton.destroy()
        #POA title
        titleLabel = tk.Label(self.root, text = "Padding Oracle Attack", font = 'Helvetica 40 bold')
        titleLabel.place(x = 20, y = 20)

        description = "The padding oracle attack (POA) is a form of attack on CBC encryption. It exploits the fact that padding has been added to plaintext before encyrption to reveal information about the ciphertext."
        #enter text label
        enter = "\nEnter plaintext:"
        enterLabel = tk.Label(self.root, text = description+enter, font = "Helvetica 12")
        enterLabel.place(x = 20, y = 110)
        #entry box
        entry = tk.Entry(self.root)
        entry.place(x = 20, y = 210,  height = 200, width = 1500)
        #next button
        nextButton = tk.Button(self.root, text = "Start", command = lambda: [GetPlaintext(), Destroy(), self.Page2()])
        nextButton.place(x = 750, y = 510)

    def Page2(self):
        def Destroy(): #destroy all widgets on page
            ptLabel.destroy()
            ptText.destroy()
            pdLabel.destroy()
            pdText.destroy()
            ctLabel.destroy()
            ctText.destroy()
            infoButton.destroy()
            nextButton.destroy()
            backButton.destroy()
        #plaintext label
        ptLabel = tk.Label(self.root, text = "Plaintext:", font = "Helvetica 15")
        ptLabel.place(x = 20, y = 20) 
        #textbox to display the plaintext
        ptText = tk.Text(self.root)
        ptText.insert(tk.END, self.plaintext)
        ptText.place(x = 20, y = 50, width = 1000, height = 50)
        #pad the plaintext using the PyCrypto method
        self.padding = pad(bytes(self.plaintext, encoding = "utf8"), AES.block_size)
        #padding label
        pdLabel = tk.Label(self.root, text = "Plaintext with Padding:", font = "Helvetica 15")
        pdLabel.place(x = 20, y = 130) 
        #textbox to display the padded plaintext
        pdText = tk.Text(self.root)
        pdText.insert(tk.END, str(self.padding)[2:-1])
        pdText.place(x = 20, y = 160, width = 1000, height = 50)
        #make the cipher using the PyCrypto method
        self.cipher = AES.new(self.key, AES.MODE_CBC)
        #encrypt the padded plaintext
        self.ciphertext = self.cipher.encrypt(self.padding)
        #label for ciphertext
        ctLabel = tk.Label(self.root, text = "Ciphertext:", font = "Helvetica 15")
        ctLabel.place(x = 20, y = 240) 
        #textbox to display ciphertext
        ctText = tk.Text(self.root)
        ctText.insert(tk.END, str(self.ciphertext)[2:-1])
        ctText.place(x = 20, y = 270, width = 1000, height = 50)
        #button to take user to the information page
        infoButton = tk.Button(self.root, text = "Information", command = lambda: [Destroy(), self.PageInfo1()])
        infoButton.place (x = 1100, y = 20)
        #button to take user to the next Page
        nextButton = tk.Button(self.root, text = "Next", command = lambda: [Destroy(), self.Page3()])
        nextButton.place(x = 1100, y = 330)
        #button to take user to the previous page
        backButton = tk.Button(self.root, text = "Back", command = lambda: [Destroy(), self.Page1()])
        backButton.place(x = 20, y = 330)

    def PageInfo1(self): #page to describe CBC and padding
        def Destroy():
            cbctitle.destroy()
            cbcLabel.destroy()
            encImg.destroy()
            decodeImg.destroy()
            pdTitle.destroy()
            pdLabel.destroy()
            backButton.destroy()
        #CBC title label
        cbctitle = tk.Label(self.root, text = "CBC Encryption", font = "Helvetica 18 bold")
        cbctitle.place(x = 20, y = 20)
        #label for info about CBC
        cbcText = "Cipher Block Chaining (CBC) is a type of block cipher, which means it is applied to a plaintext that is separated into even blocks.\nFirst the plaintext is split into equal length blocks (typically 16 bits). The first block is then exclusively OR’ed (XOR’ed) with a randomly generated block called the initialisation vector (IV). Each subsequent block is then XOR’ed with the previous block of ciphertext and is then encryption.\nDecryption works in the reverse order. After decrypting the last block of ciphertext, the result is XOR'd with the previous block of ciphertext to recover the original plaintext."
        cbcLabel = tk.Label(self.root,  wraplength = 1000, justify = "left", font = "Helvetica 12", text = cbcText)
        cbcLabel.place(x = 20, y = 60)
        #diagrams for cbc encryption and decryption
        cbcenc = Image.open("CBCENC.png")
        img1 = ImageTk.PhotoImage(cbcenc)
        encImg = tk.Label(image=img1)
        encImg.image = img1
        encImg.place(x=20, y=200)

        cbcdec = Image.open("CBCDEC.png")
        img2 = ImageTk.PhotoImage(cbcdec)
        decodeImg = tk.Label(image=img2)
        decodeImg.image = img2
        decodeImg.place(x= 700, y=200)

        #padding title
        pdTitle = tk.Label(self.root, text = "Padding", font = "Helvetica 18 bold")
        pdTitle.place(x = 20, y = 500)
        #padding description
        pdText = "If a message cannot be split into equal sized blocks padding is added. The common method of padding is PKCS7 where the value of each padded byte is the same as the number of bytes of padding. For example, if a block is 12 characters, 4 bytes need to be added to reach the block size of 16, so [04, 04, 04, 04] is added."
        pdLabel = tk.Label(self.root,  wraplength = 1000, justify = "left", font = "Helvetica 12", text = pdText)
        pdLabel.place(x = 20, y = 540)
        #button to take user back to Page2
        backButton = tk.Button(self.root, text = "Back", command = lambda: [Destroy(), self.Page2()])
        backButton.place(x = 20, y = 650)

    def Page3(self):
        def Destroy():
            blockTitle.destroy()
            blockLabel.destroy()
            block2Label.destroy()
            backButton.destroy()
            blockBox.destroy()
            for i in buttons:
                i.destroy()

        if len(self.blocks) == 0:
            self.SeperateBlocks()
        
        blockTitle = pdLabel = tk.Label(self.root, text = "Seperate the Ciphertext into Blocks:", font = "Helvetica 15 bold")
        blockTitle.place(x = 20, y = 20)

        blockText = "When encrypting, the message has to be split up into blocks. Each block is XOR’ed with the previous block. Therefore, when performing a padding oracle attack the attacker will perform the attack in block pairs."
        blockLabel = tk.Label(self.root,  wraplength = 1000, justify = "left", font = "Helvetica 12", text = blockText)
        blockLabel.place(x = 20, y = 60)
        
        block2Text = "This ciphertext is split into "+str(len(self.blocks))+" blocks with C0 being the IV:"
        block2Label = tk.Label(self.root,  wraplength = 1000, justify = "left", font = "Helvetica 12", text = block2Text)
        block2Label.place(x = 20, y = 100)

        blockBox = tk.Text(self.root)
        for i in range (len(self.blocks)):
           blockBox.insert(tk.END, "\nC"+str(i)+": "+str(self.blocks[i])) 
        blockBox.place(x = 20, y = 150, width = 1000, height = 100)

        self.my_str = tk.IntVar()
        self.searchBit = 15
        self.ivValues = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.message = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        buttons = []
        for i in range(len(self.blocks)-1):
            buttons.append(tk.Button(self.root, text = "Run for C"+str(i+1), command = lambda k=i: [Destroy(), run(k), self.Page4()]))
            buttons[i].place(x = 20+i*100, y = 300)

        backButton = tk.Button(self.root, text = "Back", command = lambda: [Destroy(), self.Page2()])
        backButton.place(x = 20, y = 370)

        def run(k):
            self.my_str.set(k)

    def Page4(self):
        i = self.my_str.get()
        iv = self.blocks[i]
        block = self.blocks[i+1]

        def destroy():
            ivLabel.destroy()
            ivplace.destroy()
            blockLabel.destroy()
            blockPlace.destroy()
            diagram.destroy()
            padLabel.destroy()
            ptLabel.destroy()
            blockInfo.destroy()
            infolabel.destroy()
            runButton.destroy()
            nextButton.destroy()

        def reset():
            self.possible = 0
            self.var2.set("INCORRECT PADDING")
            self.var3.set("")

        self.var = tk.StringVar()
        self.var2 = tk.StringVar()
        self.var3 = tk.StringVar()
        self.possible = 0
        self.result = 0

        self.knowniv = ["X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X"]
        self.knownpt = ["X","X","X","X","X","X","X","X","X","X","X","X","X","X","X","X"]

        string = ""
        if (AES.block_size - self.searchBit) > 9:
            string = "0x"+str(AES.block_size - self.searchBit)
        else:
            string = "0x0"+str(AES.block_size - self.searchBit)

        for j in range(AES.block_size - self.searchBit):
            print(AES.block_size-1-j)
            self.knownpt[AES.block_size-1-j] = string

        
        for x in range(AES.block_size - self.searchBit - 1):
            val = (AES.block_size - self.searchBit) ^ iv[AES.block_size-x-1] ^ self.message[AES.block_size-x-1]
            self.knowniv[AES.block_size - x -1] = str(val)

        self.var.set(str(self.knowniv))
        self.GetBit(iv, block, self.searchBit, False)

        ivLabel = tk.Label(self.root, text = "C"+str(i), font = "Helvetica 12")
        ivLabel.place(x = 110, y = 30)
        ivplace = tk.Label(self.root, textvariable = self.var, font  = "Helvetica 12")
        ivplace.place(x = 20, y = 60)

        blockLabel = tk.Label(self.root, text = "C"+str(i+1), font = "Helvetica 12")
        blockLabel.place(x = 900, y = 30)
        blockPlace = tk.Label(self.root, text = "".join(str(block)),font = "Helvetica 12")
        blockPlace.place(x= 700, y = 60)

        toHelp = Image.open("MP.png")
        img1 = ImageTk.PhotoImage(toHelp)
        diagram = tk.Label(image = img1)
        diagram.image = img1
        diagram.place(x=120, y = 100)

        self.var2.set("INCORRECT PADDING")

        padLabel = tk.Label(self.root, textvariable = self.var2, font = "Helvetica 12")
        padLabel.place(x = 620, y = 320)

        info ="C"+str(i)+": "+str(iv)+"\nC"+str((i+1))+": "+str(block)
        blockInfo = tk.Label(self.root, wraplength = 900, justify = "left", font = "Helvetica 12", text = info)
        blockInfo.place(x = 100, y = 410)

        infoText = "After reciveing a ciphertext, the server will decrypt the block then XOR it with the ciphertext of the previous block. The attacker will iterate through every value (apart from the original value) for the last byte of the block until the padding format is correct. This means that the plaintext result for the modified ciphertext is 0x01. The attacker can then use this knowledge to calculate the original plaintext value.\nAfter obtaining the last byte the attacker can repeat the same method on the next bit, setting the last byte of the plaintext to 0x02. Then modifies the second to last bit until the padding is correct at (0x02, 0x02)."
        infolabel = tk.Label(self.root, wraplength = 900, justify = "left", font = "Helvetica 12", text = infoText)
        infolabel.place(x = 100, y = 500)

        self.var3.set("")
        ptLabel = tk.Label(self.root, textvariable = self.var3, font = "Helvetica 12")
        ptLabel.place(x = 480, y = 360)

        runButton = tk.Button(self.root, text='Run ', command= lambda: [reset(), self.change_value_callback(iv, block, self.searchBit)])
        runButton.place(x = 1100, y = 510)

        nextButton = tk.Button(self.root, text = "Next", command = lambda: [destroy(), self.Page5(iv, block)])
        nextButton.place(x = 1100, y = 550)

    def Page5(self, iv, block):
        def Destroy():
            part1Label.destroy()
            part1Text.destroy()
            part2Label.destroy()
            part2Text.destroy()
            part3Label.destroy()
            part3Text.destroy()
            part4Label.destroy()
            part4Text.destroy()
            part5Label.destroy()
            part5Text.destroy()
            backButton.destroy()
            nextButton.destroy()
            blockButton.destroy()
            message.destroy()
            messageBox.destroy()

        def MoveNext():
            self.searchBit-=1
            self.Page4()

        def SelectNewBlock():
            self.searchBit = 15
            self.Page3()

        part1 ="Now knowing the combination of bits that make the padding value, the attacker can calculate the original plaintext.\nThe formula for decrypting the ciphertext is:"
        part1Label = tk.Label(self.root,  wraplength = 1000, justify = "left", font = "Helvetica 12", text = part1)
        part1Label.place(x = 20, y = 20)
        part1Text = tk.Text(self.root)
        part1Text.insert(tk.END, "\n\t  Pi = D(Ci) XOR Ci-1")
        part1Text.place(x = 60, y = 70, width = 330, height = 50)

        part2 = "By rearranging this formula to:"
        part2Label = tk.Label(self.root,  wraplength = 1000, justify = "left", font = "Helvetica 12", text = part2)
        part2Label.place(x = 20, y = 130)
        part2Text = tk.Text(self.root)
        part2Text.insert(tk.END, "\n\t  D(Ci) = Pi XOR Ci-1")
        part2Text.place(x = 60, y = 160, width = 330, height = 50)

        part3 = "This can be inserted into the formula for decrypting the modified ciphertext to replace the unknown D(Ci):"
        part3Label = tk.Label(self.root,  wraplength = 1000, justify = "left", font = "Helvetica 12", text = part3)
        part3Label.place(x = 20, y = 220)
        part3Text = tk.Text(self.root)
        part3Text.insert(tk.END, "\n\t  Pi’ = D(Ci) XOR Ci-1’")
        part3Text.insert(tk.END, "\n       Pi’ = Pi XOR Ci-1 XOR Ci-1’")
        part3Text.place(x = 60, y = 250, width = 330, height = 70)

        part4 = "From there, rearranging gives the final formula for the plaintext bit as:"
        part4Label = tk.Label(self.root,  wraplength = 1000, justify = "left", font = "Helvetica 12", text = part4)
        part4Label.place(x = 20, y = 330)
        part4Text = tk.Text(self.root)
        part4Text.insert(tk.END, "\n       Pi = Pi’ XOR Ci-1 XOR Ci-1’")
        part4Text.place(x = 60, y = 360, width = 330, height = 50)

        part5 = "Substituting the known values into the equation gives us the value of the plaintext:"
        part5Label = tk.Label(self.root,  wraplength = 1000, justify = "left", font = "Helvetica 12", text = part5)
        part5Label.place(x = 20, y = 420)
        part5Text = tk.Text(self.root)

        ans = 1 ^ self.possible ^ iv[self.searchBit]

        string = ""
        if (AES.block_size - self.searchBit) > 9:
            string = "0x"+str(AES.block_size - self.searchBit)
        else:
            string = "0x0"+str(AES.block_size - self.searchBit)

        eq = "\n       "+string+" XOR "+str(self.possible)+" XOR "+str(iv[self.searchBit])+ " = "+str(ans)
        part5Text.insert(tk.END, eq)
        part5Text.place(x = 60, y = 450, width = 330, height = 50)

        print(bytes(self.message))

        message = tk.Label(self.root,  wraplength = 1000, justify = "left", font = "Helvetica 12", text = "The plaintext as known:")
        message.place(x = 20, y = 510)

        messageBox = tk.Text(self.root)
        string = bytes(self.message)
        messageBox.insert(tk.END, "\n   "+str(string))
        messageBox.place(x = 60, y = 540, width = 1000, height = 50)

        backButton = tk.Button(self.root, text = "Repeat Bit", command = lambda: [Destroy(), self.Page4()])
        backButton.place(x = 20, y = 600)

        nextButton = tk.Button(self.root, text = "Move to Next Bit", command = lambda: [Destroy(), MoveNext()])
        if self.searchBit != 0:
            nextButton.place(x = 100, y = 600)

        blockButton = tk.Button(self.root, text = "Select New Block", command = lambda: [Destroy(), SelectNewBlock()])
        blockButton.place(x = 220, y = 600)

        



    def SeperateBlocks(self):
        self.blocks.append(list(self.cipher.iv)) #add the iv to the list of blocks as it is C0
        listin = [] #make a blank list to contain the next block
        bitCount = 1 #count the number of bits
        for i in list(self.ciphertext): #loop through the ciphertext and seperate it into blocks
            if bitCount == 17: #if the number of bits is 17 then the block is full
                bitCount = 1 #reset the bit count
                self.blocks.append(listin) #add the block to the list
                listin = [] #start a new block
            listin.append(i) #add the bit to the block
            bitCount+=1 #increment the count
        self.blocks.append(listin) #add the last block to the list

    def change_value_callback(self, iv, block, find):
        th = threading.Thread(target= lambda: self.GetBit(iv, block, find, True), args=())
        th.start()

    def GetBit(self, iv, block, find, sleep):
        ivcopy = iv.copy()

        bitIV = bytes(iv)
        bitBlock = bytes(block)

        while True:
            if sleep:
                time.sleep(0.05)
            try:
                if self.possible == bitIV[find]:
                    self.possible+=1

                if sleep:
                    self.knowniv[find] = " "+str(self.possible)
                    self.var.set(str(self.knowniv))

                ivcopy[find] = self.possible
                cipher2 = AES.new(self.key, AES.MODE_CBC, iv = bytes(ivcopy))
                decrypt = list(cipher2.decrypt(bitBlock))
                for i in range(AES.block_size - (find+1)):
                    decrypt.pop()

                plain = unpad(bytes(decrypt), find+1)

            except (ValueError) :
                self.possible += 1
            else:
                self.var2.set("CORRECT PADDING")
                self.var3.set("Result: "+str(self.knownpt))
                break

        val = 1 ^ self.possible ^ bitIV[find]
        print(val)
        self.result = val 
        self.message[find] = val

if __name__ =='__main__':
    gui = GUI()