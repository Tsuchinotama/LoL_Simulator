import random
import collections
import itertools
from itertools import permutations
import matplotlib.pyplot as plt
import numpy as np
import copy
import time

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

region_teams = {
    "CHN" : ["JDG", "BLG", "LNG", "WBG"], 
    "EU" : ["G2", "FNC", "MAD", "BDS"], 
    "KR" : ["GENG", "T1", "KT", "DK"], 
    "NA" : ["NRG", "C9", "TL", "GG"], 
    "PCS" : ["PSGT", "CTO"], 
    "VCS": ["GAM", "TWHA"], 
    "BRE" : ["LOD"], 
    "JPN" : ["DFM"], 
    "LAT" : ["MR7"]
}

team_regions = {
    "JDG" : "CHN", "BLG" : "CHN", "LNG" : "CHN", "WBG" : "CHN", 
    "G2" : "EU", "FNC" : "EU", "MAD" : "EU", "BDS" : "EU", 
    "GENG" : "KR", "T1" : "KR", "KT" : "KR", "DK" : "KR", 
    "NRG" : "NA", "C9" : "NA", "TL" : "NA", "GG" : "NA", 
    "CTO" : "PCS", "PSGT" : "PCS", 
    "GAM" : "VCS", "TWHA" : "VCS", 
    "LOD" : "BRE", 
    "DFM" : "JPN", 
    "MR7" : "LAT"
}

wild_card = ["BRE", "JPN", "LAT"]

# teams_ratings = {"TES" : 7.257, "DWG" : 7.207, "G2" : 6.884, "JDG" : 6.108, "DRX" : 5.789, "GEN" : 5.713, "FNC" : 5.564, "SNG" : 5.224, "LGD" : 5.154, "RGE" : 4.714, "TSM" : 4.659, "MAD" : 4.383, "TL" : 3.736, "FLY" : 3.698, "UOL" : 3.000, "SUP": 1.674, "MCX" : 1.552, "PSG" : 1.547, "INZ" : 1.485, "V3" : 1.255, "R7" : 0.750, "LGC" : 0.646}
head_to_head_odds_play_in_group = {
                        "BYG" : {"LOD" : 1.5, "CHF" : 1.59, "EG" : 2.83, "DFM" : 1.72, "FNC" : 2.87},
                        "LOD" : {"BYG" : 2.31, "DFM" : 2.56, "EG" : 3.75, "CHF" : 1.98, "FNC" : 4.2},
                        "CHF" : {"FNC" : 4.34, "DFM" : 2.14, "BYG" : 2.12, "LOD" : 1.68, "EG" : 3.41},
                        "EG" : {"LOD" : 1.2, "BYG" : 1.34, "FNC" : 2.04, "CHF" : 1.24, "DFM" : 1.41},
                        "DFM" : {"LOD" : 1.41, "CHF" : 1.58, "BYG" : 1.93, "FNC" : 3.02, "EG" : 2.56},
                        "FNC" : {"CHF" : 1.15, "EG" : 1.64, "DFM" : 1.3, "LOD" : 1.16, "BYG" : 1.33},
                        "SAI" : {"IST" : 1.41, "ISU" : 1.4, "DRX" : 3.96, "MAD" : 2.87, "RNG" : 6.05},
                        "IST" : {"SAI" : 2.56, "MAD" : 3.2, "DRX" : 6.39, "ISU" : 1.45, "RNG" : 6.39},
                        "ISU" : {"MAD" : 4.65, "SAI" : 2.59, "IST" : 2.44, "DRX" : 6.05, "RNG" : 7.22},
                        "DRX" : {"IST" : 1.06, "SAI" : 1.18, "RNG" : 2.28, "ISU" : 1.07, "MAD" : 1.41},
                        "MAD" : {"ISU" : 1.13, "IST" : 1.27, "SAI" : 1.33, "RNG" : 3.75, "DRX" : 2.56},
                        "RNG" : {"DRX" : 1.51, "IST" : 1.06, "ISU" : 1.04, "MAD" : 1.2, "SAI" : 1.07}
                    }

def world_qualifying_series():
    WQS = best_of_n_same_group(5, "BDS", "GG")
    return WQS

play_in_teams = ["PSGT", "CTO", "GAM", "TWHA", "DFM", "MR7", "LOD"]

play_in_group_A = [["GAM", "LOD"], ["MR7", "PSGT"]]
records_play_in_group_A = {"BYG" : [], "LOD" : [], "CHF" : [], "EG" : [], "DFM" : [], "FNC" : []}
group_A_play_in_init = Group(play_in_group_A, records_play_in_group_A)

play_in_group_B = [["TWHA"], ["DFM", "CFO"]]
records_play_in_group_B = {"SAI" : [], "IST" : [], "ISU" : [], "DRX" : [], "MAD" : [], "RNG" : []}
group_B_play_in_init = Group(play_in_group_B, records_play_in_group_B)

play_in_qualified_teams = []

list_main_groups_init = [["C9", "T1", "EDG"], ["JDG", "G2", "DWG"], ["RGE", "TES", "GAM"], ["GEN", "CTO", "100T"]]

class Results_available :
    def __init__(self, p_group_A_play_in_res, p_group_B_play_in_res) :
        self.group_A_play_in_res = p_group_A_play_in_res
        self.group_B_play_in_res = p_group_B_play_in_res

# Use these results value to launch a full simulation
dict_res_play_in_A = {"BYG" : ["LOD"], "LOD" : ["DFM"], "CHF" : [], "EG" : ["BYG", "LOD"], "DFM" : ["CHF"], "FNC" : ["EG", "CHF", "DFM"]}
dict_res_play_in_B = {"SAI" : ["IST", "ISU"], "IST" : [], "ISU" : [], "DRX" : ["RNG", "SAI", "IST"], "MAD" : ["ISU", "IST"], "RNG" : ["MAD"]}
dict_no_res = {}

list_res_available = Results_available(dict_res_play_in_A, dict_res_play_in_B)

def get_phase_tournament_dict_res(type_groupe) :
    if type_groupe[1] == "A" :
        return list_res_available.group_A_play_in_res
    elif type_groupe[1] == "B" :
        return list_res_available.group_B_play_in_res
    else :
        return {}

def all_games_play_in(group, type_groupe) :
    teams = group.group_teams
    records = group.group_records
    phase_res_available = get_phase_tournament_dict_res(type_groupe)
    for i in range(len(teams)) :
        teamA = teams[i]
        for j in range(i + 1, len(teams)) :
            teamB = teams[j]
            if (not teamB in phase_res_available[teamA]) and (not teamA in phase_res_available[teamB]) :
                odd_victory_A = 1 / head_to_head_odds_play_in_group[teamA][teamB]
                if random.uniform(0, 1) < odd_victory_A :
                    records[teamA].append(teamB)
                else :
                    records[teamB].append(teamA)
            elif teamB in phase_res_available[teamA] :
                records[teamA].append(teamB)
            else :
                records[teamB].append(teamA)

    sorted_records ={}
    for team in sorted(records, key=lambda team: len(records[team]), reverse=True):
        sorted_records[team] = records[team]

    group.group_records = sorted_records

def best_of_n_same_group(nb_games, team_A, team_B) :
    vict_A = 0
    vict_B = 0
    games_to_win = (nb_games // 2) + 1
    while (vict_A < games_to_win and vict_B < games_to_win) :
        odd_victory_A = 1 / (head_to_head_odds_play_in_group[team_A][team_B])
        if (random.uniform(0, 1) < odd_victory_A) :
            vict_A = vict_A + 1
        else :
            vict_B = vict_B + 1
    if vict_A == games_to_win :
        return Result_BO(team_A, team_B)
    else :
        return Result_BO(team_B, team_A)

# def best_of_n_between_groups(nb_games, team_A, team_B) :
#     vict_A = 0
#     vict_B = 0
#     games_to_win = (nb_games // 2) + 1
#     while (vict_A < games_to_win and vict_B < games_to_win) :
#         rating_A = teams_ratings[team_A]
#         rating_B = teams_ratings[team_B]
#         odd_victory_A = rating_A / (rating_A + rating_B)
#         if (random.uniform(0, 1) < odd_victory_A) :
#             vict_A = vict_A + 1
#         else :
#             vict_B = vict_B + 1
#     if vict_A == games_to_win :
#         return Result_BO(team_A, team_B)
#     else :
#         return Result_BO(team_B, team_A)

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

#retourne l'ordre après un tie-breaker à 3 équipes (toutes les équipes peuvent finir première)
def tie_2_teams(list_teams) :
    pos = []
    result = best_of_n_same_group(1, list_teams[0], list_teams[1])
    pos.append(result.win_team)
    pos.append(result.lose_team)
    return pos

#retourne l'ordre après un tie-breaker à 3 équipes (toutes les équipes peuvent finir première)
def tie_3_teams(list_teams) :
    (shortest_team, (longest_team_1, longest_team_2)) = choose_random_3(list_teams)
    pos = []
    result1 = best_of_n_same_group(1, longest_team_1, longest_team_2)
    if result1.win_team == longest_team_1 :
        result2 = best_of_n_same_group(1, shortest_team, longest_team_1)
    else :
        result2 = best_of_n_same_group(1, shortest_team, longest_team_2)
    pos.append(result2.win_team)
    pos.append(result2.lose_team)
    pos.append(result1.lose_team)
    return pos

#retourne l'ordre dans le cadre d'un tie breaker à 4 équipes en play-in
def tie_4_teams(list_teams) :
    pos = []
    order_list = choose_random_list(list_teams)
    demie1 = best_of_n_same_group(1, order_list[0], order_list[3])
    demie2 = best_of_n_same_group(1, order_list[1], order_list[2])
    finale = best_of_n_same_group(1, demie1.win_team, demie2.win_team)
    pos.append(finale.win_team)
    pos.append(finale.lose_team)
    petite_finale = best_of_n_same_group(1, demie1.lose_team, demie2.lose_team)
    pos.append(petite_finale.win_team)
    pos.append(petite_finale.lose_team)
    return pos

#retourne l'ordre après un tie-break entre les 5 équipes d'un groupe de play-in
def tie_5_teams(list_teams) :
    pos = []
    order_list = choose_random_list(list_teams)
    pos.append(order_list[0])
    demie1 = best_of_n_same_group(1, order_list[1], order_list[4])
    demie2 = best_of_n_same_group(1, order_list[2], order_list[3])
    finale = best_of_n_same_group(1, demie1.win_team, demie2.win_team)
    pos.append(finale.win_team)
    pos.append(finale.lose_team)
    petite_finale = best_of_n_same_group(1, demie1.lose_team, demie2.lose_team)
    pos.append(petite_finale.win_team)
    pos.append(petite_finale.lose_team)
    return pos


def all_ties_play_in(results_group) :
    list_results_group = list(results_group.items())
    list_ties = []
    i = 0
    while i < 6 :
        res_team = list_results_group[i]
        teams_tied = ([i + 1], [res_team[0]])
        j = i + 1
        while j < 5 and (len(res_team[1]) == len(list_results_group[j][1])) :
            teams_tied[0].append(j + 1)
            teams_tied[1].append(list_results_group[j][0])
            j = j + 1
        list_ties.append(teams_tied)
        i = j
    return list_ties

def resolve_play_in_ties(results_group, list_ties) :
    list_resolved_ties = []
    for to_tie in list_ties :
        seeds_to_tie = to_tie[0]
        teams_to_tie = to_tie[1]
        if len(teams_to_tie) == 1 :
            list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[0]))

        elif len(teams_to_tie) == 2 :
            pos = tie_2_teams(teams_to_tie)
            # if teams_to_tie[1] in results_group[teams_to_tie[0]] :
            #     list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[0]))
            #     list_resolved_ties.append((seeds_to_tie[1], teams_to_tie[1]))
            # else :
            #     list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[1]))
            #     list_resolved_ties.append((seeds_to_tie[1], teams_to_tie[0]))

        elif len(teams_to_tie) == 3 :
            res_between_3 = head_to_head(results_group, teams_to_tie)
            res_between_3 = sorted(res_between_3.items(), key=lambda x: x[1], reverse=True)
            pos_3_ties = tie_3_teams(teams_to_tie)
            for i in range(3) :
                list_resolved_ties.append((seeds_to_tie[i], pos_3_ties[i]))

        elif len(teams_to_tie) == 4 :
            random_list_teams = choose_random_list(teams_to_tie)
            pos = tie_4_teams(random_list_teams)
            for i in range(4) :
                list_resolved_ties.append((seeds_to_tie[i], pos[i]))

        else:
            random_list_teams = choose_random_list(teams_to_tie)
            pos = tie_5_teams(random_list_teams)
            for i in range(5) :
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

def affect_play_in_team(list_teams, affects_group) :
    wild_card_teams = []
    compatibilities = {}

    for team in list_teams :
        compatibilities[team] = []
        region = team_regions[team]
        if region in wild_card :
            for i in range(4) :
                compatibilities[team].append(i)
        else :
            for i in range(4) :
                group = list_main_groups_init[i].copy()
                for group_team in group :
                    if region == team_regions[group_team] :
                        break

                else :
                    compatibilities[team].append(i)
    list_all_affects = []
    generate_all_affectations(list(compatibilities.items()), affects_group, list_all_affects)
    return list_all_affects

def generate_all_affectations(compatibilities, current_affect, list_all_affects) :
    if group_already_affected(current_affect) :
        return False

    if len(compatibilities) == 0 :
        list_all_affects.append(current_affect)
        return True

    team_comp = compatibilities[0]
    for num_group in team_comp[1] :
        copy_current_affect = current_affect.copy()
        copy_current_affect.append((team_comp[0], num_group))
        generate_all_affectations(compatibilities[1:], copy_current_affect, list_all_affects)

def group_already_affected(current_affect) :
    list_num_group = list(range(4))
    for affect in current_affect :
        if not affect[1] in list_num_group :
            return True
        else :
            list_num_group.remove(affect[1])
    else :
        return False

def choose_random_affect(list_affects) :
    return list_affects[random.randrange(len(list_affects))]

def place_affected_teams(list_groups, affect) :
    for team_affect in affect :
        team_name = team_affect[0]
        num_group = team_affect[1]
        list_groups[num_group].group_teams.append(team_name)
        list_groups[num_group].group_records[team_name] = []


def play_in(group_A, group_B) :

    all_games_play_in(group_A, ("play-in", "A"))
    all_games_play_in(group_B, ("play-in", "B"))


    #results_play_in_group_A = {"TL" : ["MAD", "LGC"], "MAD" : ["LGC", "SUP"], "LGC" : ["SUP", "INZ"], "SUP" : ["INZ", "TL"], "INZ" : ["TL", "MAD"]}
    results_play_in_group_A = group_A.group_records
    results_play_in_group_B = group_B.group_records

    # print(results_play_in_group_A)
    # print(results_play_in_group_B)

    list_ties_play_in_A = all_ties_play_in(results_play_in_group_A)
    list_ties_play_in_B = all_ties_play_in(results_play_in_group_B)

    group_A_play_in_pos = resolve_play_in_ties(results_play_in_group_A, list_ties_play_in_A)
    group_B_play_in_pos = resolve_play_in_ties(results_play_in_group_B, list_ties_play_in_B)

    # play_in_qualified_teams = []

    # play_in_qualified_teams.append(group_A_play_in_pos[0][1])
    # play_in_qualified_teams.append(group_B_play_in_pos[0][1])

    # res_group_A_play_in_3_4 = best_of_n_same_group(5, group_A_play_in_pos[2][1], group_A_play_in_pos[3][1])
    # res_group_B_play_in_3_4 = best_of_n_same_group(5, group_B_play_in_pos[2][1], group_B_play_in_pos[3][1])

    # play_in_group_A_3 = res_group_A_play_in_3_4.win_team
    # play_in_group_B_3 = res_group_B_play_in_3_4.win_team

    # res_match_2nd_A_3rd_B = best_of_n(5, group_A_play_in_pos[1][1], play_in_group_A_3)
    # res_match_2nd_B_3rd_A = best_of_n(5, group_B_play_in_pos[1][1], play_in_group_B_3)

    # play_in_qualified_teams.append(res_match_2nd_A_3rd_B.win_team)
    # play_in_qualified_teams.append(res_match_2nd_B_3rd_A.win_team)

    # print(play_in_qualified_teams)

    # list_all_affects = []

    # affects_group = []
    # list_all_affects = affect_play_in_team(play_in_qualified_teams, affects_group)
    # affect = choose_random_affect(list_all_affects)

    # print(affect)

    return (group_A_play_in_pos, group_B_play_in_pos)

def tournament() :
    group_A_play_in = copy.deepcopy(Group(play_in_group_A, records_play_in_group_A))
    group_B_play_in = copy.deepcopy(Group(play_in_group_B, records_play_in_group_B))

    return play_in(group_A_play_in, group_B_play_in)

pos_B = {
    "RNG" : [0 for i in range(6)],
    "DRX" : [0 for i in range(6)],
    "SAI" : [0 for i in range(6)],
    "MAD" : [0 for i in range(6)],
    "IST" : [0 for i in range(6)],
    "ISU" : [0 for i in range(6)]
}

pos_A = {
    "FNC" : [0 for i in range(6)],
    "BYG" : [0 for i in range(6)],
    "EG" : [0 for i in range(6)],
    "DFM" : [0 for i in range(6)],
    "LOD" : [0 for i in range(6)],
    "CHF" : [0 for i in range(6)]
}

for i in range(1000):
    (group_A, group_B) = tournament()
    for (place, team) in group_A:
        pos_A[team][place-1] = pos_A[team][place-1]+1

    for (place, team) in group_B:
        pos_B[team][place-1] = pos_B[team][place-1]+1    


# for team in play_in_group_A:
#     lp=pos_A[team]
#     print(team + " : " + str(lp))
#     fig, ax = plt.subplots()
#     ax.bar(x=range(6), height=lp, align="center")
#     ax.set_xticks(range(len(lp)))
#     ax.set_xticklabels(i for i in range(1,7))
#     fig.autofmt_xdate()
#     plt.title(team)

# for team in play_in_group_B:
#     lp=pos_B[team]
#     print(team + " : " + str(lp))
#     fig, ax = plt.subplots()
#     ax.bar(x=range(6), height=lp, align="center")
#     ax.set_xticks(range(len(lp)))
#     ax.set_xticklabels(i for i in range(1,7))
#     fig.autofmt_xdate()
#     plt.title(team)

plt.show()