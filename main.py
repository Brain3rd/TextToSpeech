import PyPDF2
import pyttsx3
from tkinter import *
from tkinter import filedialog
from tkPDFViewer import tkPDFViewer

BTN_COLOR = "#1e2022"
CANVAS_COLOR = "#dddddd"
BG_COLOR = '#52616b'
FONT_COLOR = '#c9d6df'


class PDFText:
    def __init__(self):
        self.reader = pyttsx3.init()
        self.reading = True
        self.paused = False
        self.pdf_text = []
        self.read_this = []
        self.filepath = None

        window = Tk()
        window.geometry("700x800")

        self.canvas = Canvas()
        self.canvas.pack()

        open_button = Button(text='Open', command=self.open_pdf)
        open_button.place(x=155, y=5)

        read_button = Button(text='Read', command=self.read_pages)
        read_button.place(x=503, y=5)

        self.start_entry = Entry()
        self.start_entry.insert(END, 'Page to start reading')
        self.start_entry.place(x=215, y=9)

        self.stop_entry = Entry()
        self.stop_entry.insert(END, 'Page to stop reading')
        self.stop_entry.place(x=360, y=9)

        window.mainloop()

    def read_pages(self):
        try:
            self.read_words(int(self.start_entry.get()), int(self.stop_entry.get()))
        except ValueError:
            pass

    def read_words(self, from_pages, to_pages):

        # Open pdf
        pdf = PyPDF2.PdfFileReader(self.filepath)
        # pages = pdf.numPages

        # Add pages to the list to read
        for page in range(from_pages - 1, to_pages - 1):
            one_page = pdf.getPage(page)
            page_list = one_page.extractText()
            self.pdf_text.append(page_list)

        # Save pages to txt file
        with open('text.txt', 'w') as file:
            file.write(''.join(self.pdf_text))

        # Setting up new voice rate
        self.reader.setProperty('rate', 125)

        # Setting up volume level  between 0 and 1
        self.reader.setProperty('volume', 1)

        # Changing index, changes voices. o for male
        voices = self.reader.getProperty('voices')
        male = voices[0].id
        # female = voices[1].id
        self.reader.setProperty('voice', male)

        # # Save
        # self.reader.save_to_file(read_this, 'test.mp3')

        # Open txt and get rid of some not needed characters
        with open('text.txt') as file:
            read_text = file.readlines()
            for word in read_text:
                if word == ' \n':
                    word = ' '
                if word != '\n':
                    self.read_this.append(word)
            # Read this
            self.reader.say(''.join(self.read_this))
            self.reader.runAndWait()

    def open_pdf(self):
        self.filepath = filedialog.askopenfilename(title='Open PDF')
        show_pdf = tkPDFViewer.ShowPdf()
        open_pdf = show_pdf.pdf_view(self.canvas, pdf_location=self.filepath, load='after')
        open_pdf.config(padx=50, pady=35, bg=BTN_COLOR)
        open_pdf.pack()


PDFText()

