# Camp Data Analysis 2024

A comprehensive data analysis project examining camper demographics, retention patterns, counselor performance, and geographic distribution for summer camp operations.

## 📊 Project Overview

This project analyzes camp data from 2024 to provide insights into:
- Camper location distribution
- Camper retention and retirement patterns
- Counselor performance metrics
- First-time vs. returning camper statistics

## 🗂️ Repository Contents

### Data
- `CAMP2024 - Copy.xlsx` - Source data file containing camper and counselor information

### Analysis Scripts
- `Camper Location Analysis.py` - Analyzes geographic distribution of campers
- `Camper Retirements Analysis.py` - Examines patterns in camper departures and retirement
- `Number of Campers-Sessions per Counselor All Time. py` - Evaluates counselor workload and performance
- `Percentage of One Time Campers. py` - Calculates retention metrics for first-time campers
- `Number of Sessions to Camper Retention Analysis.py` - Studies the relationship between session attendance and retention

## 📈 Visualizations

### Camper Location Analysis
![Camper Location Analysis](Camper%20Location%20Analysis.png)

This visualization shows the geographic distribution of campers, helping identify primary catchment areas and potential markets for expansion.

### Camper Retirements Analysis
![Camper Retirements Analysis](Camper%20Retirements%20Analysis.png)

Analyzes patterns in when and why campers stop attending, providing insights into retention challenges and opportunities.

### Number of Campers per Leader
![Number of Campers per Leader](Number%20of%20Campers%20per%20Leader.png)

Displays the distribution of campers across different leaders, helping identify workload balance and capacity planning needs.

### Number of Sessions per Leader
![Number of Sessions per Leader](Number%20of%20Sessions%20per%20Leader.png)

Tracks the number of sessions led by each leader over time, useful for recognizing top performers and ensuring equitable distribution of responsibilities.

### First-Time Camper Retention
![Percentage of One Time Campers](Percentage%20of%20One%20Time%20Campers.png)

Shows the percentage of campers who attend only one session versus those who return, a key metric for measuring program success and satisfaction.

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas matplotlib openpyxl
```

### Running the Analysis
Each Python script can be run independently: 

```bash
python "Camper Location Analysis.py"
python "Camper Retirements Analysis.py"
python "Number of Campers-Sessions per Counselor All Time.py"
python "Percentage of One Time Campers.py"
python "Number of Sessions to Camper Retention Analysis.py"
```

## 📊 Key Insights

The analyses in this repository help answer critical questions:
- **Where are our campers coming from?** - Understand geographic reach
- **Why do campers leave?** - Identify retention challenges
- **Are counselors evenly distributed?** - Balance workloads effectively
- **How effective is our first impression?** - Track first-time camper return rates
- **What drives retention?** - Correlate attendance patterns with long-term participation

## 🛠️ Technologies Used

- **Python** - Primary programming language
- **Pandas** - Data manipulation and analysis
- **Matplotlib** - Data visualization
- **Excel** - Source data format

## 📝 Future Improvements

- Add interactive dashboards using Plotly or Dash
- Implement predictive models for camper retention
- Create automated reporting pipeline
- Add time-series analysis for trend identification
- Include demographic breakdowns by age group

## 👥 Contributors

- Oliver Lazar
- Roderick Liao
- Andrew Wu