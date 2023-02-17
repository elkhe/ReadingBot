from datetime import datetime

date_str = datetime.now().strftime('%d-%m-%y')
date_obj = datetime.strptime(date_str, '%d-%m-%y')


date1 = datetime.today().strftime('%y-%m-%d')
date1 = datetime.strptime(date1, '%y-%m-%d')
print(date1 == date_obj)