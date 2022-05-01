import random
import collections
import itertools
from itertools import permutations
import matplotlib.pyplot as plt
import numpy as np
import copy
import time

teams_ratings = {"TES" : 7.257, "DWG" : 7.207, "G2" : 6.884, "JDG" : 6.108, "DRX" : 5.789, "GEN" : 5.713, "FNC" : 5.564, "SNG" : 5.224}

list_quarters = [('TES', 'FNC'), ('JDG', 'SNG'), ('G2', 'GEN'), ('DWG', 'DRX')]

team_regions = {"TES" : "CHN", "JDG" : "CHN", "SNG" : "CHN", "G2" : "EU", "FNC" : "EU", "DWG" : "KR", "DRX" : "KR", "GEN" : "KR"}

class Result_BO :
    def __init__(self, p_win_team, p_win_team_wins, p_lose_team, p_lose_team_wins) :
        self.win_team = p_win_team
        self.win_team_wins = p_win_team_wins
        self.lose_team = p_lose_team
        self.lose_team_wins = p_lose_team_wins

    def __str__(self) :
        return (self.win_team + " " + str(self.win_team_wins) + "-" + str(self.lose_team_wins) + " " + self.lose_team)

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
        return Result_BO(team_A, vict_A, team_B, vict_B)
    else :
        return Result_BO(team_B, vict_B, team_A, vict_A)

def play_all_quarters(list_quarters) :
    results_quarters = []
    for match in list_quarters :
        results_quarters.append(best_of_n(5, match[0], match[1]))
    return results_quarters

def play_semis(res_quarters) :
    results_semis = []
    semi_finalist_1 = res_quarters[0].win_team
    semi_finalist_2 = res_quarters[1].win_team
    semi_finalist_3 = res_quarters[2].win_team
    semi_finalist_4 = res_quarters[3].win_team
    semi_final_1 = best_of_n(5, semi_finalist_1, semi_finalist_2)
    semi_final_2 = best_of_n(5, semi_finalist_3, semi_finalist_4)
    return (semi_final_1, semi_final_2)

def knock_out_stage() :
    print("Résultats des quarts de finale : ")
    res_quarters = play_all_quarters(list_quarters)
    for quarts in res_quarters :
        print(quarts)
    semi_finalists = [res_quarters[i].win_team for i in range(4)]

    print()

    print("Résultats des demies finale : ")
    res_semis = play_semis(res_quarters)
    for demie in res_semis :
        print(demie)

    print()

    print("Résultat de la finale : ")
    final = best_of_n(5, res_semis[0].win_team, res_semis[1].win_team)
    print(final)

    return (final.win_team, [res_semis[0].win_team, res_semis[1].win_team], semi_finalists)

nb_victoires = {}
nb_finales = {}
nb_demies = {}

for team in team_regions :
    nb_victoires[team] = 0
    nb_finales[team] = 0
    nb_demies[team] = 0

for i in range(1) :
    (champion, liste_finalistes, liste_demi_finalistes) = knock_out_stage()
    for semie in liste_demi_finalistes :
        nb_demies[semie] = nb_demies[semie] + 1
    for finaliste in liste_finalistes :
        nb_finales[finaliste] = nb_finales[finaliste] + 1

    nb_victoires[champion] = nb_victoires[champion] + 1

l1=sorted(nb_demies.items())
fig, ax = plt.subplots()
ax.bar(range(len(l1)), [t[1] for t in l1]  , align="center")
ax.set_xticks(range(len(l1)))
ax.set_xticklabels([t[0] for t in l1])
fig.autofmt_xdate()
plt.title("Demi-finalistes")

l2=sorted(nb_finales.items())
fig, ax = plt.subplots()
ax.bar(range(len(l2)), [t[1] for t in l2]  , align="center")
ax.set_xticks(range(len(l2)))
ax.set_xticklabels([t[0] for t in l2])
fig.autofmt_xdate()
plt.title("Finalistes")

l3=sorted(nb_victoires.items())
fig, ax = plt.subplots()
ax.bar(range(len(l3)), [t[1] for t in l3]  , align="center")
ax.set_xticks(range(len(l3)))
ax.set_xticklabels([t[0] for t in l3])
fig.autofmt_xdate()
plt.title("Vainqueurs")

plt.show()

