import PyPDF2


def main():
    pdf1File = open('chapter_15_working_with_pdf.pdf', 'rb')
    pdf1Reader = PyPDF2.PdfReader(pdf1File)

    page = pdf1Reader.pages[0]
    page.rotate(90)

    pdfWriter = PyPDF2.PdfWriter()
    pdfWriter.add_page(page)
    resultPdfFile = open('rotatedPage.pdf', 'wb')
    pdfWriter.write(resultPdfFile)
    resultPdfFile.close()
    pdf1File.close()


if __name__ == '__main__':
    main()