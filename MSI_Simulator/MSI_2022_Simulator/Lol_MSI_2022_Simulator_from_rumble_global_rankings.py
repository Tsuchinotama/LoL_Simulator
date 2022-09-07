import random
import collections
import itertools
from itertools import permutations
from typing import final
import matplotlib.pyplot as plt
import numpy as np
import copy

class Group :
    def __init__(self, p_group_teams, p_group_records) :
        self.group_teams = p_group_teams
        self.group_records = p_group_records

    def __str__(self) :
        return ("équipes du groupe : " + str(self.group_records))

class Result_BO :
    def __init__(self, p_win_team, p_lose_team) :
        self.win_team = p_win_team
        self.lose_team = p_lose_team

wild_card = ["OCE", "TUR", "BRE", "JPN", "LAT", "VIT"]

list_all_teams = ["T1", "RNG", "G2", "EG", "PSG", "DFM", "SAI", "IST", "RED", "AZE", "ORD"]
teams_rankings = {"T1": 1.5, "RNG": 2.5, "G2": 3.3, "EG": 4.4, "PSG": 5.3, "DFM": 6.7, "SAI": 7.5, "IST": 8.2, "RED": 8.6, "AZE": 9.0, "ORD": 9.0}

teams_ratings = {team: 11.0-teams_rankings[team] for team in teams_rankings}

wild_card_teams = ["DFM", "SAI", "IST", "RED", "AZE", "ORD"]

play_in_group_A = ["T1", "SAI", "DFM", "AZE"]
records_play_in_group_A = {"T1" : [], "SAI" : [], "DFM" : [], "AZE" : []}
group_A_play_in_init = Group(play_in_group_A, records_play_in_group_A)

play_in_group_B = ["RNG", "PSG", "IST", "RED"]
records_play_in_group_B = {"RNG" : [], "PSG" : [], "IST" : [], "RED" : []}
group_B_play_in_init = Group(play_in_group_B, records_play_in_group_B)

play_in_group_C = ["G2", "EG", "ORD"]
records_play_in_group_C = {"G2" : [], "EG" : [], "ORD" : []}
group_B_play_in_init = Group(play_in_group_C, records_play_in_group_C)

play_in_qualified_teams = []

main_group = ["T1", "RNG", "G2", "PSG", "EG", "SAI"]
records_main_group = {}
main_group_init = Group(main_group, records_main_group)

class Results_available :
    def __init__(self, p_group_A_play_in_res, p_group_B_play_in_res, p_group_C_play_in_res, p_main_group_res, p_coupe_phase_res) :
        self.group_A_play_in_res = p_group_A_play_in_res
        self.group_B_play_in_res = p_group_B_play_in_res
        self.group_C_play_in_res = p_group_C_play_in_res
        self.main_group_res = p_main_group_res
        self.p_coupe_phase_res = p_coupe_phase_res

# Use these results value to launch a full simulation
dict_res_play_in_A = {"T1" : [], "SAI" : [], "DFM" : [], "AZE" : []}
dict_res_play_in_B = {"RNG" : [], "PSG" : [], "RED" : [], "IST" : []}
dict_res_play_in_C = {"G2" : [], "EG" : [], "ORD" : []}
dict_no_res = {}

# Results are updated each day of competition
#dict_res_play_in_A = {"TL" : ["MAD", "LGC"], "MAD" : ["INZ"], "LGC" : ["INZ"], "SUP" : ["INZ", "MAD"], "INZ" : []}

#dict_res_play_in_B = {"LGD" : [], "PSG" : ["LGD", "R7"], "V3" : ["R7"], "UOL" : ["V3", "PSG"], "R7" : ["LGD"]}

# dict_res_main_A = {"DWG" : [], "FPX" : [], "RGE" : []}
# dict_res_main_B = {"EDG" : [], "T1" : [], "100T" : []}
# dict_res_main_C = {"PSG" : [], "FNC" : [], "RNG" : []}
# dict_res_main_D = {"MAD" : [], "GEN" : [], "TL" : []}

# list_res_available = Results_available(dict_res_play_in_A, dict_res_play_in_B, dict_no_res, dict_res_main_A, dict_res_main_B, dict_res_main_C, dict_res_main_D, dict_no_res)

list_res_available = Results_available(dict_res_play_in_A, dict_res_play_in_B, dict_res_play_in_C, dict_no_res, dict_no_res)


def get_phase_tournament_dict_res(type_groupe) :
    if type_groupe[1] == "A" :
        return list_res_available.group_A_play_in_res
    elif type_groupe[1] == "B" :
        return list_res_available.group_B_play_in_res
    elif type_groupe[1] == "C" :
        return list_res_available.group_C_play_in_res
    else :
        return {}

def all_games_play_in_msi(group, type_groupe):
    teams = group.group_teams
    records = group.group_records
    phase_res_available = get_phase_tournament_dict_res(type_groupe)

    if type_groupe[1] == "C":
        for i in range(4):
            all_games(group, i)

    else:
        all_games(group, 1)
        all_games(group, 2)

def all_games(group, num_match) :
    teams = group.group_teams
    records = group.group_records
    for i in range(len(teams)) :
        teamA = teams[i]
        rating_A = teams_ratings[teamA]
        for j in range(i + 1, len(teams)) :
            teamB = teams[j]
            rating_B = teams_ratings[teamB]
            odd_victory_A = rating_A / (rating_A + rating_B)
            if random.uniform(0, 1) < odd_victory_A :
                records[teamA].append((num_match, teamB))
            else :
                records[teamB].append((num_match, teamA))

    sorted_records = {}
    for team in sorted(records, key=lambda team: len(records[team]), reverse=True):
        sorted_records[team] = records[team]

    group.group_records = sorted_records

def best_of_n(nb_games, team_A, team_B) :
    vict_A = 0
    vict_B = 0
    games_to_win = (nb_games // 2) + 1
    while (vict_A < games_to_win and vict_B < games_to_win) :
        rating_A = teams_ratings[team_A]
        rating_B = teams_ratings[team_B]
        odd_victory_A = rating_A / (rating_A + rating_B)
        if (random.uniform(0, 1) < odd_victory_A) :
            vict_A = vict_A + 1
        else :
            vict_B = vict_B + 1
    if vict_A == games_to_win :
        return Result_BO(team_A, team_B)
    else :
        return Result_BO(team_B, team_A)

def choose_random_2(team_A, team_B) :
    if random.uniform(0, 1) < 0.5 :
        return team_A
    else :
        return team_B

def choose_random_3(list_teams) :
    rand = random.uniform(0, 3)
    if rand < 1 :
        return (list_teams[0], (list_teams[1], list_teams[2]))
    elif rand < 2 :
        return (list_teams[1], (list_teams[0], list_teams[2]))
    else :
        return (list_teams[2], (list_teams[0], list_teams[1]))

def choose_random_list(list_teams) :
    copy_list = list_teams[:]
    new_list = []
    for i in range(len(list_teams)) :
        item = copy_list[random.randrange(0, len(list_teams) - i)]
        new_list.append(item)
        copy_list.remove(item)
    return new_list

#retourne la place des équipes dans le cadre d'un tie breaker à 3 équipes pour 2 places 
#toutes les équipes peuvent finir dernière/éliminée, la pire équipe au temps ne peut pas finir première du tie-break
def tie_2_seeds_for_3_teams(list_teams) :
    (longest_team, (shortest_team_1, shortest_team_2)) = choose_random_3(list_teams)
    pos = []
    result1 = best_of_n(1, shortest_team_1, shortest_team_2)
    pos.append(result1.win_team)
    if result1.lose_team == shortest_team_1 :
        result2 = best_of_n(1, shortest_team_1, longest_team)
    else :
        result2 = best_of_n(1, shortest_team_2, longest_team)
    pos.append(result2.win_team)
    pos.append(result2.lose_team)
    return pos

#retourne la place des équipes dans le cadre d'un tie breaker à 3 équipes pour 1 place 
#toutes les équipes peuvent finir première, la meilleure équipe ne peut pas finir dernière du tie-break
def tie_1_seed_for_3_teams(list_teams) :
    (shortest_team, (longest_team_1, longest_team_2)) = choose_random_3(list_teams)
    pos = []
    result1 = best_of_n(1, longest_team_1, longest_team_2)
    if result1.win_team == longest_team_1 :
        result2 = best_of_n(1, shortest_team, longest_team_1)
    else :
        result2 = best_of_n(1, shortest_team, longest_team_2)
    pos.append(result2.win_team)
    pos.append(result2.lose_team)
    pos.append(result1.lose_team)
    return pos

#retourne les 2 équipes qualifiées dans le cadre d'un tie breaker à 4 équipes pour 2 place; la situation ne peut arriver que durant la phase de goupes du main event
def tie_2_seeds_for_4_teams(list_teams) :
    pos = []
    order_list = choose_random_list(list_teams)
    result1 = best_of_n(1, order_list[0], order_list[3])
    winner1 = result1.win_team
    loser1 = result1.lose_team
    result2 = best_of_n(1, order_list[1], order_list[2])
    winner2 = result2.win_team
    loser2 = result2.lose_team
    result3 = best_of_n(1, winner1, winner2)
    result4 = best_of_n(1, loser1, loser2)
    pos.append(result3.win_team)
    pos.append(result3.lose_team)
    pos.append(result4.win_team)
    pos.append(result4.lose_team)
    return pos

def all_ties_play_in_msi(group):
    name = group[1]
    if name != "C":
        return all_ties_group_A_B_play_in(group[0].group_records)
    else:
        return all_ties_play_in_group_C(group[0].group_records)

def all_ties_play_in_group_C(results_group) :
    list_results_group = list(results_group.items())
    list_ties = []
    i = 0
    while i < 3 :
        res_team = list_results_group[i]
        teams_tied = ([i + 1], [res_team[0]])
        j = i + 1
        while j < 3 and (len(res_team[1]) == len(list_results_group[j][1])) :
            teams_tied[0].append(j + 1)
            teams_tied[1].append(list_results_group[j][0])
            j = j + 1
        list_ties.append(teams_tied)
        i = j
    return list_ties

def all_ties_group_A_B_play_in(results_group) :
    list_results_group = list(results_group.items())
    list_ties = []
    i = 0
    while i < 4 :
        res_team = list_results_group[i]
        teams_tied = ([i + 1], [res_team[0]])
        j = i + 1
        while j < 4 and (len(res_team[1]) == len(list_results_group[j][1])) :
            teams_tied[0].append(j + 1)
            teams_tied[1].append(list_results_group[j][0])
            j = j + 1
        list_ties.append(teams_tied)
        i = j
    return list_ties

def all_ties_main(results_group) :
    list_results_group = list(results_group.items())
    list_ties = []
    i = 0
    while i < 6 :
        res_team = list_results_group[i]
        teams_tied = ([i + 1], [res_team[0]])
        j = i + 1
        while j < 6 and (len(res_team[1]) == len(list_results_group[j][1])) :
            teams_tied[0].append(j + 1)
            teams_tied[1].append(list_results_group[j][0])
            j = j + 1
        list_ties.append(teams_tied)
        i = j
    return list_ties

def resolve_play_in_ties_group_C(results_group, list_ties) :
    list_resolved_ties = []
    for to_tie in list_ties :
        seeds_to_tie = to_tie[0]
        teams_to_tie = to_tie[1]
        if len(teams_to_tie) == 1 :
            list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[0]))

        elif len(teams_to_tie) == 2 :
            team_A = teams_to_tie[0]
            team_B = teams_to_tie[1]
            if results_group[team_A].count(team_B) > 2:
                list_resolved_ties.append((seeds_to_tie[0], team_A))
                list_resolved_ties.append((seeds_to_tie[0], team_B))

            elif results_group[team_B].count(team_A) > 2:
                list_resolved_ties.append((seeds_to_tie[0], team_B))
                list_resolved_ties.append((seeds_to_tie[0], team_A))

            else:
                rating_A = teams_ratings[team_A]
                rating_B = teams_ratings[team_B]
                odd_victory_A = rating_A / (rating_A + rating_B)
                if (random.uniform(0, 1) < odd_victory_A) :
                    list_resolved_ties.append((seeds_to_tie[0], team_A))
                    list_resolved_ties.append((seeds_to_tie[0], team_B))
                else :
                    list_resolved_ties.append((seeds_to_tie[0], team_B))
                    list_resolved_ties.append((seeds_to_tie[0], team_A))

        else :
            pos_3_ties = tie_1_seed_for_3_teams(teams_to_tie)
            for i in range(3) :
                list_resolved_ties.append((seeds_to_tie[i], pos_3_ties[i]))

    return list_resolved_ties

def resolve_main_ties(results_group, list_ties) :
    list_resolved_ties = []
    for to_tie in list_ties :
        seeds_to_tie = to_tie[0]
        teams_to_tie = to_tie[1]
        if len(teams_to_tie) == 1 :
            list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[0]))

        elif len(teams_to_tie) == 2 :
            team_A = teams_to_tie[0]
            team_B = teams_to_tie[1]
            if results_group[team_A].count(team_B) > results_group[team_B].count(team_A):
                list_resolved_ties.append((seeds_to_tie[0], team_A))
                list_resolved_ties.append((seeds_to_tie[1], team_B))
            elif results_group[team_B].count(team_A) > results_group[team_A].count(team_B):
                list_resolved_ties.append((seeds_to_tie[0], team_B))
                list_resolved_ties.append((seeds_to_tie[1], team_A))
            else:
                res_tie = best_of_n(1, team_A, team_B)
                winner_tie = res_tie.win_team
                loser_tie = res_tie.lose_team
                list_resolved_ties.append((seeds_to_tie[0], winner_tie))
                list_resolved_ties.append((seeds_to_tie[1], loser_tie))

        elif len(teams_to_tie) == 3 :
            res_between_3 = head_to_head(results_group, teams_to_tie)
            # print(res_between_3)
            res_between_3 = sorted(res_between_3.items(), key=lambda x: x[1], reverse=True)
            pos_3_ties = tie_1_seed_for_3_teams(teams_to_tie)
            for i in range(3) :
                list_resolved_ties.append((seeds_to_tie[i], pos_3_ties[i]))

        else :
            random_list_teams = choose_random_list(teams_to_tie)
            pos = tie_2_seeds_for_4_teams(random_list_teams)
            for i in range(4) :
                list_resolved_ties.append((seeds_to_tie[i], pos[i]))
    return list_resolved_ties

def head_to_head(res_group, teams) :
    dict_tie = {}
    for team in teams :
        dict_tie[team] = 0
        for beated in res_group[team] :
            if beated in teams :
                dict_tie[team] = dict_tie[team] + 1
    return dict_tie

def choose_semis(res_rumble):
    team_rumble_1 = res_rumble[0][1]
    team_rumble_2 = res_rumble[1][1]
    team_rumble_3 = res_rumble[2][1]
    team_rumble_4 = res_rumble[3][1]
    semis = [team_rumble_1]
    if teams_ratings[team_rumble_3] > teams_ratings[team_rumble_4]:
        semis += [team_rumble_4, team_rumble_2, team_rumble_3]
    else:
        semis += [team_rumble_3, team_rumble_2, team_rumble_4]
    return semis

def play_semis(semis) :
    finalist_1 = best_of_n(5, semis[0], semis[1]).win_team
    finalist_2 = best_of_n(5, semis[2], semis[3]).win_team
    return (finalist_1, finalist_2)

def play_in(group_A, group_B, group_C) :
    all_games_play_in_msi(group_A, ("play-in", "A"))
    all_games_play_in_msi(group_B, ("play-in", "B"))
    all_games_play_in_msi(group_C, ("play-in", "C"))

    #results_play_in_group_A = {"TL" : ["MAD", "LGC"], "MAD" : ["LGC", "SUP"], "LGC" : ["SUP", "INZ"], "SUP" : ["INZ", "TL"], "INZ" : ["TL", "MAD"]}
    results_play_in_group_A = group_A.group_records
    results_play_in_group_B = group_B.group_records
    results_play_in_group_C = group_C.group_records

    print(results_play_in_group_A)
    print(results_play_in_group_B)
    print(results_play_in_group_C)

    list_ties_play_in_A = all_ties_play_in_msi((group_A, "A"))
    list_ties_play_in_B = all_ties_play_in_msi((group_B, "B"))
    list_ties_play_in_C = all_ties_play_in_msi((group_C, "C"))

    group_A_play_in_pos = resolve_main_ties(results_play_in_group_A, list_ties_play_in_A)
    group_B_play_in_pos = resolve_main_ties(results_play_in_group_B, list_ties_play_in_B)
    group_C_play_in_pos = resolve_play_in_ties_group_C(results_play_in_group_C, list_ties_play_in_C)

    play_in_qualified_teams = []

    play_in_qualified_teams.append(group_A_play_in_pos[0][1])
    play_in_qualified_teams.append(group_B_play_in_pos[0][1])
    play_in_qualified_teams.append(group_C_play_in_pos[0][1])


    play_in_qualified_teams.append(group_A_play_in_pos[1][1])
    play_in_qualified_teams.append(group_B_play_in_pos[1][1])
    play_in_qualified_teams.append(group_C_play_in_pos[1][1])

    # print(play_in_qualified_teams)

    return play_in_qualified_teams

def msi_main_group(main_group):
    all_games(main_group, 1)
    all_games(main_group, 2)

    results_main_group = main_group.group_records
    # print(results_main_group)
    list_ties_main_group = all_ties_main(results_main_group)

def main_groups(main_group):
    all_games(main_group, 1)
    all_games(main_group, 2)

    results_main_group = main_group.group_records
    # print(results_main_group)

    list_ties_main = all_ties_main(results_main_group)

    group_main_pos = resolve_main_ties(results_main_group, list_ties_main)
    matchup_semis = choose_semis(group_main_pos) 

    # print(matchup_semis)

    res_semis = play_semis(matchup_semis)
    # print(res_semis)

    final_winner = best_of_n(5, res_semis[0], res_semis[1]).win_team
    # print(final_winner)
    return (final_winner, res_semis, matchup_semis)

def tournament() :
    # group_A_play_in = copy.deepcopy(Group(play_in_group_A, records_play_in_group_A))
    # group_B_play_in = copy.deepcopy(Group(play_in_group_B, records_play_in_group_B))
    # group_C_play_in = copy.deepcopy(Group(play_in_group_C, records_play_in_group_C))

    # list_qualified_from_play_in = play_in(group_A_play_in, group_B_play_in, group_C_play_in)

    main_group_teams = ["T1", "RNG", "G2", "PSG", "EG", "SAI"]
    records_main_group = {team : [] for team in main_group_teams}

    main_group = copy.deepcopy(Group(main_group_teams, records_main_group))

    # main_group = [group_A_main, group_B_main, group_C_main, group_D_main]

    res_knockout = main_groups(main_group)

    return (res_knockout[0], res_knockout[1], res_knockout[2])

nb_victories = {}
nb_finales = {}
nb_demies = {}
nb_qualif_wild_card = {}

for team in main_group :
    nb_victories[team] = 0
    nb_finales[team] = 0
    nb_demies[team] = 0

for i in range(1000) :
    (champion, liste_finalistes, liste_demis_finalistes) = tournament()
    # (champion, liste_finalistes, liste_demis_finalistes, liste_qualifies_play_in) = tournament()
    nb_victories[champion] = nb_victories[champion] + 1

    for finaliste in liste_finalistes :
        nb_finales[finaliste] = nb_finales[finaliste] + 1

    for demie in liste_demis_finalistes :
        nb_demies[demie] = nb_demies[demie] + 1

print(nb_demies)
print()
print(nb_finales)
print()
print(nb_victories)

l1=sorted(nb_demies.items())
fig, ax = plt.subplots()
ax.bar(range(len(l1)), [t[1] for t in l1]  , align="center")
ax.set_xticks(range(len(l1)))
ax.set_xticklabels([t[0] for t in l1])
fig.autofmt_xdate()
plt.title("Demis-finaliste (qualif du rumble)")

l2=sorted(nb_finales.items())
fig, ax = plt.subplots()
ax.bar(range(len(l2)), [t[1] for t in l2]  , align="center")
ax.set_xticks(range(len(l2)))
ax.set_xticklabels([t[0] for t in l2])
fig.autofmt_xdate()
plt.title("Finalistes")

l3=sorted(nb_victories.items())
fig, ax = plt.subplots()
ax.bar(range(len(l3)), [t[1] for t in l3]  , align="center")
ax.set_xticks(range(len(l3)))
ax.set_xticklabels([t[0] for t in l3])
fig.autofmt_xdate()
plt.title("Vainqueurs")

plt.show()


