# attempt at extracting countries and human rights violations from HR report
import PyPDF2

def extractpdf(pdf_path):
  with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
      text +=  page.extract_text() + "\n"
  return text
