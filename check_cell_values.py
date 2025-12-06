import win32com.client
import os

xl = win32com.client.Dispatch('Excel.Application')
xl.Visible = False
wb = xl.Workbooks.Open(os.path.abspath('ATTACHED_ASSETS/english Note FINAL BILL NOTE SHEET.xlsm'))
ws = wb.Sheets(1)

print('Cell values from Excel:')
print(f'C18 (Work Order): {ws.Range("C18").Value}')
print(f'C19 (17.A): {ws.Range("C19").Value}')
print(f'C20 (17.B): {ws.Range("C20").Value}')
print(f'C21 (17.C): {ws.Range("C21").Value}')
print(f'C21 Formula: {ws.Range("C21").Formula}')

print('\nDates:')
print(f'C13 (Start): {ws.Range("C13").Value}')
print(f'C14 (Schedule): {ws.Range("C14").Value}')
print(f'C15 (Actual): {ws.Range("C15").Value}')

print('\nOther fields:')
print(f'C29 (Repair): {ws.Range("C29").Value}')
print(f'C30 (Extra Item): {ws.Range("C30").Value}')
print(f'C31 (Extra Amount): {ws.Range("C31").Value}')
print(f'C32 (Excess Qty): {ws.Range("C32").Value}')
print(f'C33 (Delay Comment): {ws.Range("C33").Value}')

wb.Close(False)
xl.Quit()
