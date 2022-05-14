from email import message
from math import comb
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


DSQH = ('Bất kỳ', 'Thành Phố Thủ Đức', 'Quận 1', 'Quận 2', 'Quận 3', 'Quận 4', 'Quận 5', 'Quận 6', 'Quận 7',
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
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))


frame1 = tkinter.Frame(root)
frame1.pack(side = tkinter.TOP)

frame2 = tkinter.Frame(root)
frame2.pack(side = tkinter.TOP)

frame3 = tkinter.Frame(root)
frame3.pack(side = tkinter.TOP)

frame4 = tkinter.Frame(root)
frame4.pack(side = tkinter.TOP)

frame5 = tkinter.Frame(root)
frame5.pack(side = tkinter.TOP)

frame6 = tkinter.Frame(root)
frame6.pack(side = tkinter.TOP)

l1 = tkinter.Label(frame1, text = "Thành Phố:       ", font="TimesNewRoman 15 bold")
l1.pack(side = tkinter.LEFT)
combo = AutocompleteCombobox(frame1, font="TimesNewRoman 20 bold")
combo.set_completion_list(DSQH)
combo.pack(side = tkinter.LEFT)


l2 = tkinter.Label(frame2, text = "Giá từ:         ", font="TimesNewRoman 15 bold")
l2.pack(side = tkinter.LEFT)
entry1 = tkinter.Entry (frame2) 
entry1.pack(side = tkinter.LEFT)
l3 = tkinter.Label(frame2, text = "đến", font="TimesNewRoman 15 bold")
l3.pack(side = tkinter.LEFT)
entry2 = tkinter.Entry (frame2) 
entry2.pack(side = tkinter.LEFT)

l4 = tkinter.Label(frame3, text = "Diện Tích từ:", font="TimesNewRoman 15 bold")
l4.pack(side = tkinter.LEFT)
entry3 = tkinter.Entry (frame3) 
entry3.pack(side = tkinter.LEFT)
l5 = tkinter.Label(frame3, text = "đến", font="TimesNewRoman 15 bold")
l5.pack(side = tkinter.LEFT)
entry4 = tkinter.Entry (frame3) 
entry4.pack(side = tkinter.LEFT)

l6 = tkinter.Label(frame4, text = "Số dữ liệu lấy: ", font="TimesNewRoman 15 bold")
l6.pack(side = tkinter.LEFT)
entry5 = tkinter.Entry (frame4) 
entry5.pack(side = tkinter.LEFT)

def CrawlData():
    messagebox.showinfo("Thành Phố", str(combo.get()))
    messagebox.showinfo("Giá", "Giá từ " + str(entry1.get()) + " đến " + str(entry2.get()))
    messagebox.showinfo("Diện tích", "Diện tích từ " + str(entry3.get()) + " đến " + str(entry4.get()))
    messagebox.showinfo("Lấy dữ liệu trang", "")
    # Crawl_Page(combo.get(), int(entry5.get()))
    # # messagebox.showinfo("Lấy dữ liệu từng trang", "")
    # print("Lấy dữ liệu từng trang")
    # Crawl_Data()
    # # messagebox.showinfo("Xóa dữ liệu lỗi", "")
    # print("Xóa dữ liệu lỗi")
    # RemoveError()
    # # messagebox.showinfo("Chuyển thành TXT", "")
    # print("Chuyển thành TXT")
    # TXT2CSV()
    # # messagebox.showinfo("Điền dữ liệu khuyết", "")
    print("Điền dữ liệu khuyết")
    FillMissing(int(entry2.get()), int(entry4.get()))
    # messagebox.showinfo("Train")
    print("Predict")
    Predicts()

submitBtn = tkinter.Button(frame5, text='Crawl Data', command=CrawlData, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
submitBtn.pack(side = tkinter.TOP)

root.bind('<Control-Q>', lambda event=None: root.destroy())
root.bind('<Control-q>', lambda event=None: root.destroy())



root.mainloop()


