import xlwt
import re
import xlrd


'''n=0
with open('12452310859.txt', 'r') as f1, open('a.txt', 'w') as f2:
    for line in f1.readlines():
        line = line.strip()
        if "content " in line:
            f2.write(line+'\n')
            
wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet('review') 
f = open(r'C:\Python27\a.txt')
j = 0
for line in f.readlines():
    ws.write(j,0,re.sub('content',' ',line))
    j+=1
wb.save('review.xlsx')

table = xlrd.open_workbook(r'C:\Python27\review.xlsx')
sheet = table.get_sheet(0)
data = sheet.col_values(0)
print data'''

r'C:\Python27\Review-Helpfulness-Prediction-master\main\Reviewset\review1.xlsx'
def extract(filepath):
    txt = open(filepath,'r')
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('review')
    j = 0
    for line in txt.readlines():
        if "content" in line:
            ws.write(j,0,re.sub('content',' ',line))
            j += 1
    wb.save('review.xlsx')


    
    
    
    
 
