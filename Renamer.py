import os
import fitz
import pytesseract
import filetype
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = (r'/usr/bin/tesseract')

directory = '/content/'

numberdict = numberdict_kv

def is_pdf(path_to_file):
    return filetype.guess(path_to_file).mime == 'application/pdf'

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
  num = "67414"

  # Open and scan image
  img = Image.open(img_name)
  scan = pytesseract.image_to_string(img, config='--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789')

  # Delete image
  img.close()
  os.remove(f"{img_name}")

  # Search 67414
  for i in scan:
    if i == num[m]:
      m += 1
      if m == 4:
        code = num+scan[n+2]+scan[n+3]+scan[n+4]+scan[n+5]
        break
    n += 1

  print(f"code: {code}")
  return code

# Rename PDF
def rename(pdf_name, code):
  name = ''

  for number in numberdict:
    if code == number:
      name = numberdict[number]
      print(f"found {name}\n")
      os.rename(f"{pdf_name}", f"{name}.pdf")

def main():
  # Find PDF files
  for filename in os.listdir(directory):
      if os.path.isfile(os.path.join(directory, filename)):
          if is_pdf(filename):
            rename(filename, scan_img(pdf_to_img(directory+filename)))


if __name__ == "__main__":
  main()