from itertools import permutations
import collections

all_main_teams = ["JDG", "TES", "EDG", "GENG", "T1", "DWG", "G2", "RGE", "C9", "100T", "CTO", "GAM"] 

all_play_in_teams = ["RNG", "DRX", "FNC", "BYG", "MAD", "EG", "SAI", "DFM", "ISU", "LOD", "CHF", "IST"]

main_teams_pool = {1: ["JDG", "GENG", "G2", "C9"], 2: ["TES", "T1", "RGE", "CTO"], 3: ["EDG", "DWG", "100T", "GAM"]}

region_teams = {"CHN" : ["TES", "JDG", "EDG", "RNG"], "EU" : ["G2", "RGE", "FNC", "MAD"], "KR" : ["GENG", "T1", "DWG", "DRX"], "NA" : ["C9", "100T", "EG"], "PCS" : ["CTO", "BYG"], "VCS": ["GAM", "SAI"], "OCE" : ["CHF"], "TUR" : ["IST"], "BRE" : ["LOD"], "JPN" : ["DFM"], "LAT" : ["ISU"]}
team_regions = {"TES" : "CHN", "JDG" : "CHN", "EDG" : "CHN", "RNG" : "CHN", "G2" : "EU", "FNC" : "EU", "RGE" : "EU", "MAD" : "EU", "DWG" : "KR", "DRX" : "KR", "GENG" : "KR", "T1" : "KR", "C9" : "NA", "100T" : "NA", "EG" : "NA", "CTO" : "PCS", "BYG" : "PCS", "GAM" : "VCS", "SAI" : "VCS", "CHF" : "OCE", "IST" : "TUR", "LOD" : "BRE", "DFM" : "JPN", "ISU" : "LAT"}

list_all_groups_main = []

occurence_all_groups_main = [[] for i in range(4)]

print({frozenset(["a", "b"]), frozenset(["c", "d"])} == {frozenset(["b", "a"]), frozenset(["d", "c"])})
print({frozenset(["a", "b"]), frozenset(["c", "d"])} in [{frozenset(["b", "a"]), frozenset(["d", "c"])}])

set_all_groups = set()
first_pool_teams = ["JDG", "GENG", "G2", "C9"]
init_first_pool_teams = [["JDG"], ["GENG"], ["G2"], ["C9"]]
list_places_second_pool = list(permutations(main_teams_pool[2]))
list_places_third_pool = list(permutations(main_teams_pool[3]))

# init_first_pool_teams[0].append("T1")

for place_second_pool in list_places_second_pool:
    for i in range(4):
        i2_team = place_second_pool[i]
        i1_team = first_pool_teams[i]
        if (team_regions[i2_team] == team_regions[i1_team]):
            break
    else:
        for place_third_pool in list_places_third_pool:
            for j in range(4):
                if (team_regions[place_third_pool[j]] == team_regions[first_pool_teams[j]]) or (team_regions[place_second_pool[j]] == team_regions[place_third_pool[j]]):
                    break
            else:
                new_init_first_pool_teams = [["JDG"], ["GENG"], ["G2"], ["C9"]]
                for k in range(4):
                    new_init_first_pool_teams[k].append(place_second_pool[k])
                    new_init_first_pool_teams[k].append(place_third_pool[k])

                one_conf_groups = frozenset(tuple(group) for group in new_init_first_pool_teams)
                set_all_groups.add(one_conf_groups)
            
print(set_all_groups)
print(len(set_all_groups))

