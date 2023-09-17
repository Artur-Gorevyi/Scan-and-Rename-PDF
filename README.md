# Issue:
There are a large number of documents that need to be scanned through the printer and get a PDF for each.
Then go into each document and rename it with the name that is in the document. 

# Solution:
In the file, there is a number attached to the name. If we know the number, we will know the name. The program uses Tesseract OCR to scan the PDF document and find that number. If we find the number, we compare it to the database and rename our PDF with the name attached to the number we found.

# Renamer GUI

After starting the program, we see a window in which there are 2 buttons.

As we can see, the "RENAME" button is not active because there is nothing to rename yet

![image](https://github.com/Artur-Gorevyi/Scan-and-Rename-PDF/assets/108293399/845ad435-0d56-44ca-a17a-b3a72168b361)

After clicking on the "UPLOAD" button, a dialog box appears in which we choose the files that we want to upload to the program

![image](https://github.com/Artur-Gorevyi/Scan-and-Rename-PDF/assets/108293399/12d4bb74-af8e-4e7b-ae3b-701aa2df79d8)

Also, we can simply drag and drop files we have selected to a special area

![image](https://github.com/Artur-Gorevyi/Scan-and-Rename-PDF/assets/108293399/2f6a5d1f-2bf4-4d27-8bb2-6819d8826ec9)

After successfully uploading the files into the program, we can see that the "RENAME" button has become active and the mini assistant shows how many files we have selected

![image](https://github.com/Artur-Gorevyi/Scan-and-Rename-PDF/assets/108293399/1ae1ac0f-56e7-43e9-9aa4-76b6ffdd4286)

After pressing the "RENAME" button, we can see how the PDF files start to be renamed, of course if it satisfies the condition in the program

![image](https://github.com/Artur-Gorevyi/Scan-and-Rename-PDF/assets/108293399/ea626e63-184d-4cc9-93b1-e64b3b0c4aee)

# How it works?

I use Tesseract-OCR and Pillow to extract text from PDF files
Using the Pillow library, I convert the PDF to a JPG photo and scan this photo using Tesseract-OCR.
At the output, I get all the text from the PDF file and scan it to match my number
And if there is a match, the program renames the PDF file to the name that is in the dictionary

![image](https://github.com/Artur-Gorevyi/Scan-and-Rename-PDF/assets/108293399/122249c5-4871-434a-9c1c-6a712524e4fa)


