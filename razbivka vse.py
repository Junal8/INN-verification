#!/usr/bin/env python
# coding: utf-8

# In[2]:


from tkinter import * 
import tkinter.ttk as ttk 
import time, threading 
from tkinter import filedialog as fd 
from tkinter import messagebox
from tkinter.ttk import Radiobutton
import datetime as dt
from PIL import Image, ImageTk
#from datetime import date

import pandas as pd
import py_win_keyboard_layout


# In[ ]:


py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)

# 📗 считывает данные от пользователя 📗
def get_address(): 
    global INN 
    global ADRESS
    global COUNT    
      
    INN = t.get(1.0, 'end-1c') 
    ADRESS = adress.get()  
    COUNT = count.get()    
    
def get_address_2(): 
    global INN_2 
    global ADRESS_2
    global COUNT_2    
      
    INN_2 = t_2.get(1.0, 'end-1c') 
    ADRESS_2 = adress_2.get()  
    COUNT_2 = count_2.get()  
    
def get_address_3(): 
    global INN_3 
    global ADRESS_3
    global COUNT_3    
      
    INN_3 = t_3.get(1.0, 'end-1c') 
    ADRESS_3 = adress_3.get()  
    COUNT_3 = count_3.get()     
    
# 💻 Размеры и название окна 💻
root = Tk() 
root.title("Разбивка списка ИНН") 
root.resizable(width=False, height=False) 
root.geometry("650x580+600+300") 
#calculated_text = Text(root,height=15, width=50) 


# 1️⃣ работа с первым блоком 1️⃣   
def work_1():
    #global SELECTED
    SELECTED = selected.get()
    INN_CHECK = inn_check.get()    
    #lbl.configure(text=selected.get())
    
    #global count_all
    #global count_all_drop_dupli
    # время для сохранения файла
    dt_now = str(dt.datetime.now().time())[:8].replace(':', ' ')
    
    # упаковка списка в датафрейм
    inn_list = INN.split()
    inn_data = pd.DataFrame({'inn' : inn_list})
    
    # в ковычках и квадратных скобках необходимо указать имя столбца с ИНН, которые надо разбить
    # сортировка и сброс индекса    
    data = inn_data['inn'].sort_values()
    count_all = len(data)   
    data = data.drop_duplicates().reset_index()
    count_all_drop_dupli = len(data)
    #data.head()
    
# ❌1️⃣ обработка ошибок - кол-во символов  
    dt_count = data['inn'].reset_index()  # pd.DataFrame()
    dt_error = data['inn'].reset_index()
    dt_contr_sum = data['inn'].reset_index()
    
    def count_num(dt, col, dt_2, col_2):
        dt[col] = dt_2[col_2].str.split('').str.len() - 2         
    
    count_num(dt_count, 'INN_count', data, 'inn') 
    count_num(dt_contr_sum, 'INN_count', data, 'inn') 
    # откидываем тех кто с меньшим кол-вом символов
    dt_count_general = dt_count.query('INN_count not in [12, 10]')
    
    dt_count_general_all_1 = dt_count_general['inn'].tolist()  
    
    
# ⭕1️⃣ обработка ошибок на неправомерные символы    
    def count_warning(dt, col, dt_2, col_2):
        dt[col] = dt_2[col_2].str.isnumeric()
        
    count_warning(dt_error, 'inn_true', data, 'inn')
    count_warning(dt_contr_sum, 'inn_true', data, 'inn')
    # откидываем тех кто с неправомерными символами
    dt_error_general = dt_error.query('inn_true == False')
    
    dt_error_general_all_1 = dt_error_general['inn'].tolist()    
    
# 🚫 1️⃣ обработка ошибок на контрольные суммы 
    # разбивая на датафремы по 10 и 12 символов и косячные
    dt_10 = dt_contr_sum.query('INN_count == 10 and inn_true == True')
    dt_12 = dt_contr_sum.query('INN_count == 12 and inn_true == True')
    dt_all = dt_contr_sum.query('INN_count not in [10, 12] or inn_true != True')
    # Косячные заполним сразу FALSE
    dt_all = dt_all[['inn']]
    dt_all['itog'] = False
    #создаю столбцы и заполняю числами из инн, каждому числу свой столбец
    def num_split(dt, col_1, col_2, numb):
        dt[col_1] = dt[col_2].apply(lambda x: x[numb]).astype('int')
    
    #ЮЛ    
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10'], range(10)):
        num_split(dt_10, i, 'inn', j)

    #ФЛ    
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10', 'n_11', 'n_12'], range(12)):    
        num_split(dt_12, i, 'inn', j)
    #Рассчитыва числа где 10 символов
    dt_10['sum_1'] = 0
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9'], [2, 4, 10, 3, 5, 9, 4, 6, 8]):
        dt_10['sum_1'] += dt_10[i] * j 
    
    dt_10['sum_1'] = dt_10['sum_1'] % 11 % 10
    dt_10['itog'] = dt_10['sum_1'] == dt_10['n_10']
    dt_10 = dt_10[['inn', 'itog']]
    
    #Рассчитыва числа где 12 символов
    dt_12['sum_1'] = 0
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10'], 
                     [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]): 
        dt_12['sum_1'] +=  dt_12[i] * j
    
    dt_12['sum_1'] = dt_12['sum_1'] % 11 % 10

    dt_12['sum_2'] = 0
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10', 'sum_1'], 
                 [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]): 
        dt_12['sum_2'] +=  dt_12[i] * j
        
    dt_12['sum_2'] = dt_12['sum_2'] % 11 % 10

    dt_12['itog_1'] = dt_12['sum_1'] == dt_12['n_11']
    dt_12['itog_2'] = dt_12['sum_2'] == dt_12['n_12']
    dt_12['itog'] = dt_12['itog_1'] == dt_12['itog_2']
    dt_12 = dt_12[['inn', 'itog']]
    # соединяю все три датафрейма(10, 12 и косячные)
    general_itog = pd.concat([dt_12, dt_10])
    general_itog = pd.concat([general_itog, dt_all])
    
    dt_cont_summ_general = general_itog.query('itog == False')
    
    dt_cont_summ_general_1 = dt_cont_summ_general['inn'].tolist()    

    
    # заданный параметр, на ск бить строк
    ff = int(COUNT)
    
    # расчеты диапазонов, не лезть
    kol = int(len(data) / ff) + 1
    dictt = {}
    for i in range(0, kol):
        dictt[i] = {ff * i : ff * (i + 1)}
        
    # создание списка ИНН
    data_22 = data['inn'].tolist()   
    
    # разбивка ИНН по диапозонам
    se = {}
    for i in range(kol):
        se[i] = pd.Series(data_22[(int(format(*dictt[i].keys()))) : (int(format(*dictt[i].values())))])
        
    # итоговая разбивка по столбцам согласно диапазонов, заданных выше
    for i in range(kol):
        data[i] = se[i]
        
    # общее кол-во столбцов, необходимо для правильной разбивки
    cols_count_all = len(data.axes[1])
    
    data_1 = data[data.columns[2 : cols_count_all-1]].dropna(how='all')
    data_2 = data[data.columns[cols_count_all-1 : ]].dropna()
    
    cols_count_data_1 = len(data_1.axes[1])
        
    #data = data.drop(['index', 'inn'], axis = 1)
    #data = data.dropna(how='all')
    #data = data.fillna('0')  
    
    #cols_count = len(data.axes[1])
    
    myfile = open(ADRESS + '\\Разбивка Spis_INN '+ dt_now + '.txt', 'w')    
    
    
    # Версия под вьюху виртуальной таблицы ИНН
    
    myfile.write('Всего ИНН - ' + str(count_all) + '. ')
    myfile.write('Из них дублей - ' + str(count_all - count_all_drop_dupli) + '. ')
    myfile.write('Всего ИНН с учетом удаленных дублей - ' + str(count_all_drop_dupli) + '.\n\n')
    if INN_CHECK == 'YES_OF_COURSE':
        myfile.write('Проверка ИНН на неправомерные символы, количество символов и контрольные суммы:\n')
        myfile.write('ИНН с неправильным количеством символов - ' + str(dt_count_general_all_1))
        myfile.write('\n')
        myfile.write('ИНН с неправомерными символами - ' + str(dt_error_general_all_1))    
        myfile.write('\n')
        myfile.write('ИНН с неправильными контрольными суммами - ' + str(dt_cont_summ_general_1))
    else: pass    
    myfile.write('\n')
    myfile.write('\n')
    myfile.write('\n')
    myfile.write('With Spis_INN as(\n')
    
    if cols_count_data_1 == 0:
        for i in range(1):
            myfile.write("select column_value as INN from\n") 
            myfile.write("table(sys.ODCIVARCHAR2LIST(\n")             
            if SELECTED == 'STR': 
                myfile.write("'")
                myfile.write(','.join(data_2[i]).replace(',', "','")) 
                myfile.write("'")
            else:
                myfile.write(','.join(data_2[i]))             
            myfile.write("))\n")
            #myfile.write("union all\n") 
    else:
        for i in range(cols_count_data_1):
            myfile.write("select column_value as INN from\n") 
            myfile.write("table(sys.ODCIVARCHAR2LIST(\n")            
            if SELECTED == 'STR':
                myfile.write("'")
                myfile.write(','.join(data_1[i]).replace(',', "','"))
                myfile.write("'")
            else:
                myfile.write(','.join(data_1[i]))   
            myfile.write("))\n")
            myfile.write("union all\n")
    
        for j in range(cols_count_data_1, cols_count_data_1 + 1):
            myfile.write("select column_value as INN from\n") 
            myfile.write("table(sys.ODCIVARCHAR2LIST(\n")            
            if SELECTED == 'STR':
                myfile.write("'")
                myfile.write(','.join(data_2[j]).replace(',', "','"))
                myfile.write("'")
            else:
                myfile.write(','.join(data_2[j])) 
            myfile.write("))\n")
        
    myfile.write('),')    
    myfile.close()
    
    
# 2️⃣ работа со вторым блоком 2️⃣       
def work_2():
    SELECTED_2 = selected_2.get()
    INN_CHECK_2 = inn_check_2.get()
    #lbl.configure(text=selected_2.get())
    
    # время для сохранения файла
    dt_now = str(dt.datetime.now().time())[:8].replace(':', ' ')
        
    # упаковка списка в датафрейм
    inn_list = INN_2.split()
    inn_data = pd.DataFrame({'inn' : inn_list})
    
    # в ковычках и квадратных скобках необходимо указать имя столбца с ИНН, которые надо разбить
    # сортировка и сброс индекса
    data = inn_data['inn'].sort_values()
    count_all = len(data)
    data = data.drop_duplicates().reset_index()
    count_all_drop_dupli = len(data)
    #data.head()
# ❌2️⃣ обработка ошибок - кол-во символов  
    dt_count = data['inn'].reset_index()  # pd.DataFrame()
    dt_error = data['inn'].reset_index()
    dt_contr_sum = data['inn'].reset_index()
    
    def count_num(dt, col, dt_2, col_2):
        dt[col] = dt_2[col_2].str.split('').str.len() - 2         
    
    count_num(dt_count, 'INN_count', data, 'inn') 
    count_num(dt_contr_sum, 'INN_count', data, 'inn') 
    # откидываем тех кто с меньшим кол-вом символов
    dt_count_general = dt_count.query('INN_count not in [12, 10]')
    
    dt_count_general_all_2 = dt_count_general['inn'].tolist()  
    
    
# ⭕2️⃣ обработка ошибок на неправомерные символы    
    def count_warning(dt, col, dt_2, col_2):
        dt[col] = dt_2[col_2].str.isnumeric()
        
    count_warning(dt_error, 'inn_true', data, 'inn')
    count_warning(dt_contr_sum, 'inn_true', data, 'inn')
    # откидываем тех кто с неправомерными символами
    dt_error_general = dt_error.query('inn_true == False')
    
    dt_error_general_all_2 = dt_error_general['inn'].tolist()

# 🚫 2️⃣ обработка ошибок на контрольные суммы 
    # разбивая на датафремы по 10 и 12 символов и косячные
    dt_10 = dt_contr_sum.query('INN_count == 10 and inn_true == True')
    dt_12 = dt_contr_sum.query('INN_count == 12 and inn_true == True')
    dt_all = dt_contr_sum.query('INN_count not in [10, 12] or inn_true != True')
    # Косячные заполним сразу FALSE
    dt_all = dt_all[['inn']]
    dt_all['itog'] = False
    #создаю столбцы и заполняю числами из инн, каждому числу свой столбец
    def num_split(dt, col_1, col_2, numb):
        dt[col_1] = dt[col_2].apply(lambda x: x[numb]).astype('int')
    
    #ЮЛ    
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10'], range(10)):
        num_split(dt_10, i, 'inn', j)

    #ФЛ    
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10', 'n_11', 'n_12'], range(12)):    
        num_split(dt_12, i, 'inn', j)
    #Рассчитыва числа где 10 символов
    dt_10['sum_1'] = 0
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9'], [2, 4, 10, 3, 5, 9, 4, 6, 8]):
        dt_10['sum_1'] += dt_10[i] * j 
    
    dt_10['sum_1'] = dt_10['sum_1'] % 11 % 10
    dt_10['itog'] = dt_10['sum_1'] == dt_10['n_10']
    dt_10 = dt_10[['inn', 'itog']]
    
    #Рассчитыва числа где 12 символов
    dt_12['sum_1'] = 0
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10'], 
                     [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]): 
        dt_12['sum_1'] +=  dt_12[i] * j
    
    dt_12['sum_1'] = dt_12['sum_1'] % 11 % 10

    dt_12['sum_2'] = 0
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10', 'sum_1'], 
                 [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]): 
        dt_12['sum_2'] +=  dt_12[i] * j
        
    dt_12['sum_2'] = dt_12['sum_2'] % 11 % 10

    dt_12['itog_1'] = dt_12['sum_1'] == dt_12['n_11']
    dt_12['itog_2'] = dt_12['sum_2'] == dt_12['n_12']
    dt_12['itog'] = dt_12['itog_1'] == dt_12['itog_2']
    dt_12 = dt_12[['inn', 'itog']]
    # соединяю все три датафрейма(10, 12 и косячные)
    general_itog = pd.concat([dt_12, dt_10])
    general_itog = pd.concat([general_itog, dt_all])
    
    dt_cont_summ_general = general_itog.query('itog == False')
    
    dt_cont_summ_general_2 = dt_cont_summ_general['inn'].tolist()  
    
    
    
    # заданный параметр, на ск бить строк
    ff = int(COUNT_2)
    
    # расчеты диапазонов, не лезть
    kol = int(len(data) / ff) + 1
    dictt = {}
    for i in range(0, kol):
        dictt[i] = {ff * i : ff * (i + 1)}
        
    # создание списка ИНН
    data_22 = data['inn'].tolist()   
    
    # разбивка ИНН по диапозонам
    se = {}
    for i in range(kol):
        se[i] = pd.Series(data_22[(int(format(*dictt[i].keys()))) : (int(format(*dictt[i].values())))])
        
    # итоговая разбивка по столбцам согласно диапазонов, заданных выше
    for i in range(kol):
        data[i] = se[i]
        
        
    cols_count_all = len(data.axes[1])
    
    data_1 = data[data.columns[2 : cols_count_all-1]].dropna(how='all')
    data_2 = data[data.columns[cols_count_all-1 : ]].dropna()
    
    cols_count_data_1 = len(data_1.axes[1])
    
    #data = data.drop(['index', 'inn'], axis = 1)
    #data = data.dropna(how='all')
    #data = data.fillna('0')  
    
    # cols_count = len(data.axes[1])
    
    myfile = open(ADRESS_2 + '\\Разбивка через запятую '+ dt_now + '.txt', 'w')    
    
    
    # Версия под вьюху виртуальной таблицы ИНН
    myfile.write('Всего ИНН - ' + str(count_all) + '. ')
    myfile.write('Из них дублей - ' + str(count_all - count_all_drop_dupli) + '. ')
    myfile.write('Все ИНН с учетом удаленных дублей - ' + str(count_all_drop_dupli) + '.\n\n')
    if INN_CHECK_2 == 'YES_OF_COURSE':
        myfile.write('Проверка ИНН на неправомерные символы, количество символов и контрольные суммы:\n')
        myfile.write('ИНН с неправильным количеством символов - ' + str(dt_count_general_all_2))
        myfile.write('\n')
        myfile.write('ИНН с неправомерными символами - ' + str(dt_error_general_all_2))
        myfile.write('\n')
        myfile.write('ИНН с неправильными контрольными суммами - ' + str(dt_cont_summ_general_2))
    else: pass     
    myfile.write('\n')    
    myfile.write('\n')    
    myfile.write('\n')  
    
    
    if cols_count_data_1 == 0:
        for i in range(1):
            if SELECTED_2 == 'STR':
                myfile.write("'")
                myfile.write(','.join(data_2[i]).replace(',', "','"))
                myfile.write("'") 
            else:
                myfile.write(','.join(data_2[i]))                
            myfile.write('\n')            
            myfile.write('\n')  
    else:
        for i in range(cols_count_data_1):
            if SELECTED_2 == 'STR':
                myfile.write("'")
                myfile.write(','.join(data_1[i]).replace(',', "','"))
                myfile.write("'")   
            else:
                myfile.write(','.join(data_1[i]))
            myfile.write('\n')            
            myfile.write('\n')  
    
        for j in range(cols_count_data_1, cols_count_data_1 + 1):
            if SELECTED_2 == 'STR':
                myfile.write("'")
                myfile.write(','.join(data_2[j]).replace(',', "','"))
                myfile.write("'")  
            else:
                myfile.write(','.join(data_2[j]))
            myfile.write('\n')            
            myfile.write('\n')     
    myfile.close()  
    
    
# 3️⃣ работа со вторым блоком 3️⃣  

def work_3():
    INN_CHECK_3 = inn_check_3.get()
    # время для сохранения файла
    dt_now = str(dt.datetime.now().time())[:8].replace(':', ' ')
        
    # упаковка списка в датафрейм
    inn_list = INN_3.split()
    inn_data = pd.DataFrame({'inn' : inn_list})
    
    # в ковычках и квадратных скобках необходимо указать имя столбца с ИНН, которые надо разбить
    # сортировка и сброс индекса
    data = inn_data['inn'].sort_values()
    count_all = len(data)
    data = data.drop_duplicates().reset_index()
    count_all_drop_dupli = len(data)
    
# ❌3️⃣ обработка ошибок - кол-во символов  
    dt_count = data['inn'].reset_index()  # pd.DataFrame()
    dt_error = data['inn'].reset_index()
    dt_contr_sum = data['inn'].reset_index()
    
    def count_num(dt, col, dt_2, col_2):
        dt[col] = dt_2[col_2].str.split('').str.len() - 2         
    
    count_num(dt_count, 'INN_count', data, 'inn') 
    count_num(dt_contr_sum, 'INN_count', data, 'inn') 
    # откидываем тех кто с меньшим кол-вом символов
    dt_count_general = dt_count.query('INN_count not in [12, 10]')
    
    dt_count_general_all_3 = dt_count_general['inn'].tolist()  
    
    
# ⭕3️⃣ обработка ошибок на неправомерные символы    
    def count_warning(dt, col, dt_2, col_2):
        dt[col] = dt_2[col_2].str.isnumeric()
        
    count_warning(dt_error, 'inn_true', data, 'inn')
    count_warning(dt_contr_sum, 'inn_true', data, 'inn')
    # откидываем тех кто с неправомерными символами
    dt_error_general = dt_error.query('inn_true == False')
    
    dt_error_general_all_3 = dt_error_general['inn'].tolist()
    

# 🚫 2️⃣ обработка ошибок на контрольные суммы 
    # разбивая на датафремы по 10 и 12 символов и косячные
    dt_10 = dt_contr_sum.query('INN_count == 10 and inn_true == True')
    dt_12 = dt_contr_sum.query('INN_count == 12 and inn_true == True')
    dt_all = dt_contr_sum.query('INN_count not in [10, 12] or inn_true != True')
    # Косячные заполним сразу FALSE
    dt_all = dt_all[['inn']]
    dt_all['itog'] = False
    #создаю столбцы и заполняю числами из инн, каждому числу свой столбец
    def num_split(dt, col_1, col_2, numb):
        dt[col_1] = dt[col_2].apply(lambda x: x[numb]).astype('int')
    
    #ЮЛ    
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10'], range(10)):
        num_split(dt_10, i, 'inn', j)

    #ФЛ    
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10', 'n_11', 'n_12'], range(12)):    
        num_split(dt_12, i, 'inn', j)
    #Рассчитыва числа где 10 символов
    dt_10['sum_1'] = 0
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9'], [2, 4, 10, 3, 5, 9, 4, 6, 8]):
        dt_10['sum_1'] += dt_10[i] * j 
    
    dt_10['sum_1'] = dt_10['sum_1'] % 11 % 10
    dt_10['itog'] = dt_10['sum_1'] == dt_10['n_10']
    dt_10 = dt_10[['inn', 'itog']]
    
    #Рассчитыва числа где 12 символов
    dt_12['sum_1'] = 0
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10'], 
                     [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]): 
        dt_12['sum_1'] +=  dt_12[i] * j
    
    dt_12['sum_1'] = dt_12['sum_1'] % 11 % 10

    dt_12['sum_2'] = 0
    for i, j in zip (['n_1', 'n_2', 'n_3', 'n_4', 'n_5', 'n_6', 'n_7', 'n_8', 'n_9', 'n_10', 'sum_1'], 
                 [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]): 
        dt_12['sum_2'] +=  dt_12[i] * j
        
    dt_12['sum_2'] = dt_12['sum_2'] % 11 % 10

    dt_12['itog_1'] = dt_12['sum_1'] == dt_12['n_11']
    dt_12['itog_2'] = dt_12['sum_2'] == dt_12['n_12']
    dt_12['itog'] = dt_12['itog_1'] == dt_12['itog_2']
    dt_12 = dt_12[['inn', 'itog']]
    # соединяю все три датафрейма(10, 12 и косячные)
    general_itog = pd.concat([dt_12, dt_10])
    general_itog = pd.concat([general_itog, dt_all])
    
    dt_cont_summ_general = general_itog.query('itog == False')
    
    dt_cont_summ_general_3 = dt_cont_summ_general['inn'].tolist()    
    
    # заданный параметр, на ск бить строк
    ff = int(COUNT_3)
    
    # расчеты диапазонов, не лезть
    kol = int(len(data) / ff) + 1
    dictt = {}
    for i in range(0, kol):
        dictt[i] = {ff * i : ff * (i + 1)}
        
    # создание списка ИНН
    data_22 = data['inn'].tolist()   
    
    # разбивка ИНН по диапозонам
    se = {}
    for i in range(kol):
        se[i] = pd.Series(data_22[(int(format(*dictt[i].keys()))) : (int(format(*dictt[i].values())))])
        
    # итоговая разбивка по столбцам согласно диапазонов, заданных выше
    for i in range(kol):
        data[i] = se[i]
    
    cols_count_all = len(data.axes[1])
    
    data_1 = data[data.columns[2 : cols_count_all-1]].dropna(how='all')
    data_2 = data[data.columns[cols_count_all-1 : ]].dropna()
    
    cols_count_data_1 = len(data_1.axes[1])
    
    #data = data.drop(['index', 'inn'], axis = 1)
    #data = data.dropna(how='all')
    #data = data.fillna('0')  
    
    #  cols_count = len(data.axes[1])
    
    myfile = open(ADRESS_3 + '\\Разбивка для АИСа '+ dt_now + '.txt', 'w')     
    
    # Версия под вьюху виртуальной таблицы ИНН
    myfile.write('Всего ИНН - ' + str(count_all) + '. ')
    myfile.write('Из них дублей - ' + str(count_all - count_all_drop_dupli) + '. ')
    myfile.write('Все ИНН с учетом удаленных дублей - ' + str(count_all_drop_dupli) + '.\n\n')
    if INN_CHECK_3 == 'YES_OF_COURSE':
        myfile.write('Проверка ИНН на неправомерные символы, количество символов и контрольные суммы:\n')
        myfile.write('ИНН с неправильным количеством символов - ' + str(dt_count_general_all_3))
        myfile.write('\n')
        myfile.write('ИНН с неправомерными символами - ' + str(dt_error_general_all_3))    
        myfile.write('\n')
        myfile.write('ИНН с неправильными контрольными суммами - ' + str(dt_cont_summ_general_3))
    else: pass    
    myfile.write('\n')    
    myfile.write('\n')    
    myfile.write('\n')
    
    if cols_count_data_1 == 0:
        for i in range(1):
            myfile.write('/'.join(data_2[i]))           
            myfile.write('\n')
            myfile.write('\n')             
    else:
        for i in range(cols_count_data_1):
            myfile.write('/'.join(data_1[i]))           
            myfile.write('\n')            
            myfile.write('\n') 
    
        for j in range(cols_count_data_1, cols_count_data_1 + 1):
            myfile.write('/'.join(data_2[j]))           
            myfile.write('\n')            
            myfile.write('\n')    
    myfile.close()     
        
    


    
# 🆑 всплывающие окно конец
def click(): 
    messagebox.showinfo('Извещение', 'Посмотрите в папке ' + ADRESS + ' , файл уже готов(Разбивка Spis_INN)!)\n')  
    
# 🆑 всплывающие окно конец
def click_info_2(): 
    messagebox.showinfo('Извещение', 'Посмотрите в папке ' + ADRESS_2 + ' , файл уже готов(Разбивка через запятую)!)') 
    
# 🆑 всплывающие окно конец
def click_info_3(): 
    messagebox.showinfo('Извещение', 'Посмотрите в папке ' + ADRESS_3 + ' , файл уже готов(Разбивка для АИС3)!)')      
    
# 🆑 всплывающие окно инн
def click_1(): 
    messagebox.showinfo('Пример заполнения', 'Вставляются ИНН следующим образом, например:\n0000000001\n0000000002\n0000000003')
    
def click_lang(): 
    messagebox.showinfo('ВАЖНО!', 'Вставка ИНН и пути сохранения происходит только на английской раскладке клавиатуры. Если не происходит вставка текста - переключите раскладку на английскую!')    
    
# 🆑 всплывающие окно адрес
def click_2(): 
    messagebox.showinfo('Информация!', 'По умолчанию указана папка С:\. '+
                        'Можно заменить на любую директорию вручную или через вставку CTRL+V.') 
    
# 🆑 всплывающие окно адрес
def click_3_0(): 
    messagebox.showinfo('Информация!', "STR - это разбивка с кавычками '', а\n INT без них.")     
    
# 🆑 всплывающие окно кол-во
def click_3(): 
    messagebox.showinfo('Информация!', 'По умолчанию указано число - 990. '+
                        'Можно заменить вручную на любое.')      
    
# ❌ очистка полей   
def delete():
    
    t.delete(1.0, END)
    #entry_1_1.delete(0, END)
    #entry_1_2.delete(0, END)
    
# ❌  очистка полей       
def delete_2():
    
    t_2.delete(1.0, END)
    #entry_2_1.delete(0, END)
    #entry_2_2.delete(0, END) 
    
# ❌ очистка полей     
def delete_3():
    
    t_3.delete(1.0, END)
    #entry_3_1.delete(0, END)
    #entry_3_2.delete(0, END)     
    
    
INN = ""
ADRESS = "" 
COUNT = ""
#SELECTED = ""    
selected = StringVar(value="STR")
inn_check = StringVar(value="YES_OF_COURSE")

INN_2 = ""
ADRESS_2 = "" 
COUNT_2 = ""
selected_2 = StringVar(value="STR")
inn_check_2 = StringVar(value="YES_OF_COURSE")

INN_3 = ""
ADRESS_3 = "" 
COUNT_3 = ""
inn_check_3 = StringVar(value="YES_OF_COURSE")


#t =  StringVar()
adress = StringVar(value='C:\\')  
count = StringVar(value=990) 


#t =  StringVar()
adress_2 = StringVar(value='C:\\')  
count_2 = StringVar(value=990) 

#t =  StringVar()
adress_3 = StringVar(value='C:\\')  
count_3 = StringVar(value=990) 


# создание вкладок
tab_control = ttk.Notebook(root)
tab_1 = ttk.Frame(tab_control)
tab_2 = ttk.Frame(tab_control)
tab_3 = ttk.Frame(tab_control)
tab_control.add(tab_1, text='Под шапку With Spis_INN',)
tab_control.add(tab_2, text='Через запятую для OR/AND')
tab_control.add(tab_3, text='Для АИСа')

#---------------------------------------------------------
# ******************************************************************************************************
# СТРАНИЦА 1 1️⃣
#Текст

lbl_1 = Label(tab_1, text="Разбивка ИНН по шаблону Spis_inn\n With Spis_INN as(\n        select column_value as INN from\ntable(sys.ODCIVARCHAR2LIST(\n        STR - '0000000001','0000000002','0000000003'\n        INT - 0000000001,0000000002,0000000003)))", 
              background='powder blue',
              foreground = 'Darkorchid4',
              borderwidth = 5,
              height = 6,
              relief=RIDGE,
              padx=135 ,
              font=('Arial', 11)
             ).grid(row=1, column=0,  columnspan=4
                             )

                             
lbl_1_2 = Label(tab_1, text="Вставьте список инн - ",
                #background='CadetBlue2',
              foreground = 'Darkorchid4',
              borderwidth = 5,
              #  relief=RIDGE,
                 height = 2,
               font=('Arial', 11),
               padx=5, pady=5).grid(row=2, column=0)  

lbl_1_3 = Label(tab_1, text="Путь сохранения файла - ",
               #background='CadetBlue2',
              foreground = 'Darkorchid4',
              borderwidth = 5, 
               # relief=RIDGE,
              #height = 2,
               font=('Arial', 11),
                justify = LEFT,
                padx=5, pady=5).grid(row=5, column=0) 

lbl_1_4 = Label(tab_1, text="На какое кол_во ИНН\n делать разбивку - ",
               #background='CadetBlue2',
               foreground = 'Darkorchid4',
               borderwidth = 5,
                #relief=RIDGE,
               #height =2,
               font=('Arial', 11),
                padx=5, pady=5).grid(row=6, column=0) 

# Приемка инфы
t = Text(tab_1, width = 30, height=10, wrap=WORD,)
t.grid(row=2, column=1,)
entry_1_1 = Entry(tab_1, textvariable=adress, width = 40)
entry_1_1.grid(row=5, column=1) 

entry_1_2 = Entry(tab_1, textvariable=count, width = 20)
entry_1_2.grid(row=6, column=1) 

# Кнопки
button = Button(tab_1, text="Выполнить разбивку", command=lambda : [get_address(), work_1(), click()],
                background='powder blue',
                foreground = 'Darkorchid4',
                borderwidth = 3,
                relief=RAISED,
                #height = 1,width = 2, 
                font=('Arial', 12),
               ).grid(row=7, column=1)
button_1 = Button(tab_1, text="?", command= click_1,
                 background='powder blue',
                  foreground = 'DarkGoldenrod1',
                  borderwidth = 3,
                  relief=RAISED,
                  #height = 1,width = 2, 
                font=('Arial', 16),).grid(row=2, column=2)
button_111 = Button(tab_1, text="?", command= click_3_0,
                 background='powder blue',
                  foreground = 'DarkGoldenrod1',
                  borderwidth = 3,
                  relief=RAISED,
                  #height = 1,width = 2, 
                font=('Arial', 16),).grid(row=4, column=2)


button_11 = Button(tab_1, text="!!!", command= click_lang,
                 background='powder blue',
                  foreground = 'red',
                  borderwidth = 3,
                  relief=RAISED,
                  #height = 1,width = 2, 
                font=('Arial', 16),).grid(row=2, column=3)

### 📻 Radiobutton 😃
rad_1_3 = Radiobutton(tab_1, text = 'Проверка ИНН', value = 'YES_OF_COURSE', variable=inn_check,
                      #fg = 'Darkorchid4',
                      
                    #command = work_1
                   )
rad_1_4 = Radiobutton(tab_1, text = 'Без проверки ИНН', value = 'NONE', variable=inn_check, 
                    #command = work_1
                   )

rad_1_1 = Radiobutton(tab_1, text = 'STR(строковые символы\n с кавычками'')', value = 'STR', variable=selected,
                      #fg = 'Darkorchid4',
                      
                    #command = work_1
                   )
rad_1_2 = Radiobutton(tab_1, text = 'INT(числовые символы\n без кавычек)', value = 'INT', variable=selected, 
                    #command = work_1
                   )

#lbl=Label(tab_1, foreground = 'Darkorchid4',
              # borderwidth = 5,               
               #font=('Arial', 11),
          # relief=RIDGE,
                #padx=5, pady=5)

rad_1_1.grid(row=4, column=0, sticky=W, padx = 30)
rad_1_2.grid(row=4, column=1, sticky=W, padx = 30)

rad_1_3.grid(row=3, column=0, sticky=W, padx = 30)
rad_1_4.grid(row=3, column=1, sticky=W, padx = 30)
#lbl.grid(row=3, column=2)


button_2 = Button(tab_1, text="?", command = click_2,
                 background='powder blue',
                  foreground = 'DarkGoldenrod1',
                  borderwidth = 3,
                    relief=RAISED,
                     #height = 1,
                  #width = 2,
                   font=('Arial', 16),).grid(row=5, column=2)
button_3 = Button(tab_1, text="?", command= click_3,
                 background='powder blue',
                  foreground = 'DarkGoldenrod1',
                  borderwidth = 3,
                    relief=RAISED,
                     #height = 2,
                   font=('Arial', 16),).grid(row=6, column=2)
button_del = Button(tab_1, text="Очистить поля", command= delete,
                 background='powder blue',
                  foreground = 'Darkorchid4',
                  borderwidth = 3,
                    relief=RAISED,
                     #height = 2,
                   font=('Arial', 12),).grid(row=7, column=0)
#t.grid(row=2, column=1,)


# СТРАНИЦА 2️⃣ ******************************************************************************
#Текст
lbl_2 = Label(tab_2,
        text="Разбивка ИНН через запятую\n\nSTR - '0000000001','0000000002','0000000003'\n\n\
        INT - 0000000001,0000000002,0000000003",          
          background='peach puff',
          foreground = 'Darkorchid4',
          borderwidth = 6,
             height = 6,
              relief=RIDGE,
              padx=135 ,
              font=('Arial', 11)
             ).grid(row=1, column=0,  columnspan=4
                   )

lbl_2_2 = Label(tab_2, text="Вставьте список инн - ",
                #background='CadetBlue2',
              foreground = 'Darkorchid4',
              borderwidth = 5,
              #  relief=RIDGE,
                 height = 2,
               font=('Arial', 11),
               padx=5, pady=5).grid(row=2, column=0)  

lbl_2_3 = Label(tab_2, text="Путь сохранения файла - ",
               #background='CadetBlue2',
              foreground = 'Darkorchid4',
              borderwidth = 5, 
               # relief=RIDGE,
              #height = 2,
               font=('Arial', 11),
                justify = LEFT,
                padx=5, pady=5).grid(row=5, column=0) 

lbl_2_4 = Label(tab_2, text="На какое кол_во ИНН\n делать разбивку - ",
               #background='CadetBlue2',
               foreground = 'Darkorchid4',
               borderwidth = 5,
                #relief=RIDGE,
               #height =2,
               font=('Arial', 11),
                padx=5, pady=5).grid(row=6, column=0) 

# Приемка инфы
t_2 = Text(tab_2, width = 30, height=10, wrap=WORD,)
t_2.grid(row=2, column=1,)
entry_2_1 = Entry(tab_2, textvariable=adress_2, width = 40)
entry_2_1.grid(row=5, column=1) 
entry_2_2 = Entry(tab_2, textvariable=count_2, width = 20)
entry_2_2.grid(row=6, column=1) 

# Кнопки
button_22 = Button(tab_2, text="Выполнить разбивку", command=lambda : [get_address_2(), work_2(), click_info_2()],
                background='peach puff',
                foreground = 'Darkorchid4',
                borderwidth = 3,
                relief=RAISED,
                #height = 1,width = 2, 
                font=('Arial', 12),
               ).grid(row=7, column=1)


button_111 = Button(tab_2, text="?", command= click_3_0,
                 background='peach puff',
                  foreground = 'Darkorchid4',
                  borderwidth = 3,
                  relief=RAISED,
                  #height = 1,width = 2, 
                font=('Arial', 16),).grid(row=4, column=2)

### 📻 Radiobutton 😃
rad_2_3 = Radiobutton(tab_2, text = 'Проверка ИНН', value = 'YES_OF_COURSE', variable=inn_check_2,
                      #fg = 'Darkorchid4',
                      
                    #command = work_1
                   )
rad_2_4 = Radiobutton(tab_2, text = 'Без проверки ИНН', value = 'NONE', variable=inn_check_2,
                    #command = work_1
                   )

rad_2_1 = Radiobutton(tab_2, text = 'STR(строковые символы\n с кавычками'')', value = 'STR', variable=selected_2,
                      #fg = 'Darkorchid4',
                      
                    #command = work_1
                   )
rad_2_2 = Radiobutton(tab_2, text = 'INT(числовые символы\n без кавычек)', value = 'INT', variable=selected_2, 
                    #command = work_1
                   )

#lbl=Label(tab_1, foreground = 'Darkorchid4',
              # borderwidth = 5,               
               #font=('Arial', 11),
          # relief=RIDGE,
                #padx=5, pady=5)

rad_2_1.grid(row=4, column=0, sticky=W, padx = 30)
rad_2_2.grid(row=4, column=1, sticky=W, padx = 30)

rad_2_3.grid(row=3, column=0, sticky=W, padx = 30)
rad_2_4.grid(row=3, column=1, sticky=W, padx = 30)
#lbl.grid(row=3, column=2)


button_11 = Button(tab_2, text="!!!", command= click_lang,
                 background='peach puff',
                  foreground = 'red',
                  borderwidth = 3,
                  relief=RAISED,
                  #height = 1,width = 2, 
                font=('Arial', 16),).grid(row=2, column=3)

button_2_1 = Button(tab_2, text="?", command= click_1,
                 background='peach puff',
                  foreground = 'Darkorchid4',
                  borderwidth = 3,
                  relief=RAISED,
                  #height = 1,width = 2, 
                font=('Arial', 16),).grid(row=2, column=2)

button_2_2 = Button(tab_2, text="?", command = click_2,
                 background='peach puff',
                  foreground = 'Darkorchid4',
                  borderwidth = 3,
                    relief=RAISED,
                     #height = 1,
                  #width = 2,
                   font=('Arial', 16),).grid(row=5, column=2)

button_2_3 = Button(tab_2, text="?", command= click_3,
                 background='peach puff',
                  foreground = 'Darkorchid4',
                  borderwidth = 3,
                    relief=RAISED,
                     #height = 2,
                   font=('Arial', 16),).grid(row=6, column=2)

button_del = Button(tab_2, text="Очистить поля", command= delete_2,
                 background='peach puff',
                  foreground = 'Darkorchid4',
                  borderwidth = 3,
                    relief=RAISED,
                     #height = 2,
                   font=('Arial', 12),).grid(row=7, column=0)


# СТРАНИЦА 3️⃣ ***************************************************************
# Текст
lbl_3 = Label(tab_3,
        text="Разбивка ИНН для АИСа\n\n 0000000001/0000000002/0000000003",          
          background='PaleGreen2',
          foreground = 'Darkorchid4',
          borderwidth = 8,
             height = 6,
              relief=RIDGE,
              padx=170 ,
              font=('Arial', 11)
             ).grid(row=1, column=0,  columnspan=4
                   )

lbl_3_2 = Label(tab_3, text="Вставьте список инн - ",
                #background='CadetBlue2',
              foreground = 'Darkorchid4',
              borderwidth = 5,
              #  relief=RIDGE,
                 height = 2,
               font=('Arial', 11),
               padx=5, pady=5).grid(row=2, column=0)  

lbl_3_3 = Label(tab_3, text="Путь сохранения файла - ",
               #background='CadetBlue2',
              foreground = 'Darkorchid4',
              borderwidth = 5, 
               # relief=RIDGE,
              #height = 2,
               font=('Arial', 11),
                justify = LEFT,
                padx=5, pady=5).grid(row=4, column=0) 

lbl_3_4 = Label(tab_3, text="На какое кол_во ИНН\n делать разбивку - ",
               #background='CadetBlue2',
               foreground = 'Darkorchid4',
               borderwidth = 5,
                #relief=RIDGE,
               #height =2,
               font=('Arial', 11),
                padx=5, pady=5).grid(row=5, column=0) 

# Приемка инфы
t_3 = Text(tab_3, width = 30, height=10, wrap=WORD,)
t_3.grid(row=2, column=1,)
entry_3_1 = Entry(tab_3, textvariable=adress_3, width = 40)
entry_3_1.grid(row=4, column=1) 
entry_3_2 = Entry(tab_3, textvariable=count_3, width = 20)
entry_3_2.grid(row=5, column=1) 

# Кнопки
button_22 = Button(tab_3, text="Выполнить разбивку", command=lambda : [get_address_3(), work_3(), click_info_3()],
                background='PaleGreen2',
                foreground = 'Darkorchid4',
                borderwidth = 3,
                relief=RAISED,
                #height = 1,width = 2, 
                font=('Arial', 12),
               ).grid(row=6, column=1)

button_11 = Button(tab_3, text="!!!", command= click_lang,
                 background='PaleGreen2',
                  foreground = 'red',
                  borderwidth = 3,
                  relief=RAISED,
                  #height = 1,width = 2, 
                font=('Arial', 16),).grid(row=2, column=3)

button_2_1 = Button(tab_3, text="?", command= click_1,
                 background='PaleGreen2',
                  foreground = 'Darkorchid4',
                  borderwidth = 3,
                  relief=RAISED,
                  #height = 1,width = 2, 
                font=('Arial', 16),).grid(row=2, column=2)

button_2_2 = Button(tab_3, text="?", command = click_2,
                 background='PaleGreen2',
                  foreground = 'Darkorchid4',
                  borderwidth = 3,
                    relief=RAISED,
                     #height = 1,
                  #width = 2,
                   font=('Arial', 16),).grid(row=4, column=2)

button_2_3 = Button(tab_3, text="?", command= click_3,
                 background='PaleGreen2',
                  foreground = 'Darkorchid4',
                  borderwidth = 3,
                    relief=RAISED,
                     #height = 2,
                   font=('Arial', 16),).grid(row=5, column=2)

button_del = Button(tab_3, text="Очистить поля", command= delete_3,
                 background='PaleGreen2',
                  foreground = 'Darkorchid4',
                  borderwidth = 3,
                    relief=RAISED,
                     #height = 2,
                   font=('Arial', 12),).grid(row=6, column=0) 

rad_3_1 = Radiobutton(tab_3, text = 'Проверка ИНН', value = 'YES_OF_COURSE', variable=inn_check_3,                      
                   )
rad_3_2 = Radiobutton(tab_3, text = 'Без проверки ИНН', value = 'NONE', variable=inn_check_3, 
                    #command = work_1
                   )

rad_3_1.grid(row=3, column=0, sticky=S, padx = 30, pady=10)
rad_3_2.grid(row=3, column=1, sticky=S, padx = 30, pady=10)

#butt_1.grid(row=2, column=2)
#butt_2.grid(row=2, column=2)
tab_control.pack(expand=1, fill='both')

py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)

root.mainloop()


# In[ ]:




