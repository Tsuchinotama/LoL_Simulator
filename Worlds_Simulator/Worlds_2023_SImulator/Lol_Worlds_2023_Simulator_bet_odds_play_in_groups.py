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
        return ("Equipes du groupe : " + str(self.group_records))

class Result_BO :
    def __init__(self, p_win_team, p_winner_score, p_lose_team, p_loser_score) :
        self.win_team = p_win_team
        self.score_winner = p_winner_score
        self.lose_team = p_lose_team
        self.score_loser = p_loser_score

all_swiss_teams = [
    "GENG", "T1", "KT", "DK",
    "JDG", "BLG", "LNG", "WBG",
    "G2", "FNC", "MAD",
    "NRG","C9", "TL"
] 

WQS_teams = ["BDS", "GG"]

all_play_in_teams = ["R7", "GAM", "TWHA", "LOUD", "PSGT", "CTO", "DFM"]

play_in_group_A = ["LOUD", "GAM", "R7", "PSGT"]
play_in_group_B = ["DFM", "CTO", "TWHA"]
play_in_group_B_BDS = ["DFM", "CTO", "TWHA", "BDS"]
play_in_group_B_GG = ["DFM", "CTO", "TWHA", "GG"]
list_all_possible_play_in_qualifs = []

region_teams = {
    "CHN" : ["JDG", "BLG", "LNG", "WBG"], 
    "EU" : ["G2", "FNC", "MAD", "BDS"], 
    "KR" : ["GENG", "T1", "KT", "DK"], 
    "NA" : ["NRG", "C9", "TL", "GG"], 
    "PCS" : ["PSGT", "CTO"], 
    "VCS": ["GAM", "TWHA"], 
    "BRE" : ["LOUD"], 
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
    "LOUD" : "BRE", 
    "DFM" : "JPN", 
    "MR7" : "LAT"
}

# Betting odd based on https://esportbet.com/league-of-legends/worlds/
teams_rating = {
    "JDG" : 2.20, "LNG" : 6, "GENG" : 6.50, "BLG" : 9.00, 
    "T1" : 10.00, "WBG" : 11.00, "KT" : 13.00, "DK" : 15.00, 
    "G2" : 26.00, "FNC" : 41.00, "MAD" : 67.00, "C9" : 81.00, 
    "NRG" : 101.00, "TL" : 201.00, "GG" : 301.00, "BDS" : 301.00, 
    "PSGT" : 401.00, "GAM" : 451.00, "LOUD" : 501.00, "CTO" : 751.00, 
    "TWHA" : 901.00, "DFM" : 1001.00, "MR7" : 1501.00
}

def world_qualifying_series():
    WQS = best_of_n(5, "BDS", "GG")
    return WQS

WQS_res = world_qualifying_series()

play_in_teams = ["PSGT", "CTO", "GAM", "TWHA", "DFM", "MR7", "LOUD"]

play_in_group_A = [["GAM", "LOUD"], ["MR7", "PSGT"]]
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

def all_games_play_in(WQS_winner, group, type_groupe) :
    teams = group.group_teams
    records = group.group_records
    phase_res_available = get_phase_tournament_dict_res(type_groupe)

    # Group A games
    AW1 = best_of_n(3, "LOUD", "GAM")
    AW2 = best_of_n(3, "MR7", "PSGT")
    AWF = best_of_n(3, AW1.win_team, AW2.win_team)
    AL1 = best_of_n(3, AW1.lose_team, AW2.lose_team)
    ALF = best_of_n(3, AWF.lose_team, AL1.win_team)

    # Group B games
    BW1 = best_of_n(3, WQS_winner, "TWHA")
    BW2 = best_of_n(3, "DFM", "CTO")
    BWF = best_of_n(3, BW1.win_team, BW2.win_team)
    BL1 = best_of_n(3, BW1.lose_team, BW2.lose_team)
    BLF = best_of_n(3, BWF.lose_team, BL1.win_team)

    # Play-in qualifiers matches
    PIQM1 = best_of_n(5, AWF.win_team, BLF.win_team)
    PIQM2 = best_of_n(5, BWF.win_team, ALF.win_team)

def best_of_n(nb_games, team_A, team_B) :
    vict_A = 0
    vict_B = 0
    games_to_win = (nb_games // 2) + 1
    odd_victory_A = teams_rating[team_B] / (teams_rating[team_A] + teams_rating[team_B])
    while (vict_A < games_to_win and vict_B < games_to_win) :
        if (random.uniform(0, 1) < odd_victory_A) :
            vict_A = vict_A + 1
        else :
            vict_B = vict_B + 1
    if vict_A == games_to_win :
        return Result_BO(team_A, team_B)
    else :
        return Result_BO(team_B, team_A)

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


for team in play_in_group_A:
    lp=pos_A[team]
    print(team + " : " + str(lp))
    fig, ax = plt.subplots()
    ax.bar(x=range(6), height=lp, align="center")
    ax.set_xticks(range(len(lp)))
    ax.set_xticklabels(i for i in range(1,7))
    fig.autofmt_xdate()
    plt.title(team)

for team in play_in_group_B:
    lp=pos_B[team]
    print(team + " : " + str(lp))
    fig, ax = plt.subplots()
    ax.bar(x=range(6), height=lp, align="center")
    ax.set_xticks(range(len(lp)))
    ax.set_xticklabels(i for i in range(1,7))
    fig.autofmt_xdate()
    plt.title(team)

plt.show()