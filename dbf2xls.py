from dbfread import DBF
import sys

table = DBF('data_yy.dbf')
i = 1
ii = 1
import xlwt

wbk = xlwt.Workbook()
sheet = wbk.add_sheet('sheet 1')

sheet2 = wbk.add_sheet('sheet 2')

print('this is : ')
sys.stdout.flush()
for record in table:
	j = 0
	if i<60000 :
		if i==1 :
			for field in record :
				sheet.write(0,j,field)
				sheet.write(i,j,record[field])
				j+=1
		else :
			for field in record:
				sheet.write(i,j,record[field])
				j += 1
		print('\r'+str(i),end='')
		sys.stdout.flush()
		i += 1
	else :
		if ii==1 :
			for field in record:
				sheet2.write(0,j,field)
				sheet2.write(ii,j,record[field])
				j += 1
		else :
			for field in record:
				sheet2.write(ii,j,record[field])
				j += 1		
		print('\r'+str(i+ii),end='')
		sys.stdout.flush()		
		ii += 1
wbk.save('data.xls')