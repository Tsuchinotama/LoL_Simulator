import copy
import random
import matplotlib.pyplot as plt

class Result_BO:
    def __init__(self, p_win_team, p_winner_score, p_lose_team, p_loser_score) :
        self.win_team = p_win_team
        self.score_winner = p_winner_score
        self.lose_team = p_lose_team
        self.score_loser = p_loser_score

class TeamRecords:
    def __init__(self, p_team):
        self.team = p_team
        self.series_win = 0
        self.series_lose = 0
        self.games_win = 0
        self.games_lose = 0
        self.reg_season_beated_teams_records = []

    def __lt__(self, other):
        if self.series_win < other.series_win:
            return True
        elif self.series_win > other.series_win:
            return False
        else: 
            if self.games_win - self.games_lose < other.games_win - other.games_lose:
                return True
            elif self.games_win - self.games_lose > other.games_win - other.games_lose:
                return False
            else:
                if len([rec for rec in self.reg_season_beated_teams_records if rec[0] == other.team]) == 2:
                    return True
                elif len([rec for rec in self.reg_season_beated_teams_records if rec[0] == other.team]) == 0:
                    return False
                else:
                    other_win_games = [rec for rec in self.reg_season_beated_teams_records if rec[0] == other.team][0][1]
                    self_win_games = [rec for rec in other.reg_season_beated_teams_records if rec[0] == self.team][0][1]
                    if self_win_games > other_win_games:
                        return True
                    elif self_win_games < other_win_games:
                        return False
                    else:

                        return self.team in other.reg_season_beated_teams_records

class TeamChampionshipPointsRecords:
    def __init__(self, p_team, p_championship_points, p_summer_records):
        self.team = p_team
        self.championship_points = p_championship_points
        self.summer_records = p_summer_records 

    def __lt__(self, other):
        if self.championship_points[0] + self.championship_points[1] < other.championship_points[0] + other.championship_points[1]:
            return True
        elif self.championship_points[0] + self.championship_points[1] > other.championship_points[0] + other.championship_points[1]:
            return False
        else: 
            if self.summer_records.games_win - self.summer_records.games_lose < other.summer_records.games_win - other.summer_records.games_lose:
                return True
            elif self.summer_records.games_win - self.summer_records.games_lose > other.summer_records.games_win - other.summer_records.games_lose:
                return False
            else:
                noise = random.uniform(-0.1, 0.1)
                odd_victory_self = min(max(0, 0.5 + (other.team - self.team) / 10 + noise), 1)
                if (random.uniform(0, 1) < odd_victory_self) :
                    return True
                else :
                    return False

nb_LCK_teams = 10
LCK_rankings = ["GENG", "T1", "KT", "DK", "HLE", "DRX", "LSB", "KDF", "NS", "BRI"]
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
    for teamA in range(1,nb_LCK_teams+1) :
        for teamB in range(teamA + 1, nb_LCK_teams+1):

            res_match = best_of_n(3, teamA, teamB)
            winner = res_match.win_team - 1 
            looser = res_match.lose_team - 1

            round_robin_res[winner].series_win += 1
            round_robin_res[winner].games_win += 2
            round_robin_res[winner].games_lose += res_match.score_loser
            round_robin_res[winner].reg_season_beated_teams_records.append((looser+1, res_match.score_loser))

            round_robin_res[looser].series_lose += 1
            round_robin_res[looser].games_win += res_match.score_loser
            round_robin_res[looser].games_lose += 2

def LCK_spring_playoff_phase1(reg_season_res, championship_points):
    choice_seed3 = max(reg_season_res[4].team,reg_season_res[5].team)
    choice_seed4 = min(reg_season_res[4].team,reg_season_res[5].team)
    res_match1 = best_of_n(5, reg_season_res[2].team, choice_seed3)
    res_match2 = best_of_n(5, reg_season_res[3].team, choice_seed4)

    loser_match1 = res_match1.lose_team
    winner_match1 = res_match1.win_team
    rank_loser1 = [i for i,record in enumerate(reg_season_res) if record.team == loser_match1][0]
    rank_winner1 = [i for i,record in enumerate(reg_season_res) if record.team == winner_match1][0]
    loser_match2 = res_match2.lose_team
    winner_match2 = res_match2.win_team
    rank_loser2 = [i for i,record in enumerate(reg_season_res) if record.team == loser_match2][0]
    rank_winner2 = [i for i,record in enumerate(reg_season_res) if record.team == winner_match2][0]

    if rank_loser1 < rank_loser2:
        championship_points[loser_match1 - 1][0] += 20
        championship_points[loser_match2 - 1][0] += 10
    else:
        championship_points[loser_match1 - 1][0] += 10
        championship_points[loser_match2 - 1][0] += 20

    return (winner_match1, rank_winner1, winner_match2, rank_winner2)

def LCK_spring_playoff_phase2(reg_season_res, SF4, SF3, championship_points):
    res_match1_winnerbracket = best_of_n(5, reg_season_res[0].team, SF4)  
    res_match2_winnerbracket = best_of_n(5, reg_season_res[1].team, SF3)

    res_match1_looserbracket = best_of_n(5, res_match1_winnerbracket.lose_team, res_match2_winnerbracket.lose_team)
    championship_points[res_match1_looserbracket.lose_team - 1][0] += 30

    res_match3_winnerbracket = best_of_n(5, res_match1_winnerbracket.win_team, res_match2_winnerbracket.win_team)
    res_match2_looserbracket = best_of_n(5, res_match3_winnerbracket.lose_team, res_match1_looserbracket.win_team)
    championship_points[res_match2_looserbracket.lose_team - 1][0] += 50

    res_grandfinal = best_of_n(5, res_match3_winnerbracket.win_team, res_match2_looserbracket.win_team)
    championship_points[res_grandfinal.lose_team - 1][0] += 70
    championship_points[res_grandfinal.win_team - 1][0] += 90

    return (res_grandfinal.win_team, res_grandfinal.lose_team)

def LCK_summer_playoff_phase1(reg_season_res, championship_points):
    res_match1_bracket1 = best_of_n(5, reg_season_res[7].team, reg_season_res[8].team)
    looser = res_match1_bracket1.lose_team - 1
    winner = res_match1_bracket1.win_team - 1
    losed_games = res_match1_bracket1.score_loser
    reg_season_res[looser].games_win += losed_games
    reg_season_res[looser].games_lose += 3
    reg_season_res[winner].games_win += 3
    reg_season_res[winner].games_lose += losed_games

    res_match2_bracket1 = best_of_n(5, reg_season_res[4].team, res_match1_bracket1.win_team)
    looser = res_match2_bracket1.lose_team - 1
    winner = res_match2_bracket1.win_team - 1
    losed_games = res_match2_bracket1.score_loser
    reg_season_res[looser].games_win += losed_games
    reg_season_res[looser].games_lose += 3
    reg_season_res[winner].games_win += 3
    reg_season_res[winner].games_lose += losed_games
    championship_points[looser][1] += 10

    res_match3_bracket1 = best_of_n(5, reg_season_res[3].team, res_match2_bracket1.win_team)
    looser = res_match3_bracket1.lose_team - 1
    winner = res_match3_bracket1.win_team - 1
    losed_games = res_match3_bracket1.score_loser
    reg_season_res[looser].games_win += losed_games
    reg_season_res[looser].games_lose += 3
    championship_points[looser][1] += 40

    res_match1_bracket2 = best_of_n(5, reg_season_res[6].team, reg_season_res[9].team)
    looser = res_match1_bracket2.lose_team - 1
    winner = res_match1_bracket2.win_team - 1
    losed_games = res_match1_bracket2.score_loser
    reg_season_res[looser].games_win += losed_games
    reg_season_res[looser].games_lose += 3
    reg_season_res[winner].games_win += 3
    reg_season_res[winner].games_lose += losed_games

    res_match2_bracket2 = best_of_n(5, reg_season_res[5].team, res_match1_bracket2.win_team)
    looser = res_match2_bracket2.lose_team - 1
    winner = res_match2_bracket2.win_team - 1
    losed_games = res_match2_bracket2.score_loser
    reg_season_res[looser].games_win += losed_games
    reg_season_res[looser].games_lose += 3
    reg_season_res[winner].games_win += 3
    reg_season_res[winner].games_lose += losed_games
    championship_points[looser][1] += 10

    res_match3_bracket2 = best_of_n(5, reg_season_res[2].team, res_match2_bracket2.win_team)   
    looser = res_match3_bracket2.lose_team - 1
    winner = res_match3_bracket2.win_team - 1
    losed_games = res_match3_bracket2.score_loser
    reg_season_res[looser].games_win += losed_games
    reg_season_res[looser].games_lose += 3
    championship_points[looser][1] += 40

    return (res_match3_bracket1.win_team, res_match3_bracket2.win_team)

def LCK_summer_playoff_phase2(reg_season_res, winner_bracket1, winner_bracket2, championship_points):
    res_match1_winnerbracket = best_of_n(5, reg_season_res[0].team, winner_bracket1)  
    res_match2_winnerbracket = best_of_n(5, reg_season_res[1].team, winner_bracket2)

    res_match1_looserbracket = best_of_n(5, res_match1_winnerbracket.lose_team, res_match2_winnerbracket.lose_team)
    championship_points[res_match1_looserbracket.lose_team - 1][1] += 60

    res_match3_winnerbracket = best_of_n(5, res_match1_winnerbracket.win_team, res_match2_winnerbracket.win_team)
    res_match2_looserbracket = best_of_n(5, res_match3_winnerbracket.lose_team, res_match1_looserbracket.win_team)
    championship_points[res_match2_looserbracket.lose_team - 1][1] += 80

    res_grandfinal = best_of_n(5, res_match3_winnerbracket.win_team, res_match2_looserbracket.win_team)
    championship_points[res_grandfinal.lose_team - 1][1] += 110
    # Give enough points to ensure qualification of summer winner as first seed
    championship_points[res_grandfinal.win_team - 1][1] += 210

    return res_grandfinal.win_team

def regional_qualifiers_LCK_for_3(regional_qualified_teams):
    res_winnerbracket = best_of_n(5, regional_qualified_teams[0].team, regional_qualified_teams[1].team)  
    seed3 = res_winnerbracket.win_team

    res_looserbracket = best_of_n(5, regional_qualified_teams[2].team, regional_qualified_teams[3].team)
    res_final_regio_qualif = best_of_n(5, res_winnerbracket.lose_team, res_looserbracket.win_team)
    seed4 = res_final_regio_qualif.win_team

    return (seed3, seed4)

def regional_qualifiers_LCK_for_4(regional_qualified_teams):
    res_winnerbracket = best_of_n(5, regional_qualified_teams[0].team, regional_qualified_teams[1].team)  
    seed3 = res_winnerbracket.win_team

    res_looserbracket = best_of_n(5, regional_qualified_teams[2].team, regional_qualified_teams[3].team)
    res_final_regio_qualif = best_of_n(5, res_winnerbracket.lose_team, res_looserbracket.win_team)
    seed4 = res_final_regio_qualif.win_team

    return (seed3, seed4)

nb_sim = 1000
for i in range(nb_sim):
    championship_points = [[0,0] for i in range(10)]

    spring_res = [TeamRecords(i) for i in range(1,11)]
    all_games_round_robin(spring_res)
    all_games_round_robin(spring_res)
    spring_res.sort(reverse=True)

    (semi_finalist3, SF3_rank, semi_finalist4, SF4_rank) = LCK_spring_playoff_phase1(spring_res, championship_points)

    if SF3_rank > SF4_rank:
        semi_finalist3, semi_finalist4 = semi_finalist4, semi_finalist3

    (spring_winner,spring_finalist) = LCK_spring_playoff_phase2(spring_res, semi_finalist4, semi_finalist3, championship_points)

    nb_qualifs_MSI[spring_winner-1] += 1
    nb_qualifs_MSI[spring_finalist-1] += 1

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

    # (winner_bracket1, winner_bracket2) = LCK_summer_playoff_phase1(summer_res, championship_points)

    # LCK_summer_playoff_phase2(summer_res, winner_bracket1, winner_bracket2, championship_points)

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
    #     (seed3,seed4) = regional_qualifiers_LCK_for_3(championship_points_res[2:6])
    #     worlds_qualified_teams.append(seed3)
    # else:
    #     (seed3,seed4) = regional_qualifiers_LCK_for_4(championship_points_res[2:6])
    #     worlds_qualified_teams += [seed3, seed4]

    # for team in MSI_qualified_teams:
    #     nb_qualifs_MSI[team-1] += 1

avg_strength = 0
print("Nb de qualifs :")
for i,team in enumerate(LCK_rankings):
    print(team + " : " + str(nb_qualifs_MSI[i]))
    avg_strength += nb_qualifs_MSI[i]*(i+1)
print("Force moyenne d'une équipe LCK qualifiée au MSI : " + str(avg_strength / (2 * nb_sim)))

avg_strength = avg_strength / (2 * nb_sim)

#lp = sorted(nb_qualifs_worlds.items())
fig, ax = plt.subplots()
ax.bar(range(len(nb_qualifs_MSI)), [t for t in nb_qualifs_MSI]  , align="center")
ax.set_xticks(range(len(nb_qualifs_MSI)))
ax.set_xticklabels(LCK_rankings)
fig.autofmt_xdate()
plt.title("Equipes de LCK se qualifiant aux MSI (sur 1000 simulations, classement basé sur l'année 2023) ; Rang moyen : " + str(avg_strength), wrap=True)
for i, v in enumerate(nb_qualifs_MSI):
    plt.text(i - 0.25, v +0.5, str(v))
plt.show()