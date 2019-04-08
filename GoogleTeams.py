import pandas as pd
tS = pd.read_csv('Team Sponsors.csv', skipinitialspace=True)
googleTeams = tS[tS['Full Name'].str.contains("Google")]
googleTeams = googleTeams.drop('Sponsors', 1)
googleTeams = googleTeams.sort_values('Team')
googleTeams.to_csv("GoogleTeams.csv", index=False)