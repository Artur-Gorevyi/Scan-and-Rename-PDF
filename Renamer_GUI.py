import os
import re
import fitz
import pytesseract
import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk, Image
from tkinter import filedialog
from Numberdict import numberdict # My dict of numbers
from tkinterdnd2 import DND_FILES, TkinterDnD
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe' # path to Tesseract.exe

# Disable button
def disable(btn):
  btn['state']='disabled'
  btn['bg']='Silver'

# Enable button
def enable(btn, clr):
  btn['state']='active'
  btn['bg']=clr

# Versions of text
def vers(text, n):
  lenf = len(files)

  if(n==0):
    text['text']='Ready to upload'
  if(n==1):
    text['text']= ('Selected ' +str(lenf)+ ' files')
  if(n==2):
    text['text']='Renamed! Ready to upload'
  if(n==3):
    text['text']='Error, not found numbers'
    
# Convert for scan
def pdf_to_img(pdf_name):
  print(f"Scaning - {pdf_name}")
  pdf_doc = fitz.open(pdf_name)
  page = pdf_doc[0]
  pix = page.get_pixmap()
  image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
  image.save(f"{pdf_name[:-4]}.jpg", format="JPEG")
  pdf_doc.close()

  return f"{pdf_name[:-4]}.jpg"

# Scan number
def scan_img(img_name):
  m = 0
  n = 0
  code = ""
  num = "67414" # In my case
  global Err

  # Open and scan image
  img = Image.open(img_name)
  scan = pytesseract.image_to_string(img, config='--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789')

  # Delete image
  img.close()
  os.remove(f"{img_name}")

  # Search 67414 (In my case)
  for i in scan:
    if i == num[m]:
      m += 1
      if m == 4:
        code = num+scan[n+2]+scan[n+3]+scan[n+4]+scan[n+5]
        break
    n += 1
  
  # If not found
  if m < 4:
    Err = True
    print(f"Not found code")
    return Err
  
  # If found
  else:
    print(f"code: {code}")
    return code


# RENAME
def rename(pdf_name, code):
  global Err

  # If have no error start rename
  if Err != True:
    name = ''
    dir = os.path.dirname(pdf_name)

    # If match - rename
    for number in numberdict:
      if code == number:
        name = numberdict[number]
        print(f"found {name}\n")
        os.rename(f"{pdf_name}", f"{dir}\{name}.pdf")

Err = False
files = {}

# DROP PDF
def drop(event):
  global files
  global main_img
  
  # Filter our event.data from DROP
  pattern = r'(?:\{([^}]*)\}|([^ ]+\.(?:pdf|PDF)))'
  files = [path[0] if path[0] else path[1] for path in re.findall(pattern, event.data)]

  # I need only PDF files
  pdf_files = [file for file in files if file.lower().endswith('.pdf')]

  files = pdf_files

  if len(files)!=0:
    enable(rename_button, 'white')
    disable(upload_button)
    vers(dtext, 1)

# UPLOAD PDF
def upload_pdf():
  global files
  files=filedialog.askopenfilenames(filetypes=[('PDF','*.pdf')],
  initialdir=os.getcwd(), title='Select File/Files')
  print(files)

  if len(files)!=0:
    enable(rename_button, 'white')
    disable(upload_button)
    vers(dtext, 1)

# MAIN FUNC - RENAME PDF
def rename_pdf():
  global files
  global Err

  # Function takes other functions
  for file in files:
    rename(file, scan_img(pdf_to_img(file)))

  disable(rename_button)
  enable(upload_button, 'white')
  if Err != True:
    vers(dtext, 2)
  else:
    vers(dtext, 3)
  Err = False

# Design GUI
win = TkinterDnD.Tk()
win.title('Renamer')
win.geometry('350x425')
win.iconbitmap('rename.ico')
win.resizable(0,0)

mybg = "#202020"
win["bg"] = mybg

# Image
canvas = Canvas(win, width=300, height=150, bg=mybg)
canvas.grid(row=0, column=0, sticky=tk.N, padx=0, pady=25)

# DROP AREA
canvas.drop_target_register(DND_FILES)
canvas.dnd_bind('<<Drop>>', drop)

# DROP IMAGE
main_img = ImageTk.PhotoImage(Image.open('drop.png'))
canvas.create_image(150, 75, image = main_img)
canvas.config(highlightthickness=0)

# Dinamic text
dtext = tk.Label(win, text='Ready to upload', width=30, height=1, font=('Helvetica', 13, 'bold'), bg=mybg, fg='white')
dtext.grid(row=2, column=0, padx=0, pady=0)

# Upload botton
upload_button = tk.Button(win, text='Upload', width=24, height=2, font=('Helvetica', 15, 'bold'), bg='White', fg='Black', relief="flat", command=upload_pdf)
upload_button.grid(row=3, column=0, padx=25, pady=20)

# Convert button
rename_button = tk.Button(win, text='Rename', width=24, height=2, font=('Helvetica', 15, 'bold'), bg='White', fg='Black', relief="flat", command=rename_pdf)
rename_button.grid(row=4, column=0, padx=25, pady=0)
disable(rename_button)

win.mainloop()