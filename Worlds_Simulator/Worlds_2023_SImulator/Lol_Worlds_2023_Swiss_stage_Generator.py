import math
import itertools

def equipart(s, p):
    import itertools
    if len(s) % p != 0:
        raise ValueError("Set must be of a length which is a multiple of p")
    com = map(set, set(itertools.combinations(s, p)))
    res = [x for x in itertools.combinations(com, int(len(s)/p)) if set().union(*x) == s]
    return res

res2 = list(itertools.combinations(
    {"JDG", "BLG", "LNG", "WBG", "G2", "FNC"}, 3
))

print(len(res2))

res3 = [frozenset(tuple_qualif) for tuple_qualif in res2]

print(res3)
for line in res3:
    print(line)

swiss_stage_teams = [
    "JDG", "BLG", "LNG", "WBG", 
    "G2", "FNC", "MAD", "BDS", 
    "GENG", "T1", "KT", "DK", 
    "NRG", "C9", "TL", "GAM"
]

region_teams = {
    "CHN" : ["JDG", "BLG", "LNG", "WBG"], 
    "EU" : ["G2", "FNC", "MAD", "BDS"], 
    "KR" : ["GENG", "T1", "KT", "DK"], 
    "NA" : ["NRG", "C9", "TL"], 
    "VCS": ["GAM"]
}

team_regions = {
    "JDG" : "CHN", "BLG" : "CHN", "LNG" : "CHN", "WBG" : "CHN", 
    "G2" : "EU", "FNC" : "EU", "MAD" : "EU", "BDS" : "EU", 
    "GENG" : "KR", "T1" : "KR", "KT" : "KR", "DK" : "KR", 
    "NRG" : "NA", "C9" : "NA", "TL" : "NA", "GAM" : "VCS"
}

# Betting odd based on https://esportbet.com/league-of-legends/worlds/
teams_rating = {
    "JDG" : 2.1, "GENG" : 5.00, "LNG" : 6.00, "T1" : 7.00, 
    "BLG" : 9.00, "WBG" : 12.00, "KT" : 12.00, "DK" : 15.00, 
    "G2" : 25.00, "FNC" : 45.00, "C9" : 65.00, "MAD" : 67.00, 
    "TL" : 200.00, "NRG" : 201.00, "BDS" : 300.00, "GAM" : 500.00
}

def win_chance(team, opponent):
    return teams_rating[opponent] / (teams_rating[team] + teams_rating[opponent])

teams_score = {team : (0, 0) for team in swiss_stage_teams}

swiss_stage_init = [
    ("BLG", "KT"), ("C9", "MAD"), ("DK", "G2"), ("FNC", "LNG"), ("GAM", "GENG"), ("T1", "TL"), ("JDG", "BDS"), ("WBG", "NRG")
]

#list_main_phase = [[["JDG"], []], [["GENG"], []]]

qualifs_raw = itertools.combinations(
    {
        "JDG", "BLG", "LNG", "WBG", 
        "G2", "FNC", "MAD", "BDS", 
        "GENG", "T1", "KT", "DK", 
        "NRG", "C9", "TL", "GAM"
    }, 8
)
qualifs_all = [frozenset(qualif) for qualif in qualifs_raw]


list_all_main_phase = []
dict_all_swiss_stage = {}

round3_2_0 = [("LNG", "JDG"), ("GENG", "G2")]
round3_1_1 = [("BLG", "FNC"), ("T1", "C9"), ("WBG", "KT"), ("NRG", "MAD")]
round3_0_2 = [("BDS", "DK"), ("TL", "GAM")]

for all_res in range(int(math.pow(2, 6))):
    proba = 1.0
    # set_winner_round1 = set()
    # set_loser_round1 = set()
    # for ind_match_round1 in range(8):
    #     res_match_round1 = (all_res >> ind_match_round1) & 1
    #     win_team_match_round1 = swiss_stage_init[ind_match_round1][res_match_round1]
    #     lose_team_match_round1 = swiss_stage_init[ind_match_round1][1-res_match_round1]
    #     set_winner_round1.add(win_team_match_round1)
    #     set_loser_round1.add(lose_team_match_round1)
    #     #Change here for probability calcul
    #     if ( team_regions[win_team_match_round1] in ["CHN", "KR"] ) and (team_regions[lose_team_match_round1] in ["EU", "NA"]):
    #         proba = 0.0
    #     else:
    #         proba *= win_chance(win_team_match_round1, lose_team_match_round1) 
    # else: 
    #     print("End of first round")

    # for round2_1_0_draw in equipart(set_winner_round1, 2):
    #     #for all_res_round2_1_0 in range(int(math.pow(2, 4))):
    #     set_winner_round2_1_0 = set()
    #     set_loser_round2_1_0 = set()
    #     for ind_match_round2_1_0 in range(8, 12):
    #         res_match_round2_1_0 = (all_res >> ind_match_round2_1_0) & 1
    #         match_round2_1_0 = list(round2_1_0_draw[ind_match_round2_1_0 - 8])
    #         win_team_match_round2_1_0 = match_round2_1_0[res_match_round2_1_0]
    #         lose_team_match_round2_1_0 = match_round2_1_0[1-res_match_round2_1_0]
    #         set_winner_round2_1_0.add(win_team_match_round2_1_0)
    #         set_loser_round2_1_0.add(lose_team_match_round2_1_0)
    #         #Change here for probability calcul
    #         if ( team_regions[win_team_match_round2_1_0] in ["CHN", "KR"] ) and (team_regions[lose_team_match_round2_1_0] in ["EU", "NA"]):
    #             proba = 0.0
    #         else:
    #             proba *= win_chance(win_team_match_round2_1_0, lose_team_match_round2_1_0)

    # for round2_0_1_draw in equipart(set_loser_round1, 2):
    #     #for all_res_round2_0_1 in range(int(math.pow(2, 4))):
    #     set_winner_round2_0_1 = set()
    #     set_loser_round2_0_1 = set()
    #     for ind_match_round2_0_1 in range(12, 16):
    #         res_match_round2_0_1 = (all_res >> ind_match_round2_0_1) & 1
    #         match_round2_0_1 = list(round2_0_1_draw[ind_match_round2_0_1 - 12])
    #         win_team_match_round2_0_1 = match_round2_0_1[res_match_round2_0_1]
    #         lose_team_match_round2_0_1 = match_round2_0_1[1-res_match_round2_0_1]
    #         set_winner_round2_0_1.add(win_team_match_round2_0_1)
    #         set_loser_round2_0_1.add(lose_team_match_round2_0_1)
    #         #Change here for probability calcul
    #         if ( team_regions[win_team_match_round2_0_1] in ["CHN", "KR"] ) and (team_regions[lose_team_match_round2_0_1] in ["EU", "NA"]):
    #             proba = 0.0
    #         else:
    #             proba *= win_chance(win_team_match_round2_0_1, lose_team_match_round2_0_1)

    #for round3_2_0_draw in equipart(set(round3_2_0), 2):
        #for all_res_round3_2_0 in range(int(math.pow(2, 2))):
    set_winner_round3_2_0 = set()
    set_loser_round3_2_0 = set()
    for ind_match_round3_2_0 in range(2):
        res_match_round3_2_0 = (all_res >> ind_match_round3_2_0) & 1
        match_round3_2_0 = list(round3_2_0[ind_match_round3_2_0])

        win_team_match_round3_2_0 = round3_2_0[ind_match_round3_2_0][res_match_round3_2_0] 
        lose_team_match_round3_2_0 = round3_2_0[ind_match_round3_2_0][1-res_match_round3_2_0]

        # win_team_match_round3_2_0 = match_round3_2_0[res_match_round3_2_0]
        # lose_team_match_round3_2_0 = match_round3_2_0[1-res_match_round3_2_0]

        set_winner_round3_2_0.add(win_team_match_round3_2_0)
        set_loser_round3_2_0.add(lose_team_match_round3_2_0)
        #Change here for probability calcul
        if ( team_regions[win_team_match_round3_2_0] in ["CHN", "KR"] ) and (team_regions[lose_team_match_round3_2_0] in ["EU", "NA"]):
            proba = 0.0
        else:
            proba *= win_chance(win_team_match_round3_2_0, lose_team_match_round3_2_0)

    #for round3_1_1_draw in equipart(set_loser_round2_1_0.union(set_winner_round2_0_1), 2):
    for all_res_round3_1_1 in range(int(math.pow(2, 4))):
        set_winner_round3_1_1 = set()
        set_loser_round3_1_1 = set()
        for ind_match_round3_1_1 in range(2, 6):
            res_match_round3_1_1 = (all_res >> ind_match_round3_1_1) & 1
            match_round3_1_1 = list(round3_1_1[ind_match_round3_1_1 - 2])
            win_team_match_round3_1_1 = match_round3_1_1[res_match_round3_1_1]
            lose_team_match_round3_1_1 = match_round3_1_1[1-res_match_round3_1_1]
            set_winner_round3_1_1.add(win_team_match_round3_1_1)
            set_loser_round3_1_1.add(lose_team_match_round3_1_1)
            #Change here for probability calcul
            if ( team_regions[win_team_match_round3_1_1] in ["CHN", "KR"] ) and (team_regions[lose_team_match_round3_1_1] in ["EU", "NA"]):
                proba = 0.0
            else:
                proba *= win_chance(win_team_match_round3_1_1, lose_team_match_round3_1_1)


        # #for round3_0_2_draw in equipart(set(set_loser_round2_0_1), 2):
        # for all_res_round3_0_2 in range(int(math.pow(2, 2))):
        #     set_winner_round3_0_2 = set()
        #     set_loser_round3_0_2 = set()
        #     for ind_match_round3_0_2 in range(6, 8):
        #         res_match_round3_0_2 = (all_res >> ind_match_round3_0_2) & 1
        #         match_round3_0_2 = list(round3_0_2[ind_match_round3_0_2 - 6])
        #         win_team_match_round3_0_2 = match_round3_0_2[res_match_round3_0_2]
        #         lose_team_match_round3_0_2 = match_round3_0_2[1-res_match_round3_0_2]
        #         set_winner_round3_0_2.add(win_team_match_round3_0_2)
        #         set_loser_round3_0_2.add(lose_team_match_round3_0_2)
        #         #Change here for probability calcul
        #         if ( team_regions[win_team_match_round3_0_2] in ["CHN", "KR"] ) and (team_regions[lose_team_match_round3_0_2] in ["EU", "NA"]):
        #             proba = 0.0
        #         else:
        #             proba *= win_chance(win_team_match_round3_0_2, lose_team_match_round3_0_2)    


            # for round4_2_1_draw in equipart(set_loser_round3_2_0.union(set_winner_round3_1_1), 2):
            #     #for all_res_round4_2_1 in range(int(math.pow(2, 3))):
            #     set_winner_round4_2_1 = set()
            #     set_loser_round4_2_1 = set()
            #     for ind_match_round4_2_1 in range(8, 11):
            #         res_match_round4_2_1 = (all_res >> ind_match_round4_2_1) & 1
            #         match_round4_2_1 = list(round4_2_1_draw[ind_match_round4_2_1 - 8])
            #         win_team_match_round4_2_1 = match_round4_2_1[res_match_round4_2_1]
            #         lose_team_match_round4_2_1 = match_round4_2_1[1-res_match_round4_2_1]
            #         set_winner_round4_2_1.add(win_team_match_round4_2_1)
            #         set_loser_round4_2_1.add(lose_team_match_round4_2_1)
            #         #Change here for probability calcul
            #         if ( team_regions[win_team_match_round4_2_1] in ["CHN", "KR"] ) and (team_regions[lose_team_match_round4_2_1] in ["EU", "NA"]):
            #             proba = 0.0
            #         else:
            #             proba *= win_chance(win_team_match_round4_2_1, lose_team_match_round4_2_1)


                # for round4_1_2_draw in equipart(set_loser_round3_1_1.union(set_winner_round3_0_2), 2):
                #     #for all_res_round4_1_2 in range(int(math.pow(2, 3))):
                #     set_winner_round4_1_2 = set()
                #     set_loser_round4_1_2 = set()
                #     for ind_match_round4_1_2 in range(11, 14):
                #         res_match_round4_1_2 = (all_res >> ind_match_round4_1_2) & 1
                #         match_round4_1_2 = list(round4_1_2_draw[ind_match_round4_1_2 - 11])
                #         win_team_match_round4_1_2 = match_round4_1_2[res_match_round4_1_2]
                #         lose_team_match_round4_1_2 = match_round4_1_2[1-res_match_round4_1_2]
                #         set_winner_round4_1_2.add(win_team_match_round4_1_2)
                #         set_loser_round4_1_2.add(lose_team_match_round4_1_2)
                #         #Change here for probability calcul
                #         if ( team_regions[win_team_match_round4_1_2] in ["CHN", "KR"] ) and (team_regions[lose_team_match_round4_1_2] in ["EU", "NA"]):
                #             proba = 0.0
                #         else:
                #             proba *= win_chance(win_team_match_round4_1_2, lose_team_match_round4_1_2)


                    # for round5_2_2_draw in equipart(set_loser_round4_2_1.union(set_winner_round4_1_2), 2):
                    #     #for all_res_round5_2_2 in range(int(math.pow(2, 3))):
                    #     set_winner_round5_2_2 = set()
                    #     set_loser_round5_2_2 = set()
                    #     for ind_match_round5_2_2 in range(14, 17):
                    #         res_match_round5_2_2 = (all_res >> ind_match_round5_2_2) & 1
                    #         match_round5_2_2 = list(round5_2_2_draw[ind_match_round5_2_2 - 14])
                    #         win_team_match_round5_2_2 = match_round5_2_2[res_match_round5_2_2]
                    #         lose_team_match_round5_2_2 = match_round5_2_2[1-res_match_round5_2_2]
                    #         set_winner_round5_2_2.add(win_team_match_round5_2_2)
                    #         set_loser_round5_2_2.add(lose_team_match_round5_2_2)
                    #         #Change here for probability calcul
                    #         if ( team_regions[win_team_match_round5_2_2] in ["CHN", "KR"] ) and (team_regions[lose_team_match_round5_2_2] in ["EU", "NA"]):
                    #             proba = 0.0
                    #         else:
                    #             proba *= win_chance(win_team_match_round5_2_2, lose_team_match_round5_2_2)


                        # set_qualified_teams = frozenset(
                        #     (set_winner_round5_2_2.union(set_winner_round4_2_1)).union(set_winner_round3_2_0)
                        # )

        set_qualified_teams = frozenset(set_winner_round3_2_0.union(set_winner_round3_1_1))

        if set_qualified_teams in dict_all_swiss_stage:
            dict_all_swiss_stage[set_qualified_teams] = dict_all_swiss_stage[set_qualified_teams] + proba
        else:
            dict_all_swiss_stage[set_qualified_teams] = proba
        if proba != 0.0:
            pass

                        #print(set_qualified_teams)

l = 0           