## ---------------------------- Imports ---------------------------- 
import tkinter as tk 
from tkinter import *
from tkinter import ttk 
from tkinter.scrolledtext import *
import tkinter.filedialog
from helpers import *

## ---------------------------- Structure ----------------------------
window = Tk()
window.title("Summarizer")
window.geometry("700x400")
window.config(background='black')
window.iconbitmap('pencil.ico')

## Style
style = ttk.Style(window)
style.configure('lefttab.TNotebook', tabposition='en',)

## Tabs
tab_control = ttk.Notebook(window, style='lefttab.TNotebook')
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab1, text=f'{"Plain Text":^20s}')
tab_control.add(tab2, text=f'{"URL":^20s}')
tab_control.add(tab3, text=f'{"Text File":^20s}')


## ---------------------------- Labels ----------------------------
## Labels
label1 = Label(tab1, text= 'Plain Text',padx=5, pady=5)
label1.grid(column=0, row=0)
label2 = Label(tab2, text= 'URL',padx=5, pady=5)
label2.grid(column=0, row=0)
label3 = Label(tab3, text= 'Text File',padx=5, pady=5)
label3.grid(column=0, row=0)
tab_control.pack(expand=1, fill='both')


## ---------------------------- Functions ----------------------------
## **************************** PLAIN TEXT ****************************
# clear text
def clear_text_pt():
    	plain_text.delete('1.0',END)
     
# clear display
def clear_display_pt():
    	plain_text_disp.delete('1.0',END)
# Ext. Summarize
def get_ext_pt():
    raw_text = str(plain_text.get('1.0',tk.END))
    num_sents = int(plain_text_ns.get())
    final_text = text_to_sents(raw_text, num_sents)
    result = '\nSummary:{}'.format(final_text)
    plain_text_disp.insert(tk.END,result)
# Abs. Summarize
def get_abs_pt():
    raw_text = str(plain_text.get('1.0',tk.END))
    final_text = abstract_summarize(raw_text)
    result = '\nSummary:{}'.format(final_text)
    plain_text_disp.insert(tk.END,result)

# **************************** URL ****************************
# clear text
def clear_text_url():
    	url_entry.delete('1.0',END)     
# clear display
def clear_display_url():
    	url_disp.delete('1.0',END)
# Ext. Summarize
def get_ext_url():
    raw_text = str(url_entry.get())
    num_sents = int(url_ns.get())
    final_text = wiki_to_sents(raw_text, num_sents)
    result = '\nSummary:{}'.format(final_text)
    url_disp.insert(tk.END,result)
# Abs. Summarize
def get_abs_url():
    raw_text = str(url_entry.get())
    pre_text = pull_text(raw_text)
    final_text = abstract_summarize(pre_text)
    result = '\nSummary:{}'.format(final_text)
    url_disp.insert(tk.END,result)

# **************************** TEXT FILE ****************************
# clear text
def clear_text_file():
    	displayed_file.delete('1.0',END)     
# clear display
def clear_display_file():
    	file_disp.delete('1.0',END)
# load file
def openfiles():
    file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files",".txt"),("All files","*")))
    read_text = open(file1).read()
    displayed_file.insert(tk.END,read_text)
# Ext. Summarize
def get_ext_file():
    raw_text = displayed_file.get('1.0',tk.END)
    num_sents = int(file_ns.get())
    final_text = text_to_sents(raw_text, num_sents)
    print(final_text)
    result = '\nSummary:{}'.format(final_text)
    file_disp.insert(tk.END,result)
# Abs. Summarize
def get_abs_file():
    raw_text = displayed_file.get('1.0',tk.END)
    final_text = abstract_summarize(raw_text)
    print(final_text)
    result = '\nSummary:{}'.format(final_text)
    file_disp.insert(tk.END,result)


## ---------------------------- Buttons ----------------------------
## **************************** PLAIN TEXT ****************************
reset1=Button(tab1,text="Reset", command=clear_text_pt, width=12,bg='#03A9F4',fg='#fff') 
reset1.grid(row=5,column=0,padx=10,pady=10)
abs1=Button(tab1,text="Abstractive", command=get_abs_pt, width=12,bg='#03A9F4',fg='#fff') 
abs1.grid(row=5,column=1,padx=10,pady=10)
clear1=Button(tab1,text="Clear Result", command=clear_display_pt, width=12,bg='#03A9F4',fg='#fff') 
clear1.grid(row=6,column=0,padx=10,pady=10)
ext1=Button(tab1,text="Extractive", command=get_ext_pt, width=12,bg='#03A9F4',fg='#fff') 
ext1.grid(row=6,column=1,padx=10,pady=10)

## **************************** URL **********************************
reset2=Button(tab2,text="Reset", command=clear_text_url, width=12,bg='#03A9F4',fg='#fff') # command=clear_text,
reset2.grid(row=4,column=0,padx=10,pady=10)
abs2=Button(tab2,text="Abstractive", command=get_abs_url, width=12,bg='#03A9F4',fg='#fff') # command=get_summary,
abs2.grid(row=4,column=1,padx=10,pady=10)
clear2=Button(tab2,text="Clear Result", command=clear_display_url, width=12,bg='#03A9F4',fg='#fff') # command=clear_display_result
clear2.grid(row=5,column=0,padx=10,pady=10)
ext2=Button(tab2,text="Extractive", command=get_ext_url, width=12,bg='#03A9F4',fg='#fff') # command=get_summary,
ext2.grid(row=5,column=1,padx=10,pady=10)

## **************************** TEXT FILE ****************************
open_file=Button(tab3,text="Load File", command=openfiles, width=12,bg='#03A9F4',fg='#fff')
open_file.grid(row=6, column=2, padx=10, pady=10)
reset3=Button(tab3,text="Reset", command=clear_text_file, width=12,bg='#03A9F4',fg='#fff') # command=clear_text,
reset3.grid(row=6,column=0,padx=10,pady=10)
abs3=Button(tab3,text="Abstractive", command=get_abs_file, width=12,bg='#03A9F4',fg='#fff') # command=get_summary,
abs3.grid(row=6,column=1,padx=10,pady=10)
clear3=Button(tab3,text="Clear Result", command=clear_display_file, width=12,bg='#03A9F4',fg='#fff') # command=clear_display_result
clear3.grid(row=7,column=0,padx=10,pady=10)
ext3=Button(tab3,text="Extractive", command=get_ext_file, width=12,bg='#03A9F4',fg='#fff') # command=get_summary,
ext3.grid(row=7,column=1,padx=10,pady=10)


## ---------------------------- Displays ----------------------------
## **************************** PLAIN TEXT ****************************
# labels and entries 
l1=Label(tab1, text="Enter Text To Summarize")
l1.grid(row=1,column=0)
plain_text=ScrolledText(tab1,height=10)
plain_text.grid(row=2,column=0,columnspan=2,padx=5,pady=5)
ns_1=Label(tab1, text="Enter Number of Sentences if Extractive")
ns_1.grid(row=3,column=0)
plain_text_ns=Entry(tab1)
plain_text_ns.grid(row=4,column=0)
# Output
plain_text_disp = Text(tab1)
plain_text_disp.grid(row=8,column=0, columnspan=3,padx=5,pady=5)

## **************************** URL **********************************
# labels and entries 
l2 = Label(tab2, text="Enter URL to summarize")
l2.grid(row=1,column=0)
raw_entry=StringVar()
url_entry=Entry(tab2,textvariable=raw_entry,width=50)
url_entry.grid(row=1,column=1)
ns_2=Label(tab2, text="Enter Number of Sentences if Extractive")
ns_2.grid(row=2,column=0)
url_ns=Entry(tab2)
url_ns.grid(row=3,column=0)
# Output
url_disp = Text(tab2)
url_disp.grid(row=7,column=0, columnspan=3,padx=5,pady=5)

## **************************** TEXT FILE ****************************
l3 = Label(tab3, text="Load Text File ")
l3.grid(row=1,column=0)
displayed_file = ScrolledText(tab3,height=7)# Initial was Text(tab2)
displayed_file.grid(row=2,column=0, columnspan=3,padx=5,pady=3)
ns_3=Label(tab3, text="Enter Number of Sentences if Extractive")
ns_3.grid(row=3,column=0)
file_ns=Entry(tab3)
file_ns.grid(row=5,column=0)
# Output
file_disp = Text(tab3)
file_disp.grid(row=8,column=0, columnspan=3,padx=5,pady=5)




window.mainloop()