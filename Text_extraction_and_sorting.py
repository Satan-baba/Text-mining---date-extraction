


import pandas as pd

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)

def date_sorter():
    import re
    import datetime
    f11 = df.str.extractall(r'(\d{1,2})[-/](\d{1,2})[-/](\d{4})\b')
    f12 = df.str.extractall(r'(\d{1,2})[-/](\d{1,2})[-/](\d{2})\b')
    f12[2] = '19' + f12[2]
    f1 = pd.concat([f11,f12])
    f1.reset_index(inplace = True)
    f1_index = f1['level_0']
    f2 = df.str.extractall(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-.,]*) (\d{2}[,-]*) (\d{4})')
    f2.reset_index(inplace = True)
    f2_index = f2['level_0']
    f35 = df.str.extractall(r'((?:\d{1,2} ))?((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[?:.,-]* )(\d{4})')
    f35.reset_index(inplace = True)
    f35_index = f35['level_0']
    f6 = df.str.extractall(r'((?:\d{1,2}))(/)(\d{4})') 
    f6.reset_index(inplace = True)
    f6_index = f6['level_0']
    rn = []
    for i in f6_index:
        if not (i in f1_index.values):
            rn.append(i)
    f6 = f6[f6['level_0'].isin(rn)]
    f71= df.str.extractall(r'[a-z]?[^0-9](\d{4})[^0-9]')
    f72 = df.str.extractall(r'^(\d{4})[^0-9]')
    f7 = pd.concat([f71,f72])
    f7.reset_index(inplace = True)
    f7_index = f7['level_0']
    rn1 = []
    for i in f7_index:
        if not ((i in f6_index.values)|(i in f2_index.values)|(i in f35_index.values)):
                   rn1.append(i)
    f7 = f7[f7['level_0'].isin(rn1)]
    f1['new'] = f1[0] + '/' + f1[1] + '/' + f1[2] 
    f1['new1'] = pd.to_datetime(f1['new'], format = '%m/%d/%Y') #f1 format
    mon = []
    dat = []
    for i in f2[0]:
        mon.append(i[:3])
    mon = pd.Series(mon)
    f2['mon'] = mon
    for i in f2[1]:
        dat.append(i[:2])
    dat = pd.Series(dat)
    f2['dat'] = dat
    f2['new'] = f2['dat'] + f2['mon'] + f2[2]
    fin = []
    for i in range(len(f2)):
        fin.append(datetime.datetime.strptime(f2['new'][i],'%d%b%Y'))
    fin = pd.Series(fin)
    f2['new1'] = fin
    f2#final format
    f35[0] = f35[0].fillna('1 ')
    mon1 = []
    for i in f35[1]:
        mon1.append(i[:3])
    mon1 = pd.Series(mon1)
    f35['mon1'] = mon1
    f35['new'] = f35[0]+f35['mon1']+f35[2]
    fin1 = []
    for i in range(len(f35)):
        fin1.append(datetime.datetime.strptime(f35['new'][i],'%d %b%Y'))
    fin1 = pd.Series(fin1)
    f35['new1'] = fin1 #finalformal
    f6['new'] = f6[0] + '/' + '1' + '/' + f6[2]
    f6['new1'] = pd.to_datetime(f6['new'], format = '%m/%d/%Y')  #finalformal f6
    f7['new'] = '1'+'/'+'1'+'/'+f7[0]
    f7['new1'] = pd.to_datetime(f7['new'], format = '%m/%d/%Y')
    frame = [f1[['level_0','new1']], f2[['level_0','new1']], f35[['level_0','new1']], f6[['level_0','new1']], f7[['level_0','new1']]]
    final = pd.concat(frame)
    final.sort_values('new1', inplace = True)
    final.reset_index(inplace = True)
    final['level_0']
    return final['level_0']

