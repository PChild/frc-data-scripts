import statistics as stat
import eventTypes
import gen

tba = gen.setup()

teams = ["3538", "3538B", "33", "33B", "5050", "3641", "3641B", "2834", "2834B", "245", "1732", "302", "1718", "2337",
         "51", "4130", "1504", "503", "6538", "1", "3322", "4395", "240", "4390", "1528", "5708"]

team_data = []
for team in teams:
    vals = []

    if team[-1] == 'B':
        team_val = 'frc' + team[:-1]
    else:
        team_val = 'frc' + team

    for event in tba.team_events(team_val, 2019):
        if event.event_type in eventTypes.NORMAL:
            try:
                vals.append(tba.event_oprs(event.key)['dprs'][team_val])
            except KeyError:
                pass

    team_data.append({'team': team,
                      'min dpr': min(vals),
                      'max dpr': max(vals),
                      'avg dpr': stat.mean(vals),
                      'med dpr': stat.median(vals)})

gen.listOfDictToCSV('qd_2019marc_data', team_data, ['team', 'min dpr', 'max dpr', 'avg dpr', 'med dpr'])
