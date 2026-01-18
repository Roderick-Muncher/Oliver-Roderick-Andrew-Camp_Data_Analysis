import pandas as pd
import matplotlib.pyplot as plt
import copy
import heapq #Imports Used

#List all necessary values e.g. cutoff years, reused names (Mr. Smith), and titles for df
MOOSE = ["1993", "2010"] #Moose has special cutoff years
ReusedNames = ["CHIP", "SLICK", "DRIFT", "MEC", "JEMIMA", "UTAH", "BAUER", "GILLIGAN", "OX", "CRUSH"] #These leaders had same name but worked multiple times
Cutoff = [2005, 2005, 2005, 2005, 2011, 2005, 2005, 2005, 1998, 2015] #Cutoff years for these leaders
namesout = ["FUSION", "WORK", "PROGRAM", "PRO", "LIT", "2)", "SN", "SN3", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(sent", "-", "(N)"]
totallist = []
newlist = [] #Lists used for calculation
titles = ["DateOfBirth",
          "ProvinceOfResidence",
          "PostalCode",
          "Country",
          "History"
    ]
#Titles used for DataFrame

#Open and read file
campers = pd.read_excel("CAMP2024.xlsx", header=None)
campersdf = pd.DataFrame(campers)
campersdf.columns = titles #Set columns of DF for easy access
    
pd.set_option("display.max_rows", None) #Max rows line to look at entire dataframe in console

campersdfcopy = copy.deepcopy(campersdf) #Create a copy to work with

historylist = campersdfcopy["History"].tolist() #List that sorts everything horizontally (Will be used better)

totallist = [
    str(history).replace("SEQWAY", "SEGWAY").replace("; ", " ").replace(";", " ").replace(": ", " ").replace(":", " ")
    for history in historylist
] #Replace all semicolons, colons, and typos found in the document

for each in totallist:
    templist = [] #Temporary list use to look at each camper"s history
    tempstring = each
    j = 0
    for i in range(0, len(tempstring) + 1):
        chunks = str(tempstring[i:i+4]) #Find all chunks in the file
        if chunks.isnumeric() == True or i == len(tempstring):
            segment = str(tempstring[j:i])
            while segment.endswith(' '): #Cut off any additional spaces
                segment = segment[:-1] #Delete the end
            templist.append(segment) #new part is properly formatted
            j = i
    templist = [segment for segment in templist if len(segment.split()) >= 3] #Gets rid of odd entries such as a blank space
    for each in templist:
        newlist.append(each) #build new list

data = copy.deepcopy(newlist) #Copy the data to work with easily

#If one counselor hosts the same camper twice, that camper is counted twice

name_count = {} #Dictionary to begin storing number of campers

for entry in data: #Again, filter through all of the data points (processed once already)
    parts = entry.split() #Split the history so that it is easy to work with
    year = int(parts[0]) #the first part of the history is the year
    names = parts[2:]  # Any element after first 2 is a counselor name
    for name in names:
        if name not in namesout and name not in ReusedNames and name != "MOOSE":
            if name in name_count: #Count the number of times the name appears
                name_count[name] += 1 #Add one to counter
            else:
                name_count[name] = 1 #Create the new value in the dictionary if it doesn't exist yet
        if name in ReusedNames and name != "MOOSE": #Restrictions for two people with same name
            newname = name + " No.2" #Create a second name for them
            index = ReusedNames.index(name)
            ctyear = Cutoff[index]
            if ctyear >= year: #Looking at cutoff year to determine which one it is
                if name in name_count:
                    name_count[name] += 1 #Add one to counter
                else:
                    name_count[name] = 1 #If the name doesn't exist yet, create it
            else: 
                if newname in name_count:
                    name_count[newname] += 1 #Add one to counter (to track special name)
                else:
                    name_count[newname] = 1 #If the name doesn't exist yet, create it
        if name == "MOOSE": #Moose is a special case as he exists 3 times
            newname1 = "MOOSE No.2"
            newname2 = "MOOSE No.3" #Create the new names for Moose
            ctyear1 = int(MOOSE[0])
            ctyear2 = int(MOOSE[1]) #Create the cutoff years
            if ctyear1 >= year: #Looking at cutoff year to determine which one it is
                if name in name_count:
                    name_count[name] += 1 #Add one to counter (to track special name)
                else:
                    name_count[name] = 1 #If the name doesn't exist yet, create it
            elif year <= ctyear2: #Looking at cutoff year to determine which one it is
                if newname1 in name_count:
                    name_count[newname1] += 1 #Add one to counter (to track special name)
                else:
                    name_count[newname1] = 1 #If the name doesn't exist yet, create it
            else:
                if newname2 in name_count: 
                    name_count[newname2] += 1 #Add one to counter (to track special name)
                else:
                    name_count[newname2] = 1 #If the name doesn't exist yet, create it

mostcampers = heapq.nlargest(15, name_count, key=name_count.get) #Use heap built-in function to find top 15

yvalues = [] #Create list for yvalues
for each in mostcampers: 
    yvalues.append(name_count[each]) #yvalues for new graph, add to list

bars = plt.bar(mostcampers, yvalues, color="red") #Make first plot of leaders with most campers

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha="center", va="bottom", size=8)
#Grab height of bar and put the corresponding value above the bar

#Build the graph

plt.xticks(fontsize=8, rotation=90)
plt.xlabel("Leader Name")
plt.ylabel("Number of Campers") #Axis titles
plt.show() #Show the graph

data2 = copy.deepcopy(data) #Create a copy of the data to easily work with
newlist2 = [] #new
for each in data2: 
    num = each.split(" ") #Split the history value so that it can be worked with
    for i in range(2, len(num)):
        newpart = f"{num[0]} {num[1]} {num[i]}" #split the value so that unique counselors are recognized
        #for example: 2020 FR2 JOE;BOB -> 2020 FR2 JOE, 2020 FR2 BOB
        newlist2.append(newpart) #Save it all to another list
        
time_count = {} #Dictionary for sessions

def simplify(x):
  return list(dict.fromkeys(x)) #Function that removes duplicates from a dictionary and returns it as a list

newlist3 = simplify(newlist2) #Simplify the old list, which gets rid of duplicate sessions

for entry in newlist3:
    parts = entry.split() #Split the history into parts that are easy to work with
    names = parts[2:] #The camp counselor names are found after the session and code are given
    year = int(parts[0]) #Save the year
    for name in names:
        if name == "SEQWAY":
            name = "SEGWAY" #Replace seqway, a typo in the doc, for segway
        if name not in namesout and name not in ReusedNames and name != "MOOSE": #For names who are only used once
            if name in time_count:
                time_count[name] += 1
            else:
                time_count[name] = 1
        if name in ReusedNames and name != "MOOSE": #For the names that are used twice
            newname = name + " No.2" #Automatically create new name, called "no. 2", for that person
            index = ReusedNames.index(name)
            ctyear = Cutoff[index] #Refer to their cutoff year, found in a predetermined list
            if ctyear >= year: #Check if it below cutoff year (then it will be no.1)
                if name in time_count: #Check if it exists already
                    time_count[name] += 1 #Add one to counter
                else:
                    time_count[name] = 1 #Create it if it doesn't exist
            else: #Else, it will be above the cutoff year (then it will be no.2)
                if newname in time_count: #Check if it exists already
                    time_count[newname] += 1 #Add one to counter
                else:
                    time_count[newname] = 1#Create it if it doesn't exist
        if name == "MOOSE":
            newname1 = "MOOSE No.2"
            newname2 = "MOOSE No.3" #Create exceptions for MOOSE, as he was used 3 times
            ctyear1 = int(MOOSE[0])
            ctyear2 = int(MOOSE[1]) #Take in moose's custom cutoff years
            if ctyear1 >= year: #Looking at cutoff year to determine which one it is
                if name in time_count:
                    time_count[name] += 1 #Add one to counter (to track special name)
                else:
                    time_count[name] = 1 #If the name doesn't exist yet, create it
            elif year <= ctyear2: #Looking at cutoff year to determine which one it is
                if newname1 in time_count:
                    time_count[newname1] += 1 #Add one to counter (to track special name)
                else:
                    time_count[newname1] = 1 #If the name doesn't exist yet, create it
            else:
                if newname2 in time_count: 
                    time_count[newname2] += 1 #Add one to counter (to track special name)
                else:
                    time_count[newname2] = 1 #If the name doesn't exist yet, create it

mostsessions = heapq.nlargest(15, time_count, key=time_count.get) #Use heapq to find top 15 values

y2values = [] #Second list for y values (session bar graph)
for each in mostsessions: 
    y2values.append(time_count[each]) #Add the y value to the list

bars = plt.bar(mostsessions, y2values, color="green") #Create the bar graph and bars

for bar in bars:
    yval = bar.get_height() #Grab the bar's maximum value
    plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha="center", va="bottom", size=8)
    #Insert the value of the bar on top of each bar

plt.xticks(fontsize=8, rotation=90) #Set xticks for the graph (graph properties)
plt.xlabel("Leader Name")
plt.ylabel("Number of Sessions") #Axis labels for the new bar graph
plt.show()
#Show the new bar graph