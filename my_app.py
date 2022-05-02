# Importing Libraries

from PIL import Image, ImageTk
import tkinter as tk
import cv2
from keras.models import model_from_json
# from keras.models import load_model
import operator
import  os
from string import ascii_uppercase
import enchant
import pyttsx3


##Creating Class


class Application:
    def __init__(self):

        # Setting Up path
        self.directory = os.getcwd() + '\\models\\'
        # initializing Enchant
        self.en = enchant.Dict('en_US')

        #Capturing image
        self.vs = cv2.VideoCapture(0)
        self.current_image = None           #For Process
        self.current_image2 = None          #For Displaying

        #Initializing Some variables
        self.str = ""
        self.word = ""
        self.current_symbol = "Empty"
        self.photo = "Empty"

        # Loading Models
        # black White
        self.json_file = open(self.directory + "model-bw.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()
        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights(self.directory + "model-bw.h5")

        #AMNT
        self.json_file_amnt = open(self.directory + "model-amnt.json", "r")
        self.model_json_amnt = self.json_file_amnt.read()
        self.json_file_amnt.close()
        self.loaded_model_amnt = model_from_json(self.model_json_amnt)
        self.loaded_model_amnt.load_weights(self.directory + "model-amnt.h5")

        #AS
        self.json_file_as = open(self.directory + "model-as.json", "r")
        self.model_json_as = self.json_file_as.read()
        self.json_file_as.close()
        self.loaded_model_as = model_from_json(self.model_json_as)
        self.loaded_model_as.load_weights(self.directory + "model-as.h5")

        #CO
        self.json_file_co = open(self.directory + "model-co.json", "r")
        self.model_json_co = self.json_file_co.read()
        self.json_file_co.close()
        self.loaded_model_co = model_from_json(self.model_json_co)
        self.loaded_model_co.load_weights(self.directory + "model-co.h5")

        #GHP
        self.json_file_ghp = open(self.directory + "model-ghp.json", "r")
        self.model_json_ghp = self.json_file_ghp.read()
        self.json_file_ghp.close()
        self.loaded_model_ghp = model_from_json(self.model_json_ghp)
        self.loaded_model_ghp.load_weights(self.directory + "model-ghp.h5")

        #KV
        self.json_file_kv = open(self.directory + "model-kv.json", "r")
        self.model_json_kv = self.json_file_kv.read()
        self.json_file_kv.close()
        self.loaded_model_kv = model_from_json(self.model_json_kv)
        self.loaded_model_kv.load_weights(self.directory + "model-kv.h5")

        # #IR
        # self.json_file_ir = open(self.directory + "model-ri.json", "r")
        # self.model_json_ir = self.json_file_ir.read()
        # self.json_file_ir.close()
        # self.loaded_model_ir = model_from_json(self.model_json_ir)
        # self.loaded_model_ir.load_weights(self.directory + "model-ri.h5")





        print("Loaded model from disk")

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0
        for i in ascii_uppercase:
            self.ct[i] = 0


        # Creating GUI

        self.root = tk.Tk()
        self.root.title("Sign language to Text Converter")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("1600x800")
        self.root.state('zoomed')

        self.panel = tk.Label(self.root)                                    #Panel for Full Image Coloured
        self.panel.place(x=100, y=10, width=640, height=640)

        self.panel2 = tk.Label(self.root)                                   #Panel2 for BW Image
        self.panel2.place(x=425, y=95, width=310, height=310)

        self.T = tk.Label(self.root)                                        #T Panel for Title
        self.T.place(x=480, y=0)
        self.T.config(text="Sign Language to Text", font=("Comic Sans MS", 40, "bold"),foreground="red")

        self.panel3 = tk.Label(self.root)                                   #Panel3 for Current predicted Letter
        self.panel3.place(x=1200, y=95)

        self.T1 = tk.Label(self.root)                                       #Panel T1 for "Character" hedding
        self.T1.place(x=750, y=95)
        self.T1.config(text="Character :", font=("Courier", 40, "bold"))

        self.panel4 = tk.Label(self.root)                                   #Panel4 for predicted Word
        self.panel4.place(x=950, y=190)

        self.T2 = tk.Label(self.root)                                       #Panel T2 for 'Word' Heading
        self.T2.place(x=750, y=190)
        self.T2.config(text="Word :", font=("Courier", 40, "bold"))

        self.panel5 = tk.Label(self.root)                                   #Panel4 for predicted Sentence
        self.panel5.place(x=1100, y=285)

        self.T3 = tk.Label(self.root)                                       #Panel T3 for 'Sentence' Heading
        self.T3.place(x=750, y=285)
        self.T3.config(text="Sentence :", font=("Courier", 40, "bold"))

        self.T4 = tk.Label(self.root)                                       #Panel T4 for 'Suggestion' Heading
        self.T4.place(x=550, y=575)
        self.T4.config(text="Suggestions", fg="red", font=("Courier", 40, "bold"))

        # Placing Buttons

        self.btcall = tk.Button(self.root,command = self.about,height = 0,width = 0)
        self.btcall.config(text = "About",font = ("Courier",14))
        self.btcall.place(x = 10, y = 0)

        self.sign = tk.Button(self.root, command=self.sign, height=0, width=0)
        self.sign.config(text="Sign", font=("Courier", 14))
        self.sign.place(x=1450, y=0)

        self.suggestionbt=tk.Button(self.root,command=self.suggestion,height=0,width=0)
        self.suggestionbt.config(text='Suggestions',font=("Courier",14))
        self.suggestionbt.place(x=0,y=575)


        self.bt1=tk.Button(self.root, command=self.action1,height = 0,width = 0)
        self.bt1.place(x = 20,y=700)
        # self.bt1.grid(padx = 10, pady = 10)

        self.bt2=tk.Button(self.root, command=self.action2,height = 0,width = 0)
        self.bt2.place(x = 340,y=700)
        # self.bt2.grid(row = 4, column = 1, columnspan = 1, padx = 10, pady = 10, sticky = tk.NW)

        self.bt3=tk.Button(self.root, command=self.action3,height = 0,width = 0)
        self.bt3.place(x = 660,y=700)
        # self.bt3.grid(row = 4, column = 2, columnspan = 1, padx = 10, pady = 10, sticky = tk.NW)

        self.bt4=tk.Button(self.root, command=self.action4,height = 0,width = 0)
        self.bt4.place(x = 980,y=700)
        # self.bt4.grid(row = 4, column = 0, columnspan = 1, padx = 10, pady = 10, sticky = tk.N)

        self.bt5=tk.Button(self.root, command=self.action5,height = 0,width = 0)
        self.bt5.place(x = 1300,y=700)
        # self.bt5.grid(row = 5, column = 1, columnspan = 1, padx = 10, pady = 10, sticky = tk.N)

        self.saybtn = tk.Button(self.root, command=self.say, height=0, width=0)
        self.saybtn.config(text='Say the Sentence', font=("Courier", 14))
        self.saybtn.place(x=225, y=575)

        self.addletter = tk.Button(self.root, command=self.add_let, height=0, width=0)
        self.addletter.config(text='Add', font=("Courier", 14))
        self.addletter.place(x=160, y=575)












        self.video_loop()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.7)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[2].id)
        text = 'Hello I am Sign language recognizer \n lets Start'
        self.engine.say(text)
        self.engine.runAndWait()

    def video_loop(self):
        ok, frame = self.vs.read()
        if ok:
            cv2image = cv2.flip(frame, 1)
            x1 = int(0.5*frame.shape[1])
            y1 = 10
            x2 = frame.shape[1]-10
            y2 = int(0.5*frame.shape[1])
            cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)
            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)
            cv2image = cv2image[y1:y2, x1:x2]
            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),2)
            th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
            ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            self.predict(res)
            self.current_image2 = Image.fromarray(res)
            imgtk = ImageTk.PhotoImage(image=self.current_image2)
            self.panel2.imgtk = imgtk
            self.panel2.config(image=imgtk)
            self.panel3.config(text=self.current_symbol,font=("Courier",50))
            self.panel4.config(text=self.word,font=("Courier",40))
            self.panel5.config(text=self.str,font=("Courier",40))
            self.root.after(30, self.video_loop)

    def predict(self,test_image):
        test_image = cv2.resize(test_image, (128,128))
        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))



        prediction={}
        prediction['blank'] = result[0][0]
        inde = 1
        for i in ascii_uppercase:
            prediction[i] = result[0][inde]
            inde += 1
        #LAYER 1
        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
        self.current_symbol = prediction[0][0]
        #LAYER 2
        #AS
        if(self.current_symbol == 'A' or self.current_symbol == 'S'):
            result_as = self.loaded_model_as.predict(test_image.reshape(1, 128, 128, 1))
            prediction = {}
            prediction['A'] = result_as[0][0]
            prediction['S'] = result_as[0][1]
            prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
            self.current_symbol = prediction[0][0]

        # AMNT
        if(self.current_symbol == 'A' or self.current_symbol == 'M' or self.current_symbol == 'N' or self.current_symbol == 'T'):
            result_amnt = self.loaded_model_amnt.predict(test_image.reshape(1, 128, 128, 1))
            prediction = {}
            prediction['A'] = result_amnt[0][0]
            prediction['M'] = result_amnt[0][1]
            prediction['N'] = result_amnt[0][2]
            prediction['T'] = result_amnt[0][3]
            prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
            self.current_symbol = prediction[0][0]

        #CO
        if(self.current_symbol == 'C' or self.current_symbol == 'O'):
            result_co = self.loaded_model_co.predict(test_image.reshape(1, 128, 128, 1))
            prediction1 = {}
            prediction1['C'] = result_co[0][0]
            prediction1['O'] = result_co[0][1]
            prediction1 = sorted(prediction1.items(), key=operator.itemgetter(1), reverse=True)
            self.current_symbol = prediction1[0][0]

        #GHP
        if (self.current_symbol == 'G' or self.current_symbol == 'H' or self.current_symbol == 'P' ):
            result_ghp = self.loaded_model_ghp.predict(test_image.reshape(1, 128, 128, 1))
            prediction = {}
            prediction['G'] = result_ghp[0][0]
            prediction['H'] = result_ghp[0][1]
            prediction['P'] = result_ghp[0][2]
            prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
            self.current_symbol = prediction[0][0]

        #KV
        if (self.current_symbol == 'K' or self.current_symbol == 'V'):
            result_kv = self.loaded_model_kv.predict(test_image.reshape(1, 128, 128, 1))
            prediction1 = {}
            prediction1['K'] = result_kv[0][0]
            prediction1['V'] = result_kv[0][1]
            prediction1 = sorted(prediction1.items(), key=operator.itemgetter(1), reverse=True)
            self.current_symbol = prediction1[0][0]

        # #IR
        # if (self.current_symbol == 'I' or self.current_symbol == 'R'):
        #     result_ir = self.loaded_model_ir.predict(test_image.reshape(1, 128, 128, 1))
        #     prediction1 = {}
        #     prediction1['I'] = result_ir[0][0]
        #     prediction1['R'] = result_ir[0][1]
        #     prediction1 = sorted(prediction1.items(), key=operator.itemgetter(1), reverse=True)
        #     self.current_symbol = prediction1[0][0]

        if(self.current_symbol == 'blank'):
            for i in ascii_uppercase:
                self.ct[i] = 0
        self.ct[self.current_symbol] += 1
        if(self.ct[self.current_symbol] > 60):
            for i in ascii_uppercase:
                if i == self.current_symbol:
                    continue
                tmp = self.ct[self.current_symbol] - self.ct[i]
                if tmp < 0:
                    tmp *= -1
                if tmp <= 20:
                    self.ct['blank'] = 0
                    for i in ascii_uppercase:
                        self.ct[i] = 0
                    return
            self.ct['blank'] = 0
            for i in ascii_uppercase:
                self.ct[i] = 0
            if self.current_symbol == 'blank':
                if self.blank_flag == 0:
                    self.blank_flag = 1
                    if len(self.str) > 0:
                        self.str += " "
                    self.engine.say(self.word)
                    self.engine.runAndWait()
                    self.str += self.word
                    self.word = ""
            else:
                if(len(self.str) > 16):
                    self.str = ""
                self.blank_flag = 0
                self.word += self.current_symbol

    def action1(self):
        if(len(self.predicts) > 0):
            self.word=""
            self.str+=" "
            self.engine.say(self.predicts[0])
            self.engine.runAndWait()
            self.str+=self.predicts[0]
    def action2(self):
        if(len(self.predicts) > 1):
            self.word=""
            self.str+=" "
            self.engine.say(self.predicts[1])
            self.engine.runAndWait()
            self.str+=self.predicts[1]
    def action3(self):
        if(len(self.predicts) > 2):
            self.word=""
            self.str+=" "
            self.engine.say(self.predicts[2])
            self.engine.runAndWait()
            self.str+=self.predicts[2]
    def action4(self):
        if(len(self.predicts) > 3):
            self.word=""
            self.str+=" "
            self.engine.say(self.predicts[3])
            self.engine.runAndWait()
            self.str+=self.predicts[3]
    def action5(self):
        if(len(self.predicts) > 4):
            self.word=""
            self.str+=" "
            self.engine.say(self.predicts[4])
            self.engine.runAndWait()
            self.str+=self.predicts[4]


    def add_let(self):
        self.word+=self.current_symbol


    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()

    def about(self):

        self.root1 = tk.Toplevel(self.root)
        self.root1.title("About")
        self.root1.protocol('WM_DELETE_WINDOW', self.destructor1)
        self.root1.geometry("620x861")
        self.photo1 = tk.PhotoImage(file="images//about.png")
        self.w1 = tk.Label(self.root1, image=self.photo1)
        self.w1.place(x=0, y=0)


    def sign(self):
        self.root2 = tk.Toplevel(self.root)
        self.root2.title("Sign")
        self.root2.geometry("640x480")
        self.photo2 = tk.PhotoImage(file='images//sign.png')
        self.w2 = tk.Label(self.root2, image=self.photo2)
        self.w2.place(x=0, y=0)


    def suggestion(self):
        self.predicts = self.en.suggest(self.word)
        if (len(self.predicts) > 0):
            self.bt1.config(text=self.predicts[0], font=("Courier", 20))
        else:
            self.bt1.config(text="")
        if (len(self.predicts) > 1):
            self.bt2.config(text=self.predicts[1], font=("Courier", 20))
        else:
            self.bt2.config(text="")
        if (len(self.predicts) > 2):
            self.bt3.config(text=self.predicts[2], font=("Courier", 20))
        else:
            self.bt3.config(text="")
        if (len(self.predicts) > 3):
            self.bt4.config(text=self.predicts[3], font=("Courier", 20))
        else:
            self.bt4.config(text="")
        if (len(self.predicts) > 4):
            self.bt5.config(text=self.predicts[4], font=("Courier", 20))
        else:
            self.bt5.config(text="")


    def say(self):
        self.engine.say(self.str)
        self.engine.runAndWait()


    def destructor1(self):
        print("Closing Application...")
        self.root1.destroy()


print("Starting Application...")
pba = Application()
pba.root.mainloop()

