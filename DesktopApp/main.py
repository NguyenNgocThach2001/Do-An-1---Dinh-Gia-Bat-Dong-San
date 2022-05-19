from cProfile import label
import csv
from tkinter import *
from PIL import ImageTk, Image
import sys
sys.path.insert(0, 'Do-An-1---Dinh-Gia-Bat-Dong-San\Selenium_Crawl')
from Scrape_Page import Crawl_Page
from Scrape_Data import Crawl_Data 
import sys
sys.path.insert(0, 'Do-An-1---Dinh-Gia-Bat-Dong-San\PrepareData')
from FillMissingData import FillMissing
from RemoveErrorRow import RemoveError
from TXT2CSV import TXT2CSV
import sys
sys.path.insert(0, 'Do-An-1---Dinh-Gia-Bat-Dong-San\Regression')
from Regression import Predicts

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter
from tkinter import END, Entry, font
from tkinter import messagebox
import tkinter.ttk

from matplotlib.pyplot import text

__version__ = "1.1"

# I may have broken the unicode...
tkinter_umlauts=['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']

class AutocompleteEntry(tkinter.Entry):
        """
        Subclass of tkinter.Entry that features autocompletion.

        To enable autocompletion use set_completion_list(list) to define
        a list of possible strings to hit.
        To cycle through hits use down and up arrow keys.
        """
        def set_completion_list(self, completion_list):
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)

        def autocomplete(self, delta=0):
                """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()):  # Match case-insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,tkinter.END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,tkinter.END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(tkinter.INSERT), tkinter.END)
                        self.position = self.index(tkinter.END)
                if event.keysym == "Left":
                        if self.position < self.index(tkinter.END): # delete the selection
                                self.delete(self.position, tkinter.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, tkinter.END)
                if event.keysym == "Right":
                        self.position = self.index(tkinter.END) # go to end (no selection)
                if event.keysym == "Down":
                        self.autocomplete(1) # cycle to next hit
                if event.keysym == "Up":
                        self.autocomplete(-1) # cycle to previous hit
                if len(event.keysym) == 1 or event.keysym in tkinter_umlauts:
                        self.autocomplete()

class AutocompleteCombobox(tkinter.ttk.Combobox):

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,tkinter.END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,tkinter.END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(tkinter.INSERT), tkinter.END)
                        self.position = self.index(tkinter.END)
                if event.keysym == "Left":
                        if self.position < self.index(tkinter.END): # delete the selection
                                self.delete(self.position, tkinter.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, tkinter.END)
                if event.keysym == "Right":
                        self.position = self.index(tkinter.END) # go to end (no selection)
                if len(event.keysym) == 1:
                        self.autocomplete()
                # No need for up/down, we'll jump to the popup
                # list at the position of the autocompletion


DSQH = ('Thành Phố Thủ Đức', 'Quận 1', 'Quận 2', 'Quận 3', 'Quận 4', 'Quận 5', 'Quận 6', 'Quận 7',
        'Quận 8', 'Quận 9', 'Quận 10', 'Quận 11', 'Quận 12', 'Quận Bình Tân',
        'Quận Bình Thạnh', 'Quận Gò Vấp', 'Quận Phú Nhuận', 'Quận Tân Bình',
        'Quận Tân Phú', 'Huyện Bình Chánh', 'Huyện Cần Giờ', 'Huyện Củ Chi',
        'Huyện Hóc Môn', 'Huyện Nhà Bè')

"""Run a mini application to test the AutocompleteEntry Widget."""
root = tkinter.Tk(className=' Định Giá Bất Động Sản')
root.resizable(False, False)
ws = root.winfo_screenwidth() 
hs = root.winfo_screenheight() 
w = 700
h = 700
x = (ws/2) - (w/2)
y = (hs/2) - (h/2) - 25
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

top_left_frame_container = tkinter.Frame(root, width=700, height=200)
top_left_frame_container.pack_propagate(0)
middle_left_frame_container = tkinter.Frame(root, width=700, height=300)
middle_left_frame_container.pack_propagate(0)
bottom_left_frame_container = tkinter.Frame(root, width=700, height=200)
bottom_left_frame_container.pack_propagate(0)

root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=0)

top_left_frame_container.grid(row = 0)
middle_left_frame_container.grid(row = 1)
bottom_left_frame_container.grid(row = 2)




wrapperCrawl = tkinter.LabelFrame(top_left_frame_container, text="Cào dữ liệu", width = 700)
wrapperCrawl.pack(fill = BOTH, padx = 10, pady=10)

frame1 = tkinter.Frame(wrapperCrawl)            
frame1.pack(side = tkinter.TOP, fill = BOTH)
frame2 = tkinter.Frame(wrapperCrawl)            
frame2.pack(side = tkinter.TOP, fill = BOTH)
frame3 = tkinter.Frame(wrapperCrawl)            
frame3.pack(side = tkinter.TOP, fill = BOTH)
frame4 = tkinter.Frame(wrapperCrawl)            
frame4.pack(side = tkinter.TOP, fill = BOTH)
frame5 = tkinter.Frame(wrapperCrawl)            #Crawl Btn
frame5.pack(side = tkinter.TOP, fill = BOTH)

wrapperData = tkinter.LabelFrame(middle_left_frame_container, text = "Dữ Liệu", width=700)
wrapperData.pack(fill = BOTH, padx = 10, pady=10)

wrapperPredict = tkinter.LabelFrame(bottom_left_frame_container, text = "Nhập và định giá bất động sản", width=700)
wrapperPredict.pack(fill = BOTH, padx = 10, pady=10)
frame11 = tkinter.Frame(wrapperPredict)
frame11.pack(side = tkinter.BOTTOM, fill="both")
frame6 = tkinter.Frame(wrapperPredict)
frame6.pack(side = tkinter.TOP, fill="both")
frame7 = tkinter.Frame(wrapperPredict)
frame7.pack(side = tkinter.TOP, fill="both")
frame8 = tkinter.Frame(wrapperPredict)
frame8.pack(side = tkinter.TOP, fill="both")
frame9 = tkinter.Frame(wrapperPredict)
frame9.pack(side = tkinter.TOP, fill="both")   
frame10 = tkinter.Frame(wrapperPredict)
frame10.pack(side = tkinter.TOP, fill="both")


l1 = tkinter.Label(frame1, text = "Thành Phố: ", font="TimesNewRoman 15 bold")
l1.pack(side = tkinter.LEFT)
combo = AutocompleteCombobox(frame1, font="TimesNewRoman 20 bold")
combo.set_completion_list(DSQH)
combo.insert(END, 'Thành Phố Thủ Đức')
combo.pack(side = tkinter.LEFT, padx = 30)


l2 = tkinter.Label(frame2, text = "Giá (tỷ): ", font="TimesNewRoman 15 bold")
l2.pack(side = tkinter.LEFT)
entry1 = tkinter.Entry (frame2, width=5) 
entry1.insert(END, '0')
entry1.pack(side = tkinter.LEFT, padx = (63, 0))
l3 = tkinter.Label(frame2, text = "đến", font="TimesNewRoman 15 bold")
l3.pack(side = tkinter.LEFT)
entry2 = tkinter.Entry (frame2, width=5) 
entry2.insert(END, '100')
entry2.pack(side = tkinter.LEFT)

l4 = tkinter.Label(frame3, text = "Diện tích (m2): ", font="TimesNewRoman 15 bold")
l4.pack(side = tkinter.LEFT)
entry3 = tkinter.Entry (frame3, width=5) 
entry3.insert(END, '0')
entry3.pack(side = tkinter.LEFT, padx = 1)
l5 = tkinter.Label(frame3, text = "đến", font="TimesNewRoman 15 bold")
l5.pack(side = tkinter.LEFT)
entry4 = tkinter.Entry (frame3, width=5) 
entry4.insert(END, '100')
entry4.pack(side = tkinter.LEFT)

l6 = tkinter.Label(frame4, text = "Số dữ liệu lấy: ", font="TimesNewRoman 15 bold")
l6.pack(side = tkinter.LEFT)
entry5 = tkinter.Entry (frame4, width=10) 
entry5.insert(END, '100')
entry5.pack(side = tkinter.LEFT, padx = 3)

def CrawlData():
    messagebox.showinfo("Thành Phố", str(combo.get()))
    messagebox.showinfo("Giá", "Giá từ " + str(entry1.get()) + " đến " + str(entry2.get()))
    messagebox.showinfo("Diện tích", "Diện tích từ " + str(entry3.get()) + " đến " + str(entry4.get()))
    messagebox.showinfo("Lấy dữ liệu trang", "")
    Crawl_Page(combo.get(), int(entry5.get()))
    # messagebox.showinfo("Lấy dữ liệu từng trang", "")
    print("Lấy dữ liệu từng trang")
    Crawl_Data()
    # messagebox.showinfo("Xóa dữ liệu lỗi", "")
    print("Xóa dữ liệu lỗi")
    RemoveError()
    # messagebox.showinfo("Chuyển thành TXT", "")
    print("Chuyển thành TXT")
    TXT2CSV()
    # messagebox.showinfo("Điền dữ liệu khuyết", "")
    print("Điền dữ liệu khuyết")
    FillMissing(int(float(entry2.get())), int(float(entry4.get())))
    print("Xong")

submitBtn = tkinter.Button(frame5, text='Crawl Data', command=CrawlData, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
submitBtn.pack(side = tkinter.TOP)

class TreeVieww:
    def __init__(self, root, lst):
        trv = tkinter.ttk.Treeview(root,selectmode='browse', columns=(1,2,3,4,5,6), show="headings", height = "12")
        trv.pack(side = 'left')
        vsb = tkinter.ttk.Scrollbar(root, orient="vertical", command=trv.yview)
        vsb.pack(side='right', fill=BOTH)
        trv.configure(yscrollcommand=vsb.set)
        trv.heading(1, text="STT")
        trv.heading(2, text="Giá")
        trv.heading(3, text="Diện tích")
        trv.heading(4, text="Số Phòng Ngủ")
        trv.heading(5, text="Số Toilet")
        trv.heading(6, text="Số tầng")
        trv.column("# 1", width = 30)
        trv.column("# 2", width = 125)
        trv.column("# 3", width = 125)
        trv.column("# 4", width = 125)
        trv.column("# 5", width = 125)
        trv.column("# 6", width = 125)
        for row in lst[1:]:
            trv.insert('', 'end', values = row)
        

def createTable(): 
    with open("Dataset.csv", newline = "") as file:
        reader = csv.reader(file)
        data = [tuple(row) for row in reader]
        lst = []
        for row in data:
            lst.append(row)
        t = TreeVieww(wrapperData, lst)   

l7 = tkinter.Label(frame7, text = "Diện Tích (m2): ", font="TimesNewRoman 15 bold")
l7.pack(side = tkinter.LEFT)
entry6 = tkinter.Entry (frame7) 
entry6.insert(END, '100')
entry6.pack(side = tkinter.LEFT)

l8 = tkinter.Label(frame8, text = "Số Phòng Ngủ: ", font="TimesNewRoman 15 bold")
l8.pack(side = tkinter.LEFT)
entry7 = tkinter.Entry (frame8) 
entry7.insert(END, '3')
entry7.pack(side = tkinter.LEFT, padx = 2)

l9 = tkinter.Label(frame9, text = "Số Toilet: ", font="TimesNewRoman 15 bold")
l9.pack(side = tkinter.LEFT)
entry8 = tkinter.Entry (frame9) 
entry8.insert(END, '5')
entry8.pack(side = tkinter.LEFT, padx = 54)

l10 = tkinter.Label(frame10, text = "Số tầng: ", font="TimesNewRoman 15 bold")
l10.pack(side = tkinter.LEFT)
entry9 = tkinter.Entry (frame10) 
entry9.insert(END, '3')
entry9.pack(side = tkinter.LEFT, padx = 65)

root.bind('<Control-Q>', lambda event=None: root.destroy())
root.bind('<Control-q>', lambda event=None: root.destroy())

def openNewWindow(plot, root, resultStr1,resultStr2,resultStr3,resultStr4):
    newWindow = Toplevel(root)
    newWindow.title("New Window")
    w = 1200
    h = 900
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2) - 25
    newWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
    newWindowFrame1 = tkinter.Frame(newWindow)
    newWindowFrame1.pack(side = 'top')
    resultLabel1 = tkinter.Label(newWindowFrame1, text = resultStr1,  font="TimesNewRoman 15 bold")
    resultLabel1.pack(side = 'left')
    resultLabel2 = tkinter.Label(newWindowFrame1, text = resultStr2 + "(RT)",  font="TimesNewRoman 15 bold", fg='#FFCC00')
    resultLabel2.pack(side = 'left')
    resultLabel3 = tkinter.Label(newWindowFrame1, text = resultStr3,  font="TimesNewRoman 15 bold")
    resultLabel3.pack(side = 'left')
    resultLabel4 = tkinter.Label(newWindowFrame1, text = resultStr4 + " (MLR)",  font="TimesNewRoman 15 bold", fg = "#FF0000")
    resultLabel4.pack(side = 'left')
    newWindowFrame2 = tkinter.Frame(newWindow)
    newWindowFrame2.pack(side = 'top')
    img1 = Image.open('IMG1.PNG')
    img1 = img1.resize((600,400), Image.ANTIALIAS)
    img1 = ImageTk.PhotoImage(img1)
    label1 = Label(newWindowFrame2, image = img1)
    label1.image = img1
    label1.grid(row=0, column = 0)
    img2 = Image.open('img2.PNG')
    img2 = img2.resize((600,400), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)
    label2 = Label(newWindowFrame2, image = img2)
    label2.image = img2
    label2.grid(row=0, column = 1)
    img3 = Image.open('img3.PNG')
    img3 = img3.resize((600,400), Image.ANTIALIAS)
    img3 = ImageTk.PhotoImage(img3)
    label3 = Label(newWindowFrame2, image = img3)
    label3.image = img3
    label3.grid(row=1, column = 0)
    img4 = Image.open('img4.PNG')
    img4 = img4.resize((600,400), Image.ANTIALIAS)
    img4 = ImageTk.PhotoImage(img4)
    label4 = Label(newWindowFrame2, image = img4)
    label4.image = img4
    label4.grid(row=1, column = 1)
    newWindow.mainloop()

def Predict():
    print("Predict")
    New_Data = [[[int(float(entry6.get())),int(float(entry7.get())),int(float(entry8.get())),int(float(entry9.get()))]]]
    plot, resultStr1, resultStr2, resultStr3, resultStr4 = Predicts(New_Data) 
    openNewWindow(plot, root, resultStr1, resultStr2,resultStr3,resultStr4)

def Startup():
    createTable()

predictBtn = tkinter.Button(frame11, text = 'Predict', command= Predict,  bg='brown', fg='white', font=('helvetica', 9, 'bold')) 
predictBtn.pack()

Startup()

root.mainloop()

