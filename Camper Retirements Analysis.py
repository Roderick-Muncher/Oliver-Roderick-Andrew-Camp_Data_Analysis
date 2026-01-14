import pandas as pd
import matplotlib.pyplot as plt
import copy
import numpy as np #Imports

namesout = ["FUSION", "WORK", "PROGRAM", "PRO", "LIT", "2)", "SN", "SN3", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(sent", "-", "(N)"]   # Values to skip which may interfere with the logic
# Defines empty lists used throughout this program
totallist = []
agelist = []

# Defines new names for the columns of the dataframe
titles = ["DateOfBirth",
          "ProvinceOfResidence",
          "PostalCode",
          "Country",
          "History"
    ]

sections = ["RO", "FR", "RA", "VO"] # Sessions the program looks through

# Opens the CAMP2025.xlsx into a dataframe
campers = pd.read_excel("CAMP2024.xlsx", header=None)
campersdf = pd.DataFrame(campers)
campersdf.columns = titles   # Sets the column names to the titles
    
pd.set_option("display.max_rows", None)

campersdfcopy = copy.deepcopy(campersdf) # Creates a deep copy of campersdf so modifications can be made independently from campersdf

historylist = campersdfcopy["History"].tolist() # Storing all rows in the "History" column in a list

# Removes all semicolons and colons from the dataset to separate leaders
totallist = [
    str(history).replace("; ", " ").replace(";", " ").replace(": ", " ").replace(":", " ")
    for history in historylist
]

retirelist = []

# Splits the rows of their spaces
for each in totallist:
    each = each.split(" ")
    retirelist.append([int(each[0]), str(each[1])[0:2]])

# Defines dictionaries to store values for each session and the total
totaldict, RODICT, FRDICT, RADICT, VODICT = {}, {}, {}, {}, {}

# Creates keys from 2001-2018 with placeholders of 0
for i in range(2001, 2019):
    RODICT[i] = 0
    FRDICT[i] = 0
    RADICT[i] = 0
    VODICT[i] = 0
    totaldict[i] = 0 #Total dictionary (NOT USED FOR GRAPH, WAS JUST USED TO TEST IF DATA WAS WORKING)

# Determines the number of each session in a camper's history
for each in retirelist:
    numyear = each[0]
    section = each[1]
    if numyear >= 2001 and numyear <= 2018:   # Defines the range of years (2001-2018)
        if section == "RO": #If the camper was in an RO session, it is added to its dictionary
            RODICT[numyear] += 1
        if section == "FR": #If the camper was in an FR session, it is added to its dictionary
            FRDICT[numyear] += 1
        if section == "RA": #If the camper was in an RA session, it is added to its dictionary
            RADICT[numyear] += 1
        if section == "VO": #If the camper was in an VO session, it is added to its dictionary
            VODICT[numyear] += 1
        
data = np.array([list(RODICT.values()), list(FRDICT.values()), list(RADICT.values()), list(VODICT.values())]) # Puts all the values for sessions in one array

years = list(totaldict.keys()) #Creates a list of years from 2001-2018

x = np.arange(len(years)) #Defines the number of xticks for future logic

# Plot the stacked bar chart
fig, ax = plt.subplots() #Create a figure and axis object

bars = []  # Initialize a list to store the bars for each section
for i in range(0, 4): #Iterate through each section
    # Plot a stacked bar for each section with a width offset for visual separation
    bar = ax.bar(x + 0.2, data[i], bottom=np.sum(data[:i], axis=0), label=str(sections[i]))
    bars.append(bar)  # Append the bar to the list

# Annotate bars with total values
totals = np.sum(data, axis=0) # Calculate the total values for each year
for i in range(len(totals)): # Iterate through each year
    # Add text annotation for the total value on top of each bar
    ax.text(x[i]+0.2, totals[i], int(totals[i]), ha="center", va="bottom", size=8)

# Add labels and title
ax.set_ylabel("Values") # Set the y-axis label
ax.set_xlabel("Years") # Set the x-axis label
ax.set_title("Camper Retirements Per Section, Per Year") # Set the title of the plot
ax.legend(bbox_to_anchor=(1.01, 1.05)) # Add a legend outside the plot area

ax.set_xticks(x + 0.2)  # Set the x-ticks in the middle of the grouped bars
ax.set_xticklabels(years, rotation=45) # Set the year labels with rotation for better readability

plt.tight_layout() # Adjust layout to prevent overlap
plt.show() # Display the plot
