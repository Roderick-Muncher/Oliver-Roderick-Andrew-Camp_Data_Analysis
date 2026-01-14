import pandas as pd
import matplotlib.pyplot as plt
import copy

MOOSE = ["1993", "2010"]
ReusedNames = ["CHIP", "SLICK", "DRIFT", "MEC", "JEMIMA", "UTAH", "BAUER", "GILLIGAN", "OX", "CRUSH"] #These leaders had same name but worked multiple times
Cutoff = [2005, 2005, 2005, 2005, 2011, 2005, 2005, 2005, 1998, 2015] #Cutoff years for these leaders
namesout = ["FUSION", "WORK", "PROGRAM", "PRO", "LIT", "2)", "SN", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(sent", "-", "(N)", " ", "sent", "home", "on", "day"]
totallist = []
newlist = []
agelist = [] 
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

campersdfcopy = copy.deepcopy(campersdf) #Saveacopy for easy access/working with it

historylist = campersdfcopy["History"].tolist() #List that sorts everything horizontally (Will be used better)

totallist = [
    str(history).replace("SEQWAY", "SEGWAY").replace("; ", " ").replace(";", " ").replace(": ", " ").replace(":", " ")
    for history in historylist
] #Replace all semicolons, colons, and typos found in the document

newlist2 = [] #define new list used temporarily to store data and then sort it
    
for each in totallist: #Look through every data point
    templist = []
    templist2 = [] #Two temporary lists to split the data into the two new lists, cleared per cycle
    tempstring = each #save each (optional, but makes it easier to work with)
    j = 0 #Start a secondary counter (looking at length of the string)
    for i in range(0, len(tempstring) + 1):
        chunks = str(tempstring[i:i+4]) #Find all chunks in the file
        if chunks.isnumeric() == True or i == len(tempstring):
            segment = str(tempstring[j:i])
            while segment.endswith(' '): #Cut off any additional spaces
                segment = segment[:-1]
            templist.append(segment) #New part is properly formatted
            j = i #Set the secondary counter which sets a new start point to build a new chunk
    templist = [segment for segment in templist if len(segment.split()) >= 3] #Gets rid of odd entries such as a blank space
    for each in templist:
        newlist.append(each) #build new list, with values in one type of format (all in one row)
        templist2.append(each.split(" ")) #build the same list, but this time which each section having its own list (makes it easy to work with)
    newlist2.append(templist2) #Another new list, but formatted differently (defined previously) and is used later

data = copy.deepcopy(newlist) #Copy the data to work with easily

totalcampersthatyear_person = {}
totalreturneesthatyear_person = {} #Create new dictionaries for campers and returnees

for i in range(1989, 2019): #loop through every year to make a dictionary for every year
    totalcampersthatyear_persontemp = {} #We want to add dictionaries for every year into a larger dictionary
    for each in newlist2:
        for segment in each: #Looping through every camper and every chunk (session) for that camper
            if segment[0] == str(i): #check if the year is correct
                for name in segment[2:]: #Check the name
                    if name in totalcampersthatyear_persontemp and name not in namesout: #See if the name exists already
                        totalcampersthatyear_persontemp[name] += 1 #Add one to counter
                    if name not in totalcampersthatyear_persontemp and  name not in namesout:
                        totalcampersthatyear_persontemp[name] = 1 #If the name doesn't exist yet, create it
    totalcampersthatyear_person[i] = totalcampersthatyear_persontemp #Apped the year's dictionary to the total

newlist3 = [] #Another list used to store data
savedlist = copy.deepcopy(newlist2)

for each in newlist2:
    if len(each) >= 2: #If the person goes to camp more than onece, then run this
        del each[0] #Delete the first instance as that signifies someone is not a returnee
        newlist3.append(each) #Add the values to a new list
        
for i in range(1989, 2019):
    totalcampersthatyear_persontemp = {} #again, we want dictionaries for every year (looking at returnees this time, however)
    for each in newlist3:
        for segment in each:
            if segment[0] == str(i): #Check the year to make sure it corresponds
                for name in segment[2:]: #This time, the new list doesn't include the non-returnees, so look through everything
                    if name in totalcampersthatyear_persontemp and name not in namesout: #See if the name exists already
                        totalcampersthatyear_persontemp[name] += 1 #Add one to counter
                    if name not in totalcampersthatyear_persontemp and  name not in namesout:
                        totalcampersthatyear_persontemp[name] = 1 #If the name doesn't exist yet, create it

    totalreturneesthatyear_person[i] = totalcampersthatyear_persontemp #Update returnees dictionary

for i in range(1989, 2019): #Some returnees dont exist, so just set 0 as their value (easy to match) - Look through every year
    for key in totalcampersthatyear_person[i]:
        if key not in totalreturneesthatyear_person[i]:
            (totalreturneesthatyear_person[i])[key] = 0 

tempsessionyearcount = {} #number of sessions per year

# Iterate over each year from 1989 to 2018
for i in range(1989, 2019):
    tempsessionyearcount[i] = {}  # Initialize the dictionary for the year
    
    # Iterate over each entry in the saved list
    for each in savedlist:
        for segment in each:
            year = int(segment[0])
            if year == i:
                segment_id = segment[1] #Take Camp code
                for name in segment[2:]:
                    if name in tempsessionyearcount[i] and name not in namesout: 
                        tempsessionyearcount[i][name].append(segment_id) #If the name is already in the dictionary for the current year
                        #Add the segment_id to the list associated with the name
                    if name not in tempsessionyearcount[i] and name not in namesout:  #If name isn't in the dictionary yet
                        tempsessionyearcount[i][name] = [segment_id]  # Create a new list with segment_id and add it to the dictionary if it doesn't exist
XVALS = [] 
YVALS = []
#List for xvalues and yvalues of scatterplot

for i in range(1989, 2019):
    mydict = tempsessionyearcount[i] #for every year, look at a person's sessions
    for key in mydict:
        unique_count = len(set(mydict[key])) #use a set to get rid of duplicates and count number of sessions for that person
        mydict[key] = unique_count #Now, replace the original value in that dictionary (sessions) with simply the number
        XVALS.append(unique_count) #Add this x-value

for i in range(1989, 2019):
    dict1 = totalcampersthatyear_person[i] #Grab year from total campers
    dict2 = totalreturneesthatyear_person[i] #Grab that same year from total returnees
    for key in dict1:
        aval = dict1[key] #Total campers for one counselor
        bval = dict2[key] #Total returnees for one counselor (that year)
        YVALS.append(100 * bval/aval) #Calculate percentage return

group_data = {} #dictionary for the group

for i in range(len(XVALS)):
    group = XVALS[i] #XVALS stores the group names
    value = YVALS[i] #YVALS stores the individual values
    if group not in group_data:
        group_data[group] = {'sum': 0, 'count': 0} #dictionary for sum and count for each number of sessions (AVG LINE)
    group_data[group]['sum'] += value
    group_data[group]['count'] += 1
#Find total sum and total count to be used to calculate avg

# Dictionary to hold the average results
averages = {}

# Display the sorted dictionary

# Calculate the averages, as we found sum and count for each
for group in group_data:
    avg = group_data[group]['sum'] / group_data[group]['count'] #Average calculation
    averages[group] = avg #Extract data from the dictionary and get it so that each value corresponds to the average

xline = []
yline = [] #X and Y points for the line

sortedaverages = dict(sorted(averages.items())) #Sort them in ascending order so that line graph can be properly plotted

for key in sortedaverages:
    xline.append(key) #Add key (number of sessions) to xlist
    yline.append(sortedaverages[key]) #Add percentage to ylist

plt.scatter(XVALS, YVALS, marker='.', color='purple', label='Staff Performance')

plt.xlabel('Number of Sessions per Year')
plt.ylabel('Percent Return')
plt.title('Percent Return vs. Number of Sessions')
#Labels for the plot

plt.plot(xline, yline, color='red', label='Average return rate') #Create line for the average return rate

plt.legend()
plt.tight_layout()
plt.show()
#Show legend and plot
        