import pandas as pd
import matplotlib.pyplot as plt #Imports

percentdict = {}
onetimedict = {}
totaldict = {} #Create dictionaries to store onetimers and averages
for i in range(36): #Create a key for each year inside the dictionary
    onetimedict[str(1989 + i)] = 0
    totaldict[str(1989 + i)] = 0
    percentdict[str(1989 + i)] = 0 
    
alist = []
dflist = []
totallist = [] #Creating lists to be used in calculations process
titles = ["DateOfBirth",
          "ProvinceOfResidence",
          "PostalCode",
          "Country",
          "History"
    ] #Titles for dataframe from excel sheet

campers = pd.read_excel("CAMP2024.xlsx", header=None) #Open and read the excel file, taking the values out
campersdf = pd.DataFrame(campers)
campersdf.columns = titles #Add titles to dataframe for easy access
    
pd.set_option('display.max_rows', None) #Option to allow for easy printing of df in console

allyearslist = []

def simplify(x):
  return list(dict.fromkeys(x)) #Function that removes duplicates from a dictionary and returns it as a list

for each in campersdf["History"]: #Search through camper history column in the dataframe
    templist = [] #Temporary variable to loop through, cleared per cycle
    tempstring = each #Temporary variable to loop through, cleared per cycle
    for i in range(0, len(tempstring) - 4):
        chunks = str(tempstring[i:i+4]) #Grab 4 digit chunks, which are the years
        if chunks.isnumeric() == True:
            templist.append(chunks) #Chunks allow us to split the data apart
    allyearslist.append(simplify(templist))
    
    if len(templist) == 1 or all(x == templist[0] for x in templist): #If its a one timer: look at if its only one session (or one year)
        onetimedict[templist[0]] += 1 #Counter
        
    for each in templist: 
        totaldict[each] += 1 #Add one to total, no matter what

totalonetime = 0
totalalltime = 0 #Counters to find overall average
for year in onetimedict:
   if int(year) > 1989 and int(year) < 2019: #Filter it out to find percentages, only for years below 2019
       percentdict[year] = int(onetimedict[year]) / int(totaldict[year]) #Percent calculation - onetime divided by total
       totalonetime += int(onetimedict[year])
       totalalltime += int(totaldict[year])

xlist = []
ylist = []
#X and Y List to plot the points on the line graph

for year in percentdict:
   if int(year) > 1989 and int(year) < 2019:
       xlist.append(year) #add points to xlist and ylist
       ylist.append(float(percentdict[year]) * 100) #Multiple by 100 for whole number
      
#Plot the graph, add all its properties
plt.figure(figsize=(15, 8))
plt.plot(xlist, ylist, "-", color="blue", lw=2, marker='o')
plt.xticks(fontsize=8, rotation=90)

plt.xlabel('Year')
plt.ylabel('One-Timers Percentage (%)') #Create axis titles

for i in range(len(xlist)):
    plt.annotate(f'{ylist[i]:.1f}%', (xlist[i], ylist[i]), textcoords="offset points", xytext=(2,7), ha='center', fontsize=10)
#Show rounded percentages

plt.show() #Display Plot

#Calculate total averages

print(f'From 1990 to 2018, {(100 * totalonetime / totalalltime):.3f}% of campers were onetimers')
