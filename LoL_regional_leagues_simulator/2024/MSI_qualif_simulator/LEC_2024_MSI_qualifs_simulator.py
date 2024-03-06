import copy
import random
import matplotlib.pyplot as plt
from functools import cmp_to_key

class Group :
    def __init__(self, p_group_teams, p_group_records) :
        self.group_teams = p_group_teams
        self.group_records = p_group_records

    def __str__(self) :
        return ("équipes du groupe : " + str(self.group_records))

class Result_BO:
    def __init__(self, p_win_team, p_winner_score, p_lose_team, p_loser_score) :
        self.win_team = p_win_team
        self.score_winner = p_winner_score
        self.lose_team = p_lose_team
        self.score_loser = p_loser_score

class TeamRecords:
    def __init__(self, p_team):
        self.team = p_team
        self.games_win = 0
        self.reg_season_beated_teams_records = []

    def __lt__(self, other):
        if self.games_win < other.games_win :
            return True
        elif self.games_win > other.games_win :
            return False
        else:
            return self.team in other.reg_season_beated_teams_records

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

class TeamChampionshipPointsRecords:
    def __init__(self, p_team, p_championship_points):
        self.team = p_team
        self.championship_points = p_championship_points
        self.summer_records

    def __lt__(self, other):
        if (self.championship_points[0] + self.championship_points[1] <
            other.championship_points[0] + other.championship_points[1]) :
            return True
        elif (self.championship_points[0] + self.championship_points[1] >
            other.championship_points[0] + other.championship_points[1]) :
            return False
        else: 
            if self.championship_points[1] < other.championship_points[1] :
                return True
            elif self.championship_points[1] > other.championship_points[1] :
                return False

nb_LEC_teams = 10
LEC_rankings = ["G2", "FNC", "MDK", "BDS", "XL", "SK", "VIT", "TH", "RGE", "KC"]
nb_qualifs_MSI = [0 for i in range(10)]

def best_of_n(nb_games, team_A, team_B) :
    vict_A = 0
    vict_B = 0
    games_to_win = (nb_games // 2) + 1

    # if team_A == 9:
    #     return Result_BO(team_A, vict_A, team_B, 0)
    # elif team_B == 9:
    #     return Result_BO(team_B, vict_B, team_A, 0)
    
    while (vict_A < games_to_win and vict_B < games_to_win) :
        noise = random.uniform(-0.1, 0.1)
        #noise = 0
        odd_victory_A = min(max(0, 0.5 + (team_B - team_A) / 10 + noise), 1)
        if (random.uniform(0, 1) < odd_victory_A) :
            vict_A = vict_A + 1
        else :
            vict_B = vict_B + 1
    if vict_A == games_to_win :
        return Result_BO(team_A, vict_A, team_B, vict_B)
    else :
        return Result_BO(team_B, vict_B, team_A, vict_A)

def all_games_round_robin(round_robin_res) :
    records = {i : [] for i in range(1,nb_LEC_teams+1)}
    for teamA in range(1,nb_LEC_teams+1) :
        for teamB in range(teamA + 1, nb_LEC_teams+1):

            res_match = best_of_n(1, teamA, teamB)
            winner = res_match.win_team - 1 
            looser = res_match.lose_team - 1

            round_robin_res[winner].games_win += 1
            round_robin_res[winner].reg_season_beated_teams_records.append(looser+1)
            records[winner+1].append(looser+1)

    sorted_records ={}
    for team in sorted(records, key=lambda team: len(records[team]), reverse=True):
        sorted_records[team] = records[team]

    round_robin_res.sort(reverse=True)
    return sorted_records

def all_ties(sorted_records) :
    list_results_group = list(sorted_records.items())
    list_ties = []
    i = 0
    while i < 10 :
        res_team = list_results_group[i]
        teams_tied = ([i + 1], [res_team[0]])
        j = i + 1
        while j < 10 and (len(res_team[1]) == len(list_results_group[j][1])) :
            teams_tied[0].append(j + 1)
            teams_tied[1].append(list_results_group[j][0])
            j = j + 1

        list_ties.append(teams_tied)
        i = j
    return list_ties

def head_to_head(res, teams) :
    dict_tie = {}
    for team in teams :
        dict_tie[team] = 0
        for beated in res[team] :
            if beated in teams :
                dict_tie[team] = dict_tie[team] + 1
    return dict_tie

def strength_victory_score(res, list_ties) :
    # list_scores = []
    dict_score = {}
    full_score = 10
    for (ranks,teams) in list_ties :
        if len(ranks) == 1 :
            # list_scores.append({teams[0], full_score - ranks[0] + 1})
            dict_score[teams[0]] = full_score - ranks[0] + 1

        elif len(ranks) == 2 :
            teamA = teams[0]
            teamB = teams[1]
            if teamB in res[teamA]:
                # list_scores.append({teamA, full_score - ranks[0] + 1})
                # list_scores.append({teamB, full_score - ranks[0]})
                dict_score[teamA] = full_score - ranks[0] + 1
                dict_score[teamB] = full_score - ranks[0]
            else: 
                # list_scores.append({teamB, full_score - ranks[0] + 1})
                # list_scores.append({teamA, full_score - ranks[0]})
                dict_score[teamB] = full_score - ranks[0] + 1
                dict_score[teamA] = full_score - ranks[0]

        else:
            for team in teams :
                # list_scores.append({teams[0], full_score - ranks[0] + 1})
                dict_score[team] = full_score - ranks[0] + 1

    return dict_score

#retourne la place des équipes dans le cadre d'un tie breaker à 3 équipes pour 2 places (toutes les équipes peuvent finir 1ère/qualifiée)
def tie_1_seed_for_3_teams(res_between_3) :
    tie_break = {"finalist":0, "semi":(0,0)}
    #une équipe a gagné vs les 2 autres en matchs particuliers, ou a un meilleur score que les 2 autres, et va en match qualificatif du tie-break
    if res_between_3[0][1][0] == 2 or (res_between_3[0][1][1] > res_between_3[1][1][1]):
        tie_break["finalist"] = res_between_3[2][0]
        tie_break["semi"] = (res_between_3[0][0],res_between_3[1][0])
    else:
        #pour les temps de victoire, tirage aléatoire
        pos_loser = random.randint(0,3)
        tie_break["finalist"] = res_between_3[pos_loser][0]
        tie_break["semi"] = tuple([team[0] for i, team in enumerate(res_between_3) if i != pos_loser])
    pos = []
    result1 = best_of_n(1, tie_break["semi"][0], tie_break["semi"][1])
    result2 = best_of_n(1, tie_break["finalist"], result1.win_team)
    pos.append(result2.win_team)
    pos.append(result2.lose_team)
    pos.append(result1.lose_team)
    return pos

#retourne la place des équipes dans le cadre d'un tie breaker à 3 équipes pour 2 places (toutes les équipes peuvent finir dernière/éliminée)
def tie_2_seeds_for_3_teams(res_between_3) :
    tie_break = {"loser":0, "semi":(0,0)}
    #une équipe a perdu vs les 2 autres en matchs particuliers, ou a un moins bon score que les 2 autres, et va en match éliminatoire du tie-break
    if res_between_3[2][1][0] == 0 or (res_between_3[2][1][1] < res_between_3[1][1][1]):
        tie_break["loser"] = res_between_3[2][0]
        tie_break["semi"] = (res_between_3[0][0],res_between_3[1][0])
    else:
        #pour les temps de victoire, tirage aléatoire
        pos_loser = random.randint(0,3)
        tie_break["loser"] = res_between_3[pos_loser][0]
        tie_break["semi"] = tuple([team[0] for i, team in enumerate(res_between_3) if i != pos_loser])
    pos = []
    result1 = best_of_n(1, tie_break["semi"][0], tie_break["semi"][1])
    result2 = best_of_n(1, tie_break["loser"], result1.lose_team)
    pos.append(result1.win_team)
    pos.append(result2.win_team)
    pos.append(result2.lose_team)
    return pos

def resolve_ties(res, list_ties) :
    dict_score = strength_victory_score(res, list_ties)
    list_resolved_ties = []
    for to_tie in list_ties :
        
        seeds_to_tie = to_tie[0]
        teams_to_tie = to_tie[1]

        if len(teams_to_tie) == 1 :
            list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[0]))

        else:
            if (8 in seeds_to_tie) and (9 in seeds_to_tie):

                if len(teams_to_tie) == 2 :
                    tie_break = best_of_n(1, teams_to_tie[0], teams_to_tie[1])
                    list_resolved_ties.append((seeds_to_tie[0], tie_break.win_team))
                    list_resolved_ties.append((seeds_to_tie[1], tie_break.lose_team))

                    # if teams_to_tie[1] in res[teams_to_tie[0]] :
                    #     list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[0]))
                    #     list_resolved_ties.append((seeds_to_tie[1], teams_to_tie[1]))
                    # else :
                    #     list_resolved_ties.append((seeds_to_tie[0], teams_to_tie[1]))
                    #     list_resolved_ties.append((seeds_to_tie[1], teams_to_tie[0]))

                elif len(teams_to_tie) == 3 :
                    res_between_3 = head_to_head(res, teams_to_tie)
                    res_between_3_scored = {sing_res : (res_between_3[sing_res], sum(dict_score[beated] for beated in res[sing_res])) for sing_res in res_between_3.keys()}
                    res_between_3_scored = sorted(res_between_3_scored.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)

                    if seeds_to_tie[0] == 8 :
                        pos_3_ties = tie_1_seed_for_3_teams(res_between_3_scored)
                        for i in range(3) :
                            list_resolved_ties.append((seeds_to_tie[i], pos_3_ties[i]))
                    else :
                        pos_3_ties = tie_2_seeds_for_3_teams(res_between_3_scored)
                        for i in range(3) :
                            list_resolved_ties.append((seeds_to_tie[i], pos_3_ties[i]))

                # 4-way ties or more with 8th place involved
                else:
                    limit_tie = 8 - seeds_to_tie[0]
                    

                    res_between_tie = head_to_head(res, teams_to_tie)
                    res_between_tie_scored = {sing_res : (res_between_tie[sing_res], sum(dict_score[beated] for beated in res[sing_res])) for sing_res in res_between_tie.keys()}
                    res_between_tie_scored = sorted(res_between_tie_scored.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)

                    if res_between_tie_scored[limit_tie-1][1] > res_between_tie_scored[limit_tie][1][0]:
                        if seeds_to_tie[-1] == 9:
                            tie_break = best_of_n(1, teams_to_tie[0], teams_to_tie[1])
                            list_resolved_ties.append((8, tie_break.win_team))
                            list_resolved_ties.append((9, tie_break.lose_team))
                        

                    l = 0

    return list_resolved_ties

list_ties_test = [([1], [1])] + [([2], [2])] + [([3, 4], [3, 4])] + [([5], [5])] + [([6, 7, 8, 9, 10], [6, 7, 8, 9, 10])]
# list_ties_test = [([i], [i]) for i in range(1, 8)] + [([8, 9, 10], [8, 9, 10])]
# res_test = {i : list(range(i+1, 11)) for i in range(4, 8)}
# res1 = list(range(2, 11))
# res1.remove(8)
# res_test[1] = res1

# res2 = list(range(3, 11))
# res2.remove(9)
# res_test[2] = res2

# res3= list(range(4, 11))
# res3.remove(10)
# res_test[3] = res3

# res_test[7] = [1, 8, 10]
# res_test[8] = [2, 9, 10]
# res_test[9] = [3, 7, 10]

res_test = {i : list(range(i+1, 11)) for i in range(1, 6)}
res_test[6] = [7, 8]
res_test[7] = [8, 9]
res_test[8] = [9, 10]
res_test[9] = [6, 10]
res_test[10] = [6, 7]
resolve_ties(res_test, list_ties_test)
l = 0

def choose_random_list(list_teams) :
    copy_list = list_teams[:]
    new_list = []
    for i in range(len(list_teams)) :
        item = copy_list[random.randrange(0, len(list_teams) - i)]
        new_list.append(item)
        copy_list.remove(item)
    return new_list


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

def LEC_winter_playoff(tree, championship_points):
    res_winner1_match1 = best_of_n(3, tree[0][0], tree[0][1])
    res_winner1_match2 = best_of_n(3, tree[1][0], tree[1][1])
    res_winner1_match3 = best_of_n(3, tree[2][0], tree[2][1])
    res_winner1_match4 = best_of_n(3, tree[3][0], tree[3][1])

    res_winner2_match1 = best_of_n(3, res_winner1_match1.win_team, res_winner1_match2.win_team)
    res_winner2_match2 = best_of_n(3, res_winner1_match3.win_team, res_winner1_match4.win_team)

    res_winner4 = best_of_n(5, res_winner2_match1.win_team, res_winner2_match2.win_team)

    res_loser1_match1 = best_of_n(3, res_winner1_match3.lose_team, res_winner1_match4.lose_team)
    res_loser1_match2 = best_of_n(3, res_winner1_match1.lose_team, res_winner1_match2.lose_team)
    championship_points[res_loser1_match1.lose_team - 1][0] += 30
    championship_points[res_loser1_match2.lose_team - 1][0] += 30

    res_loser2_match1 = best_of_n(3, res_winner2_match1.lose_team, res_loser1_match1.lose_team)
    res_loser2_match2 = best_of_n(3, res_winner2_match2.lose_team, res_loser1_match2.lose_team)
    championship_points[res_loser2_match1.lose_team - 1][0] += 45
    championship_points[res_loser2_match2.lose_team - 1][0] += 45

    res_loser3 = best_of_n(5, res_loser2_match1.win_team, res_loser2_match2.win_team)
    championship_points[res_loser3.lose_team - 1][0] += 60

    res_loser4 = best_of_n(5, res_winner4.lose_team, res_loser3.win_team)
    championship_points[res_loser4.lose_team - 1][0] += 80  

    res_final = best_of_n(5, res_winner4.win_team, res_loser4.win_team)
    championship_points[res_final.lose_team - 1][0] += 100
    championship_points[res_final.win_team - 1][0] += 120

    return res_final.win_team

def LEC_spring_playoff(tree, championship_points):
    res_winner1_match1 = best_of_n(3, tree[0][0], tree[0][1])
    res_winner1_match2 = best_of_n(3, tree[1][0], tree[1][1])
    res_winner1_match3 = best_of_n(3, tree[2][0], tree[2][1])
    res_winner1_match4 = best_of_n(3, tree[3][0], tree[3][1])

    res_winner2_match1 = best_of_n(3, res_winner1_match1.win_team, res_winner1_match2.win_team)
    res_winner2_match2 = best_of_n(3, res_winner1_match3.win_team, res_winner1_match4.win_team)

    res_winner4 = best_of_n(5, res_winner2_match1.win_team, res_winner2_match2.win_team)

    res_loser1_match1 = best_of_n(3, res_winner1_match3.lose_team, res_winner1_match4.lose_team)
    res_loser1_match2 = best_of_n(3, res_winner1_match1.lose_team, res_winner1_match2.lose_team)
    championship_points[res_loser1_match1.lose_team - 1][0] += 35
    championship_points[res_loser1_match2.lose_team - 1][0] += 35

    res_loser2_match1 = best_of_n(3, res_winner2_match1.lose_team, res_loser1_match1.lose_team)
    res_loser2_match2 = best_of_n(3, res_winner2_match2.lose_team, res_loser1_match2.lose_team)
    championship_points[res_loser2_match1.lose_team - 1][0] += 55
    championship_points[res_loser2_match2.lose_team - 1][0] += 55

    res_loser3 = best_of_n(5, res_loser2_match1.win_team, res_loser2_match2.win_team)
    championship_points[res_loser3.lose_team - 1][0] += 70

    res_loser4 = best_of_n(5, res_winner4.lose_team, res_loser3.win_team)
    championship_points[res_loser4.lose_team - 1][0] += 95  

    res_final = best_of_n(5, res_winner4.win_team, res_loser4.win_team)
    championship_points[res_final.lose_team - 1][0] += 120
    championship_points[res_final.win_team - 1][0] += 145

    return res_final.win_team

def LEC_summer_playoff(tree, championship_points):
    res_winner1_match1 = best_of_n(3, tree[0][0], tree[0][1])
    res_winner1_match2 = best_of_n(3, tree[1][0], tree[1][1])
    res_winner1_match3 = best_of_n(3, tree[2][0], tree[2][1])
    res_winner1_match4 = best_of_n(3, tree[3][0], tree[3][1])

    res_winner2_match1 = best_of_n(3, res_winner1_match1.win_team, res_winner1_match2.win_team)
    res_winner2_match2 = best_of_n(3, res_winner1_match3.win_team, res_winner1_match4.win_team)

    res_winner4 = best_of_n(5, res_winner2_match1.win_team, res_winner2_match2.win_team)

    res_loser1_match1 = best_of_n(3, res_winner1_match3.lose_team, res_winner1_match4.lose_team)
    res_loser1_match2 = best_of_n(3, res_winner1_match1.lose_team, res_winner1_match2.lose_team)
    championship_points[res_loser1_match1.lose_team - 1][1] += 35
    championship_points[res_loser1_match2.lose_team - 1][1] += 35

    res_loser2_match1 = best_of_n(3, res_winner2_match1.lose_team, res_loser1_match1.lose_team)
    res_loser2_match2 = best_of_n(3, res_winner2_match2.lose_team, res_loser1_match2.lose_team)
    championship_points[res_loser2_match1.lose_team - 1][1] += 55
    championship_points[res_loser2_match2.lose_team - 1][1] += 55

    res_loser3 = best_of_n(5, res_loser2_match1.win_team, res_loser2_match2.win_team)
    championship_points[res_loser3.lose_team - 1][1] += 70

    res_loser4 = best_of_n(5, res_winner4.lose_team, res_loser3.win_team)
    championship_points[res_loser4.lose_team - 1][1] += 95  

    res_final = best_of_n(5, res_winner4.win_team, res_loser4.win_team)
    championship_points[res_final.lose_team - 1][1] += 120
    championship_points[res_final.win_team - 1][1] += 145

    return (res_final.win_team, res_final.lose_team, res_loser4.lose_team)

n = 100
for i in range(n):
    championship_points = [[0,0] for i in range(17)]

    spring_res = [TeamRecords(i) for i in range(1,18)]
    sorted_records = all_games_round_robin(spring_res)
    list_all_ties = all_ties(sorted_records)
    reg_season_pos =  resolve_ties(sorted_records, list_all_ties)
    winter_winner = LEC_winter_playoff(spring_res, championship_points)


    spring_winner = LEC_spring_playoff(spring_res, championship_points)

    nb_qualifs_MSI[spring_winner-1] += 1
    
    if winter_winner == spring_winner :
        championship_points_res = [TeamChampionshipPointsRecords(i, championship_points[i-1]) for i in range(1,11)]
        #ranking = list(enumerate(championship_points_res))
        championship_points_res.sort(reverse = True)

    else:
        nb_qualifs_MSI[winter_winner-1] += 1

    # summer_res = [TeamRecords(i) for i in range(1,18)]
    # all_games_round_robin(summer_res)

    # MSI_winner_auto_qualif = True
    # MSI_qualified_teams = []
    # worlds_auto_qualif_team = None
    # if random.uniform(0,1) < 0.5:
    #     if spring_winner in [summer_res[i].team for i in range(10)]:
    #         MSI_qualified_teams.append(spring_winner)
    #     else:
    #         MSI_winner_auto_qualif = False
    # else:
    #     if spring_finalist in [summer_res[i].team for i in range(10)]:
    #         MSI_qualified_teams.append(spring_finalist)
    #     else:
    #         MSI_winner_auto_qualif = False 

    # (winner_bracket1, winner_bracket2) = LEC_summer_playoff_phase1(summer_res, championship_points)

    # LEC_summer_playoff_phase2(summer_res, winner_bracket1, winner_bracket2, championship_points)

    # ind_ranking_res = {}
    # for i,record in enumerate(summer_res):
    #     ind_ranking_res[record.team] = i

    # championship_points_res = [TeamChampionshipPointsRecords(i, championship_points[i-1], summer_res[ind_ranking_res[i]]) for i in range(1,11)]
    # #ranking = list(enumerate(championship_points_res))
    # championship_points_res.sort(reverse = True)

    # championship_points_res = [rec for rec in championship_points_res if not rec.team in MSI_qualified_teams]
    # MSI_qualified_teams += [championship_points_res[0].team, championship_points_res[1].team]

    # regional_qualified_teams= []
    # for record in championship_points_res[2:6]:
    #     regional_qualified_teams.append(record.team)

    # if MSI_winner_auto_qualif:
    #     (seed3,seed4) = regional_qualifiers_LEC_for_3(championship_points_res[2:6])
    #     worlds_qualified_teams.append(seed3)
    # else:
    #     (seed3,seed4) = regional_qualifiers_LEC_for_4(championship_points_res[2:6])
    #     worlds_qualified_teams += [seed3, seed4]

    # for team in MSI_qualified_teams:
    #     nb_qualifs_MSI[team-1] += 1

avg_strength = 0
print("Nb de qualifs :")
for i,team in enumerate(LEC_rankings):
    print(team + " : " + str(nb_qualifs_MSI[i]))
    avg_strength += nb_qualifs_MSI[i]*(i+1)
print("Force moyenne d'une équipe LCK qualifiée au MSI : " + str(avg_strength / (2*n)))

#lp = sorted(nb_qualifs_worlds.items())
fig, ax = plt.subplots()
ax.bar(range(len(nb_qualifs_MSI)), [t for t in nb_qualifs_MSI]  , align="center")
ax.set_xticks(range(len(nb_qualifs_MSI)))
ax.set_xticklabels(LEC_rankings)
fig.autofmt_xdate()
plt.title("Equipes de LEC se qualifiant aux MSI (sur " + str(n) + "1000 simulations, classement basé sur l'année 2023)", wrap=True)

plt.show()