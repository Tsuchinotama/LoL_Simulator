import copy
from itertools import permutations
import itertools
import xlsxwriter

all_main_teams = ["GENG", "T1", "JDG", "MAD","C9"] 

all_play_in_teams = ["BLG", "R7", "GG", "GAM", "G2", "LOUD", "PSGT", "DFM"]

play_in_group_A = ["BLG", "R7", "GG", "GAM"]
play_in_group_B = ["G2", "LOUD", "PSGT", "DFM"]
list_all_possible_play_in_qualifs = []

list_2_qualifs_from_A = [list(i) for i in itertools.combinations(play_in_group_A, 2)]
for qualifs_group_A in list_2_qualifs_from_A:
    for team_B in play_in_group_B:
        LCQ_qualifs_group_A = copy.deepcopy(qualifs_group_A)
        LCQ_qualifs_group_A.append(team_B)
        # LCQ_qualifs_group_A.append("T1")
        list_all_possible_play_in_qualifs.append(LCQ_qualifs_group_A)
del LCQ_qualifs_group_A
del team_B
del qualifs_group_A

list_2_qualifs_from_B = [list(i) for i in itertools.combinations(play_in_group_B, 2)]
for qualifs_group_B in list_2_qualifs_from_B:
    for team_A in play_in_group_A:
        LCQ_qualifs_group_B = copy.deepcopy(qualifs_group_B)
        LCQ_qualifs_group_B.append(team_A)
        # LCQ_qualifs_group_B.append("T1")
        list_all_possible_play_in_qualifs.append(LCQ_qualifs_group_B)
del LCQ_qualifs_group_B
del team_A
del qualifs_group_B

main_teams_pool = {1: ["JDG", "GENG"], 2: ["MAD", "C9"], 3: ["T1"] + all_play_in_teams}

# region_teams = {"CHN" : ["JDG", "BLG"], "EU" : ["G2", "MAD"], "KR" : ["GENG", "T1"], "NA" : ["C9", "GG"], "PCS" : ["PSGT"], "VCS" : ["GAM"], "LJL" : ["DFM"], "BRE" : ["LOUD"], "LAT" : ["R7"]}
team_regions = {"BLG" : "CHN", "JDG" : "CHN", "G2" : "EU", "MAD" : "EU", "GENG" : "KR", "T1" : "KR", "C9" : "NA", "GG" : "NA", "PSGT" : "PCS", "GAM" : "VCS", "LOUD" : "BRE", "DFM" : "JPN", "R7" : "LAT"}

main_phase_init = [[["JDG"], []], [["GENG"], []]]
#list_main_phase = [[["JDG"], []], [["GENG"], []]]

list_all_main_phase = []
dict_all_main_phase = {}

copy_main_phase = copy.deepcopy(main_phase_init)
list_places_second_pool = list(permutations(main_teams_pool[2]))

list_all_possible_play_in_qualifs = [["DFM", "PSGT", "GAM"], ["BLG", "GG", "G2"]]

for play_in_qualified_teams in list_all_possible_play_in_qualifs:
    tuple_play_in_qualified_teams = tuple(play_in_qualified_teams)
    dict_all_main_phase[tuple_play_in_qualified_teams] = []
    copy_play_in_qualified_teams = copy.deepcopy(play_in_qualified_teams)
    copy_play_in_qualified_teams.append("T1")
    set_all_possible_third_pool = list(permutations(copy_play_in_qualified_teams))
    for affect_third_pool_teams in set_all_possible_third_pool:
        for permutation_second_pool in list_places_second_pool:
            second_pool_first_team = permutation_second_pool[0]
            #copy_main_phase[0][1].append(second_pool_first_team)
            second_pool_second_team = permutation_second_pool[1]
            #copy_main_phase[1][1].append(second_pool_second_team)
            for i in range(4):
                ith_third_pool_team = affect_third_pool_teams[i]
                if (
                    ((i == 0) and (team_regions[copy_main_phase[i//2][i%2][0]] == team_regions[ith_third_pool_team])) or
                    ((i == 2) and (team_regions[copy_main_phase[i//2][i%2][0]] == team_regions[ith_third_pool_team])) or
                    ((i == 1) and (team_regions[second_pool_first_team] == team_regions[ith_third_pool_team])) or
                    ((i == 3) and (team_regions[second_pool_second_team] == team_regions[ith_third_pool_team]))
                    ):
                    break
            else:
                copy_main_phase[0][1].append(second_pool_first_team)
                copy_main_phase[1][1].append(second_pool_second_team)
                for j in range(4):
                    jth_third_pool_team = affect_third_pool_teams[j]
                    copy_main_phase[j//2][j%2].append(jth_third_pool_team)
                # if not copy_main_phase in list_all_main_phase:
                dict_all_main_phase[tuple_play_in_qualified_teams].append(copy_main_phase)
                copy_main_phase = copy.deepcopy(main_phase_init)

no_wildcard_play_in_teams = ["BLG", "G2", "GG"]

workbook = xlsxwriter.Workbook('main_phase_generator.xlsx')
worksheet = workbook.add_worksheet()

content_titles = ["Qualifications from play-ins", "Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"]
col = 0
for content in content_titles:
    worksheet.write(0, col, content)
    col = col + 1

row = 2

for qualifs in list_all_possible_play_in_qualifs:
    tuple_qualifs = tuple(qualifs)
    list_all_possible_tirages = dict_all_main_phase[tuple_qualifs]
    nb_tirage_possible = len(list_all_possible_tirages)
    qualifs_teams_to_write = tuple_qualifs[0] + "/" + tuple_qualifs[1] + "/" + tuple_qualifs[2]

    # worksheet.write(row + nb_tirage_possible//2, 0, qualifs_teams_to_write)
    for i in range(nb_tirage_possible):
        Q1_to_write = list_all_possible_tirages[i][0][0][0] + "/" + list_all_possible_tirages[i][0][0][1]
        worksheet.write(row + i, 1, Q1_to_write)
        Q2_to_write = list_all_possible_tirages[i][0][1][0] + "/" + list_all_possible_tirages[i][0][1][1]
        worksheet.write(row + i, 2, Q2_to_write)
        Q3_to_write = list_all_possible_tirages[i][1][0][0] + "/" + list_all_possible_tirages[i][1][0][1]
        worksheet.write(row + i, 3, Q3_to_write)
        Q4_to_write = list_all_possible_tirages[i][1][1][0] + "/" + list_all_possible_tirages[i][1][1][1]
        worksheet.write(row + i, 4, Q4_to_write)
    merge_format = workbook.add_format(
        {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter"
        }
    )
    worksheet.set_column("A:A", 30)
    worksheet.set_column("B:E", 20)
    worksheet.merge_range(first_row=row, last_row=row+nb_tirage_possible-1, first_col=0, last_col=0, data=qualifs_teams_to_write, cell_format=merge_format)
    row = row + nb_tirage_possible + 1

workbook.close()