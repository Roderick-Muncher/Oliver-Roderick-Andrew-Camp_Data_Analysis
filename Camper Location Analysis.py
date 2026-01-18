import pandas as pd
import matplotlib.pyplot as plt
import copy
import numpy as np #Imports

totallist = []
agelist = []


titles = ["DateOfBirth",
          "ProvinceOfResidence",
          "PostalCode",
          "Country",
          "History"
    ]

GTA = ["L4", "L5", "L6", "L7", "L8", "L9"]

campers = pd.read_excel("CAMP2024.xlsx", header=None)
campersdf = pd.DataFrame(campers)
campersdf.columns = titles 
    
pd.set_option("display.max_rows", None)

campersdfcopy = copy.deepcopy(campersdf) 

historylist = campersdfcopy["History"].tolist()
provincelist = campersdfcopy["ProvinceOfResidence"].tolist()
postalcodelist = campersdfcopy["PostalCode"].tolist()
countrylist = campersdfcopy["Country"].tolist()

totallist = [
    str(history).replace("; ", " ").replace(";", " ").replace(": ", " ").replace(":", " ")
    for history in historylist
]

allyearslist = []

def simplify(x):
  return list(dict.fromkeys(x)) 

for each in campersdf["History"]: 
    templist = [] 
    tempstring = each 
    for i in range(0, len(tempstring) - 4):
        chunks = str(tempstring[i:i+4])
        if chunks.isnumeric() == True:
            templist.append(chunks) 
    allyearslist.append(simplify(templist))

metrodict = {}
gtadict = {}
can_usdict = {}
foreigndict = {}
totaldict = {}

for i in range(1989, 2024):
    metrodict[i] = 0
    gtadict[i] = 0
    can_usdict[i] = 0
    foreigndict[i] = 0
    totaldict[i] = 0

count = []
for i in range(len(historylist)):
    for year in range(1989, 2024):
        if str(year) in allyearslist[i]:
            province = provincelist[i]
            postal = postalcodelist[i]
            country = countrylist[i]
            if type(postal) == str and postal[0] == 'M':
                metrodict[year] += 1
            elif type(postal) == str and postal[:2] in GTA:
                gtadict[year] += 1
            elif type(province) == str:
                can_usdict[year] += 1
            else:
                foreigndict[year] += 1             
            totaldict[year] += 1

metrodictper = {}
gtadictper = {}
can_usdictper = {}
foreigndictper = {}

for i in range(1989, 2024):
    metrodictper[i] = 0
    gtadictper[i] = 0
    can_usdictper[i] = 0
    foreigndictper[i] = 0
    if totaldict[i] == 0:
        totaldict[i] = 1

for i in range(1989, 2024):
    metrodictper[i] = 100 * metrodict[i] / totaldict[i]
    gtadictper[i] = 100 * gtadict[i] / totaldict[i]
    can_usdictper[i] = 100 * can_usdict[i] / totaldict[i]
    foreigndictper[i] = 100 * foreigndict[i] / totaldict[i]
    
#print(postal, province, country, year)
data = np.array([list(metrodictper.values()), list(gtadictper.values()), list(can_usdictper.values()), list(foreigndictper.values())])

years = list(totaldict.keys()) 

x = np.arange(len(years)) 

labels = ["METRO", "GTA", "CAN_US", "FOREIGN"]
hexcodes = ['#0000AA', '#00BB00', '#001467', '#010101'] #Forest green, teal, charcoal, tears
colours = ['#FF0000', '#BBDD00', '#00CC00', '#0000EE']

fig, ax = plt.subplots() 

bars = []  
for i in range(0, 4): 
    bar = ax.bar(x + 0.3, data[i], bottom=np.sum(data[:i], axis=0), label=labels[i], color=hexcodes[i])
    bars.append(bar)  

ax.set_ylabel("Percentage of Campers, Per Group") 
ax.set_xlabel("Years") 
ax.set_title("Percentage of Campers Per Group, Per Year") 
ax.legend(bbox_to_anchor=(0.99, 0.65)) 

ax.set_xticks(x + 0.3)
ax.set_xticklabels(years, rotation=90, fontsize=7)

plt.tight_layout() 
plt.show() 

print("")
print(" YEAR     METRO    GTA    CAN_US    FOREIGN ")
print("---------------------------------------------")
for i in range(1989, 2024):
    if i != 2020:
        print(f' {i}:   {metrodictper[i]:.2f}%   {gtadictper[i]:.2f}%   {can_usdictper[i]:.2f}%   {foreigndictper[i]:.2f}%')
    else:
        print(" 2020:   NO CAMPERS THIS YEAR")
