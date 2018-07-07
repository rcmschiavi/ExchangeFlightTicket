
import xlwt

# Initialize a workbook
book = xlwt.Workbook()

# Add a sheet to the workbook
sheet1 = book.add_sheet("Sheet1")

# The data
cols = ["A", "B", "C", "D", "E","F"]
titulo = ["Departure","Arrival","Outbound","Return","Amount","Days"]
def grava_linha(linha,cont):
    global book,sheet,cols,titulo,txt
    # Loop over the rows and columns and fill in the values
    row = sheet1.row(cont)
    for index, col in enumerate(cols):
      if(cont==0):
          value = titulo[index]
          row.write(index, value)
      else:
          value = linha[index]
          row.write(index, value)


# Save the result
def salvar(nome):
    global book
    book.save("{0}.xls".format(nome))