# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 15:14:52 2017

@author: Tiago Monteiro
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import csv

def offset(x, l):
    valorOffset = x / l
    return valorOffset


def subtrairOffset (*a):
    b = []
    l=len(a)
    offsetAF3 = offset(sum(a), l)
    for i in range (0, l ): 
        val = a[i]
        val = val - offsetAF3
        b.append(val)
    return b

def dottohifen(Path):
    
    filelist = os.listdir(Path)
    for i in filelist:
        if i.endswith('.edf'):
            os.rename(os.path.join(Path, i), os.path.join(Path, i.replace('.' , '-')))

def correctextension1(Path):
    
    [os.rename(f, f.replace('-csv', '.csv')) for f in os.listdir(Path) if not f.endswith('-edf')]

def correctextension2(Path):
    
    filelist = os.listdir(Path)
    for i in filelist:
        if i.endswith('-edf'):
            os.rename(os.path.join(Path, i), os.path.join(Path, i.replace('-edf' , '.edf')))
    
#    [os.rename(f, f.replace('-', '.')) for f in os.listdir('.') if not f.endswith('.edf')]
def correctextension3(Path):
    filelist = os.listdir(Path)
    for i in filelist:
        if i.endswith('.csv.txt'):
            os.rename(os.path.join(Path, i), os.path.join(Path, i.replace('.csv.txt' , '.txt')))

def csvtotxt(Path):
    
    filelist = os.listdir(Path)
    print(filelist)
    for i in filelist:
        if i.endswith(".csv"):  # You could also add "and i.startswith('f')
            print(i)
            text_list = []
            with open(Path + i, "r") as f:
                for line in f:
                    line = line.split(",", 2)
                    text_list.append(",".join(line))
                
            with open(Path + i + ".txt", "w") as o:
                #    my_output_file.write("#1\n")
                    #    my_output_file.write("double({},{})\n".format(len(text_list), 2))
                for line in text_list[1:]:
                    o.write(line)
                print('File Successfully written.')

def csvtoexcel(Path):
    
    import os
    import glob
    import csv
    from xlsxwriter.workbook import Workbook
    
    
    for csvfile in glob.glob(os.path.join('.', '*.csv')):
        workbook = Workbook(csvfile[:-4] + '.xlsx')
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()
        
        
    
                
def SinalRaw(Path):
    filelist = os.listdir(Path)
    for i in filelist:
        if i.endswith(".txt"):
            signal = np.loadtxt(i,delimiter=',',usecols=range(2,16),skiprows=1)
            l = len(signal)
            time = []
            t = 1/256; #periodo do sinal. Diretamente proporcional com a frequencia de amostragem
            for y in range (0, l):
                tempo = t * y
                time.append(tempo)
            
#representação e save do sinal bruto de entrada
#            fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
 #           ax.plot(time, signal)
  #          fig.savefig(Path + i + '.png') 
   #         plt.close(fig) 
    #        plt.show
            
            AF3 = np.array(signal[:,0]); F7 = np.array(signal[:,1])
            F3 = np.array(signal[:,2]); FC5 = np.array(signal[:,3])
            T7 = np.array(signal[:,4]); P7 = np.array(signal[:,5])
            O1 = np.array(signal[:,6]); O2 = np.array(signal[:,7])
            P8 = np.array(signal[:,8]); T8 = np.array(signal[:,9])
            FC6 = np.array(signal[:,10]); F4 = np.array(signal[:,11])
            F8 = np.array(signal[:,12]); AF4 = np.array(signal[:,13])
            
            #Subtração do offset
            AF3 = subtrairOffset (*AF3); F7 = subtrairOffset (*F7)
            F3 = subtrairOffset (*F3); FC5 = subtrairOffset (*FC5)
            T7 = subtrairOffset (*T7); P7 = subtrairOffset (*P7)
            O1 = subtrairOffset (*O1); O2 = subtrairOffset (*O2)
            P8 = subtrairOffset (*P8); T8 = subtrairOffset (*T8)
            FC6 = subtrairOffset (*FC6); F4 = subtrairOffset (*F4)
            F8 = subtrairOffset (*F8); AF4 = subtrairOffset (*AF4)
                        
            #Junção dos sinais sem OFFSET 
            signal2 = np.column_stack((AF3,F7, F3, FC5, T7, P7, O1, O2, P8, T8, FC6, F4, F8, AF4))
            fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
            ax.plot(time, signal2)
            fig.savefig(Path + i + 'SemOffset.png') 
            plt.close(fig)



Path = input("path of the txt files: ")
ans=True
while ans==True:
    print ("""
    1. Dot to Hifen (mantem .edf)
    2. -csv to .csv 
    3. -edf to .edf
    4. .csv to .txt
    5. .txt.csv to .txt
    6. .png dos sinais raw
    
    """)
    ans=input("Que operação?") 
    if ans=="1": 
        dottohifen(Path) 
        correctextension2(Path)
    elif ans=="2":
        correctextension1(Path)
    elif ans=="3":
        correctextension2(Path)
    elif ans=="4":
        csvtoexcel(Path) 
    elif ans=="5":
        correctextension3(Path) 
    elif ans=="6":
        SinalRaw(Path)
    elif ans !="":
      print("\n Not Valid Choice Try again") 
