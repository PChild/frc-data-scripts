import gen

YEAR = 2018

tba = gen.setup()

teams = gen.readTeamListCsv(2018).Teams


def fetchNames(robotList):
    print('memes')
    


robotNames = []
for team in teams:
    robots = tba.team_robots(team)
    for robot in robots:
        if robot.year == 2018:
            robotNames.append({'name': robot.robot_name, 'length': len(robot.robot_name)})
print(len(robotNames))
robotNames = sorted(robotNames, key= lambda k:k['Length'])
gen.listOfDictToCSV('robotNames', robotNames, ['Length', 'Name'])