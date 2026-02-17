
import xlsxwriter

workbook = xlsxwriter.Workbook('test_edge.xlsx')
worksheet = workbook.add_worksheet()

# Regular link
worksheet.write_url('A1', 'https://www.google.com', string='Open in Default')

# Edge link
# Note: "microsoft-edge:" is a URI scheme registered by Edge on Windows
worksheet.write_url('A2', 'microsoft-edge:https://www.google.com', string='Open in Edge')

workbook.close()
print("Created test_edge.xlsx")
