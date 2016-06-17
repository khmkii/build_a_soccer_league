import csv
import os
import random
import sys


def build_player_list(filepath, players):
    with open(filepath, 'r') as csvFile:
        csvReader = csv.DictReader(csvFile, fieldnames=['name', 'height', 'exp', 'guardians'], delimiter=',')
        next(csvReader, None)
        for row in csvReader:
            playerAtts = {'height': row['height'], 'exp': row['exp'], 'guardians': row['guardians']}
            players[row['name']] = playerAtts


def change_exp(players):
    names = []
    for key in players.keys():
        names.append(key)
    for name in names:
        if players[name]['exp'] == 'YES':
            players[name]['exp'] = True
        else:
            players[name]['exp'] = False
    return names


def equality(names, players, teams):
    expert = []
    green = []
    for name in names:
        if players[name]['exp']:
            expert.append(name)
        else:
            green.append(name)
    if len(expert) == len(green) and len(green) % teams == 0:
        return expert, green
    else:
        return None, None


def average_height(teams, playerDict):
    average_height_list = []
    for team in teams:
        sumHeight = 0
        for name in team:
            sumHeight += int(playerDict[name]['height'])
        average_height_list.append(sumHeight / len(team))
    return average_height_list


def build_teams(expertList, greenList, playerDetails, team_count):
    league_list = []
    random.shuffle(expertList)
    random.shuffle(greenList)
    if len(greenList) % team_count == 0:
        increment = len(greenList) // team_count
    else:
        print("Cannot construct even teams")
        sys.exit()
    start = 0
    stop = increment
    for i in range(team_count):
        team = greenList[start:stop] + expertList[start:stop]
        league_list.append(team)
        start += increment
        stop += increment
    return league_list


def letter_to_parent(name, team, playerDict, practice_time, folder_name):
    lower_split_name = name.lower().split(' ')
    save = lower_split_name[0] + '_' + lower_split_name[1] + '.txt'
    parents = playerDict[name]['guardians']
    with open(os.path.join(folder_name, save), 'w') as file:
        file.write('Dear {},\n'.format(parents))
        file.write('You child, {}, has been selected to play for the {}.\n'.format(name, team))
        file.write('The first practice is on {}'.format(practice_time[team]))


def write_letters(folder_name, playerDict, league_teams, practice_time):
    for key, value in league_teams.items():
        for playerName in value:
            letter_to_parent(playerName, key, playerDict, practice_time, folder_name)


if __name__ == '__main__':
    filepath = 'C:\\...file path'
    folder = 'C:\\...folder path'
    players = {}
    how_many_teams = 3

    practiceTimes = {'Dragons': 'March 17th at 1pm',
                     'Sharks': 'March 17th at 3pm',
                     'Raptors': 'March 18th at 1pm'}

    build_player_list(filepath, players)

    names = change_exp(players)

    expert, green = equality(names, players, how_many_teams)

    teams = build_teams(expert, green, players, how_many_teams)

    averages = average_height(teams, players)

    while max(averages) - min(averages) > 2:
        teams = build_teams(expert, green, players, how_many_teams)
        averages = average_height(teams, players)

    dragons, sharks, raptors = teams

    league = {'Dragons': dragons,
              'Sharks': sharks,
              'Raptors': raptors}

    write_letters(folder, players, league, practiceTimes)