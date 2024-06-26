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

class head_to_head :
    def __init__(self, p_wins, p_losses, p_ratio) :
        self.wins = p_wins
        self.losses = p_losses
        self.ratio = p_ratio

    def __str__(self) :
        return ("victoires : " + str(self.wins) + " , defaites : " + str(self.losses) + " , ratio : " + str(self.ratio))

region_teams = {"CHN" : ["TES", "JDG", "SN", "LGD"], "EU" : ["G2", "FNC", "RGE", "MAD"], "KR" : ["DWG", "DRX", "GEN"], "NA" : ["TSM", "FLY", "TL"], "PCS" : ["MCX", "PSG"], "OCE" : ["LGC"], "TUR" : ["SUP"], "BRE" : ["INZ"], "JPN" : ["V3"], "RUS" : ["UOL"], "LAT" : ["R7"]}

team_regions = {"TES" : "CHN", "JDG" : "CHN", "SN" : "CHN", "LGD" : "CHN", "G2" : "EU", "FNC" : "EU", "RGE" : "EU", "MAD" : "EU", "DWG" : "KR", "DRX" : "KR", "GEN" : "KR", "TSM" : "NA", "FLY" : "NA", "TL" : "NA", "MCX" : "PCS", "PSG" : "PCS", "LGC" : "OCE", "SUP" : "TUR", "INZ" : "BRE", "V3" : "JPN", "UOL" : "RUS", "R7" : "LAT"}

wild_card = ["OCE", "TUR", "BRE", "JPN", "RUS", "LAT"]


dict_head_to_head = {}

for team in team_regions :
    inner_dict = {opponent : head_to_head(0, 0, 0) for opponent in team_regions}
    del inner_dict[team]
    dict_head_to_head[team] = inner_dict

f = open("C:\\Users\\admistrteur\\Documents\\Python\\Lol_Worlds_Simulator\\2020data.csv", 'r')

line = f.readline().split(",")

while len(line) != 1 :
    dict_head_to_head[line[1]][line[2][:-1]].wins = dict_head_to_head[line[1]][line[2][:-1]].wins + 1
    dict_head_to_head[line[2][:-1]][line[1]].losses = dict_head_to_head[line[2][:-1]][line[1]].losses + 1
    line = f.readline().split(",")

for team in dict_head_to_head :
    print(team)
    for opponent, h2h in dict_head_to_head[team].items() :
        dict_head_to_head[team][opponent].ratio = dict_head_to_head[team][opponent].wins / (dict_head_to_head[team][opponent].wins + dict_head_to_head[team][opponent].losses)
        print(opponent + " " + str(h2h) + " ")
    print()

f.close()

# teams_ratings = {"TES" : 7.257, "DWG" : 7.207, "G2" : 6.884, "JDG" : 6.108, "DRX" : 5.789, "GEN" : 5.713, "FNC" : 5.564, "SN" : 5.224, "LGD" : 5.154, "RGE" : 4.714, "TSM" : 4.659, "MAD" : 4.383, "TL" : 3.736, "FLY" : 3.698, "UOL" : 3.000, "SUP": 1.674, "MCX" : 1.552, "PSG" : 1.547, "INZ" : 1.485, "V3" : 1.255, "R7" : 0.750, "LGC" : 0.646}

play_in_teams = ["TL", "MAD", "LGC", "SUP", "INZ", "LGD", "PSG", "V3", "UOL", "R7"]

play_in_group_A = ["TL", "MAD", "LGC", "SUP", "INZ"]
records_play_in_group_A = {"TL" : [], "MAD" : [], "LGC" : [], "SUP" : [], "INZ" : []}
group_A_play_in_init = Group(play_in_group_A, records_play_in_group_A)

play_in_group_B = ["LGD", "PSG", "V3", "UOL", "R7"]
records_play_in_group_B = {"LGD" : [], "PSG" : [], "V3" : [], "UOL" : [], "R7" : []}
group_B_play_in_init = Group(play_in_group_B, records_play_in_group_B)

play_in_qualified_teams = []

main_group_A = ["G2", "SN", "MCX"]
records_main_group_A = {"G2" : [], "SN" : [], "MCX" : []}
group_A_main_init = Group(main_group_A, records_main_group_A)

main_group_B = ["DWG", "JDG", "RGE"]
records_main_group_B = {"DWG" : [], "JDG" : [], "RGE" : []}
group_B_main_init = Group(main_group_B, records_main_group_B)

main_group_C = ["TSM", "GEN", "FNC"]
records_main_group_C = {"TSM" : [], "GEN" : [], "FNC" : []}
group_C_main_init = Group(main_group_C, records_main_group_C)

main_group_D = ["TES", "DRX", "FLY"]
records_main_group_D = {"TES" : [], "DRX" : [], "FLY" : []}
group_D_main_init = Group(main_group_D, records_main_group_D)

list_main_groups_init = [["G2", "SN", "MCX"], ["DWG", "JDG", "RGE"], ["TSM", "GEN", "FNC"], ["TES", "DRX", "FLY"]]

class Results_available :
    def __init__(self, p_group_A_play_in_res, p_group_B_play_in_res, p_barrages_res, p_group_A_main_res, p_group_B_main_res, p_group_C_main_res, p_group_D_main_res, p_coupe_phase_res) :
        self.group_A_play_in_res = p_group_A_play_in_res
        self.group_B_play_in_res = p_group_B_play_in_res
        self.barrages_res = p_barrages_res
        self.group_A_main_res = p_group_A_main_res
        self.group_B_main_res = p_group_B_main_res
        self.group_C_main_res_res = p_group_C_main_res
        self.group_D_main_res_res = p_group_D_main_res
        self.p_coupe_phase_res = p_coupe_phase_res

# Use these results value to launch a full simulation
dict_res_play_in_A = {"TL" : [], "MAD" : [], "LGC" : [], "SUP" : [], "INZ" : []}
dict_res_play_in_B = {"LGD" : [], "PSG" : [], "V3" : [], "UOL" : [], "R7" : []}
dict_no_res = {}

# Results are updated each day of competition
#dict_res_play_in_A = {"TL" : ["MAD", "LGC"], "MAD" : ["INZ"], "LGC" : ["INZ"], "SUP" : ["INZ", "MAD"], "INZ" : []}

#dict_res_play_in_B = {"LGD" : [], "PSG" : ["LGD", "R7"], "V3" : ["R7"], "UOL" : ["V3", "PSG"], "R7" : ["LGD"]}

dict_res_main_A = {"G2" : [], "SN" : [], "MCX" : []}
dict_res_main_B = {"DWG" : [], "JDG" : [], "RGE" : []}
dict_res_main_C = {"TSM" : [], "GEN" : [], "FNC" : []}
dict_res_main_D = {"TES" : [], "DRX" : [], "FLY" : []}

list_res_available = Results_available(dict_res_play_in_A, dict_res_play_in_B, dict_no_res, dict_res_main_A, dict_res_main_B, dict_res_main_C, dict_res_main_D, dict_no_res)

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
            ratio_win_A_over_B = dict_head_to_head[teamA][teamB].ratio
            if (not teamB in phase_res_available[teamA]) and (not teamA in phase_res_available[teamB]) :
                ratio_win_A_over_B = dict_head_to_head[teamA][teamB].ratio
                if random.uniform(0, 1) < ratio_win_A_over_B :
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

def all_games(group) :
    teams = group.group_teams
    records = group.group_records
    for i in range(len(teams)) :
        teamA = teams[i]
        for j in range(i + 1, len(teams)) :
            teamB = teams[j]
            ratio_win_A_over_B = dict_head_to_head[teamA][teamB].ratio
            if random.uniform(0, 1) < ratio_win_A_over_B :
                records[teamA].append(teamB)
            else :
                records[teamB].append(teamA)

    sorted_records ={}
    for team in sorted(records, key=lambda team: len(records[team]), reverse=True):
        sorted_records[team] = records[team]

    group.group_records = sorted_records

def best_of_n(nb_games, teamA, teamB) :
    vict_A = 0
    vict_B = 0
    games_to_win = (nb_games // 2) + 1
    while (vict_A < games_to_win and vict_B < games_to_win) :
        ratio_win_A_over_B = dict_head_to_head[teamA][teamB].ratio
        if (random.uniform(0, 1) < ratio_win_A_over_B) :
            vict_A = vict_A + 1
        else :
            vict_B = vict_B + 1
    if vict_A == games_to_win :
        return Result_BO(teamA, teamB)
    else :
        return Result_BO(teamB, teamA)

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

#retourne la place des équipes dans le cadre d'un tie breaker à 3 équipes pour 2 places (toutes les équipes peuvent finir dernière/éliminée)
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

#retourne la place des équipes dans le cadre d'un tie breaker à 3 équipes pour 1 place (toutes les équipes peuvent finir première)
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

#retourne l'ordre après un tie-break entre les 5 équipes d'un groupe de play-in
def tie_5_teams_for_5_seeds(list_teams) :
    pos = []
    order_list = choose_random_list(list_teams)
    result1 = best_of_n(1, order_list[3], order_list[4])
    result2 = best_of_n(1,order_list[0], result1.win_team)
    result3 = best_of_n(1, order_list[1], order_list[2])
    result4 = best_of_n(1, result2.lose_team, result3.lose_team)
    result5 = best_of_n(1, result2.win_team, result3.win_team)
    pos.append(result5.win_team)
    pos.append(result5.lose_team)
    pos.append(result4.win_team)
    pos.append(result4.lose_team)
    pos.append(result1.lose_team)
    return pos


def all_ties_play_in(results_group) :
    list_results_group = list(results_group.items())
    list_ties = []
    i = 0
    while i < 5 :
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

def all_ties_main(results_group) :
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

def resolve_play_in_ties(results_group, list_ties) :
    list_resolved_ties = []
    for to_tie in list_ties :
        seeds_to_tie = to_tie[0]
        teams_to_tie = to_tie[1]
        if len(teams_to_tie) == 1 :
            list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[0]))

        elif len(teams_to_tie) == 2 :
            if teams_to_tie[1] in results_group[teams_to_tie[0]] :
                list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[0]))
                list_resolved_ties.append((seeds_to_tie[1], teams_to_tie[1]))
            else :
                list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[1]))
                list_resolved_ties.append((seeds_to_tie[1], teams_to_tie[0]))

        elif len(teams_to_tie) == 3 :
            res_between_3 = head_to_head(results_group, teams_to_tie)
            res_between_3 = sorted(res_between_3.items(), key=lambda x: x[1], reverse=True)
            if res_between_3[0][1] == 2 or seeds_to_tie[0] == 1 :
                pos_3_ties = tie_1_seed_for_3_teams(teams_to_tie)
                for i in range(3) :
                    list_resolved_ties.append((seeds_to_tie[i], pos_3_ties[i]))
            else :
                pos_3_ties = tie_2_seeds_for_3_teams(teams_to_tie)
                for i in range(3) :
                    list_resolved_ties.append((seeds_to_tie[i], pos_3_ties[i]))

        else :
            random_list_teams = choose_random_list(teams_to_tie)
            pos = tie_5_teams_for_5_seeds(random_list_teams)
            for i in range(5) :
                list_resolved_ties.append((seeds_to_tie[i], pos[i]))

    return list_resolved_ties

def resolve_main_ties(results_group, list_ties) :
    list_resolved_ties = []
    for to_tie in list_ties :
        seeds_to_tie = to_tie[0]
        teams_to_tie = to_tie[1]
        if len(teams_to_tie) == 1 :
            list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[0]))

        elif len(teams_to_tie) == 2 :
            if teams_to_tie[1] in results_group[teams_to_tie[0]] :
                list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[0]))
                list_resolved_ties.append((seeds_to_tie[1], teams_to_tie[1]))
            else :
                list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[1]))
                list_resolved_ties.append((seeds_to_tie[1], teams_to_tie[0]))

        elif len(teams_to_tie) == 3 :
            res_between_3 = head_to_head(results_group, teams_to_tie)
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

def generate_all_quarters(list_first_seed, list_second_seed) :

    unique_combinations = []

    # Getting all permutations of list_1
    # with length of list_2
    permut = itertools.permutations(list(range(4)), 4)

    # zip() is called to pair each permutation
    # and shorter list element into combination
    for comb in permut:
        zipped = zip(comb, list(range(4)))
        unique_combinations.append(list(zipped))

    copy_permut = unique_combinations.copy()

    for permut in copy_permut :
        for match in permut :
            if match[0] == match[1] :
                unique_combinations.remove(permut)
                break
    return(unique_combinations)


def get_quarter(list_pos_groups, list_all_quarters) :
    list_matches = []
    i = random.randrange(9)
    affect_quarters = list_all_quarters[i]
    for match in affect_quarters :
        first_seed = list_pos_groups[match[0]][0][1]
        second_seed = list_pos_groups[match[1]][1][1]
        list_matches.append((first_seed, second_seed))
    return list_matches

def play_all_quarters(list_quarters) :
    results_quarters = []
    for match in list_quarters :
        results_quarters.append(best_of_n(5, match[0], match[1]).win_team)
    return results_quarters

def play_semis(res_quarters) :
    results_semis = []
    semi_finalist_1 = res_quarters[0]
    semi_finalist_2 = res_quarters[1]
    semi_finalist_3 = res_quarters[2]
    semi_finalist_4 = res_quarters[3]
    finalist_1 = best_of_n(5, semi_finalist_1, semi_finalist_2).win_team
    finalist_2 = best_of_n(5, semi_finalist_3, semi_finalist_4).win_team
    return (finalist_1, finalist_2)

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

    #print(results_play_in_group_B)

    list_ties_play_in_A = all_ties_play_in(results_play_in_group_A)
    list_ties_play_in_B = all_ties_play_in(results_play_in_group_B)

    group_A_play_in_pos = resolve_play_in_ties(results_play_in_group_A, list_ties_play_in_A)
    group_B_play_in_pos = resolve_play_in_ties(results_play_in_group_B, list_ties_play_in_B)

    play_in_qualified_teams = []

    play_in_qualified_teams.append(group_A_play_in_pos[0][1])
    play_in_qualified_teams.append(group_B_play_in_pos[0][1])

    res_group_A_play_in_3_4 = best_of_n(5, group_A_play_in_pos[2][1], group_A_play_in_pos[3][1])
    res_group_B_play_in_3_4 = best_of_n(5, group_B_play_in_pos[2][1], group_B_play_in_pos[3][1])

    play_in_group_A_3 = res_group_A_play_in_3_4.win_team
    play_in_group_B_3 = res_group_B_play_in_3_4.win_team

    res_match_2nd_A_3rd_B = best_of_n(5, group_A_play_in_pos[1][1], play_in_group_A_3)
    res_match_2nd_B_3rd_A = best_of_n(5, group_B_play_in_pos[1][1], play_in_group_B_3)

    play_in_qualified_teams.append(res_match_2nd_A_3rd_B.win_team)
    play_in_qualified_teams.append(res_match_2nd_B_3rd_A.win_team)

    print(play_in_qualified_teams)

    list_all_affects = []

    affects_group = []
    list_all_affects = affect_play_in_team(play_in_qualified_teams, affects_group)
    affect = choose_random_affect(list_all_affects)

    print(affect)

    return (affect, play_in_qualified_teams)

def main_groups(list_main_groups, affect) :

    place_affected_teams(list_main_groups, affect)

    for group in list_main_groups :
        print(group.group_teams)

    for group in list_main_groups :
        all_games(group)

    for group in list_main_groups :
        all_games(group)

    results_main_group_A = list_main_groups[0].group_records
    results_main_group_B = list_main_groups[1].group_records
    results_main_group_C = list_main_groups[2].group_records
    results_main_group_D = list_main_groups[3].group_records

    list_ties_main_A = all_ties_main(results_main_group_A)
    list_ties_main_B = all_ties_main(results_main_group_B)
    list_ties_main_C = all_ties_main(results_main_group_C)
    list_ties_main_D = all_ties_main(results_main_group_D)

    group_A_main_pos = resolve_main_ties(results_main_group_A, list_ties_main_A)
    group_B_main_pos = resolve_main_ties(results_main_group_B, list_ties_main_B)
    group_C_main_pos = resolve_main_ties(results_main_group_C, list_ties_main_C)
    group_D_main_pos = resolve_main_ties(results_main_group_D, list_ties_main_D)

    list_main_groups_pos = [group_A_main_pos, group_B_main_pos, group_C_main_pos, group_D_main_pos]

    list_all_quarters = generate_all_quarters(list(range(4)), list(range(4)))

    list_quarters = get_quarter(list_main_groups_pos, list_all_quarters)

    print(list_quarters)

    res_quarters = play_all_quarters(list_quarters)

    print(res_quarters)

    res_semis = play_semis(res_quarters)

    print(res_semis)

    final_winner = best_of_n(5, res_semis[0], res_semis[1]).win_team
    print(final_winner)
    return (final_winner, list_quarters)

def tournament() :
    group_A_play_in = copy.deepcopy(Group(play_in_group_A, records_play_in_group_A))
    group_B_play_in = copy.deepcopy(Group(play_in_group_B, records_play_in_group_B))

    (affect, list_qualified_from_play_in) = play_in(group_A_play_in, group_B_play_in)

    group_A_main = copy.deepcopy(Group(main_group_A, records_main_group_A))
    group_B_main = copy.deepcopy(Group(main_group_B, records_main_group_B))
    group_C_main = copy.deepcopy(Group(main_group_C, records_main_group_C))
    group_D_main = copy.deepcopy(Group(main_group_D, records_main_group_D))

    list_main_groups = [group_A_main, group_B_main, group_C_main, group_D_main]

    (champion, liste_quarts) = main_groups(list_main_groups, affect)

    print()

    return (champion, list_qualified_from_play_in, liste_quarts)

nb_victories = {}
nb_qualif_play_in = {}
nb_quarts = {}

for team in team_regions :
    nb_victories[team] = 0
    nb_quarts[team] = 0

for team in play_in_teams :
    nb_qualif_play_in[team] = 0

for i in range(100) :
    (champion, liste_qualifies_play_in, liste_quart_finalistes) = tournament()
    for quart_de_finale in liste_quart_finalistes :
        nb_quarts[quart_de_finale[0]] = nb_quarts[quart_de_finale[0]] + 1
        nb_quarts[quart_de_finale[1]] = nb_quarts[quart_de_finale[1]] + 1

    for team in liste_qualifies_play_in :
        nb_qualif_play_in[team] = nb_qualif_play_in[team] + 1

    nb_victories[champion] = nb_victories[champion] + 1

lp=sorted(nb_qualif_play_in.items())
fig, ax = plt.subplots()
ax.bar(range(len(lp)), [t[1] for t in lp]  , align="center")
ax.set_xticks(range(len(lp)))

ax.set_xticklabels([t[0] for t in lp])
fig.autofmt_xdate()
plt.title("Equipes des play-in se qualifiant (en head-to-head)")

l1=sorted(nb_quarts.items())
fig, ax = plt.subplots()
ax.bar(range(len(l1)), [t[1] for t in l1]  , align="center")
ax.set_xticks(range(len(l1)))
ax.set_xticklabels([t[0] for t in l1])
fig.autofmt_xdate()
plt.title("Quarts de finaliste (en head-to-head)")

l2=sorted(nb_victories.items())
fig, ax = plt.subplots()
ax.bar(range(len(l2)), [t[1] for t in l2]  , align="center")
ax.set_xticks(range(len(l2)))
ax.set_xticklabels([t[0] for t in l2])
fig.autofmt_xdate()
plt.title("Vainqueurs (en head-to-head)")

plt.show()


