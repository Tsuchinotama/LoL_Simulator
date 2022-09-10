import copy
from itertools import permutations
import collections
import itertools

all_main_teams = ["JDG", "TES", "EDG", "GENG", "T1", "DWG", "G2", "RGE", "C9", "100T", "CTO", "GAM"] 

all_play_in_teams = ["RNG", "DRX", "FNC", "BYG", "MAD", "EG", "SAI", "DFM", "ISU", "LOD", "CHF", "IST"]

main_teams_pool = {1: ["JDG", "GENG", "G2", "C9"], 2: ["TES", "T1", "RGE", "CTO"], 3: ["EDG", "DWG", "100T", "GAM"]}

region_teams = {"CHN" : ["TES", "JDG", "EDG", "RNG"], "EU" : ["G2", "RGE", "FNC", "MAD"], "KR" : ["GENG", "T1", "DWG", "DRX"], "NA" : ["C9", "100T", "EG"], "PCS" : ["CTO", "BYG"], "VCS": ["GAM", "SAI"], "OCE" : ["CHF"], "TUR" : ["IST"], "BRE" : ["LOD"], "JPN" : ["DFM"], "LAT" : ["ISU"]}
team_regions = {"TES" : "CHN", "JDG" : "CHN", "EDG" : "CHN", "RNG" : "CHN", "G2" : "EU", "FNC" : "EU", "RGE" : "EU", "MAD" : "EU", "DWG" : "KR", "DRX" : "KR", "GENG" : "KR", "T1" : "KR", "C9" : "NA", "100T" : "NA", "EG" : "NA", "CTO" : "PCS", "BYG" : "PCS", "GAM" : "VCS", "SAI" : "VCS", "CHF" : "OCE", "IST" : "TUR", "LOD" : "BRE", "DFM" : "JPN", "ISU" : "LAT"}

list_all_groups_main = []

occurence_all_groups_main = [[] for i in range(4)]

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

# print(list(set_all_groups))
# for all_groups in set_all_groups:            
#     print(all_groups)
#     print(list(all_groups))
print(len(set_all_groups))
list_set_all_groups = list(set_all_groups)

no_wildcard_play_in_teams = ["RNG", "DRX", "FNC", "BYG", "MAD", "EG", "SAI"]

def check_valid_affect(qualif_play_in, list_main_groups):
    if not ("FNC" in qualif_play_in) or not ("MAD" in qualif_play_in):
        for order_qualif in itertools.permutations(qualif_play_in):
            for i in range(4):
                to_affect_team = order_qualif[i]
                current_group= list_main_groups[i]
                for qualified in current_group:
                    if team_regions[qualified] == team_regions[to_affect_team]:
                        break
                else:
                    continue
                break
            else:
                return (True, None)
        else:
            return (False, qualif_play_in)

    else:
        for order_qualif in itertools.permutations(qualif_play_in):
            for i in range(4):
                to_affect_team = order_qualif[i]
                current_group= list_main_groups[i]
                if to_affect_team == "MAD":
                    continue
                for qualified in current_group:
                    if team_regions[qualified] == team_regions[to_affect_team]:
                        break
                else:
                    continue
                break
            else:
                return (True, None)
        else:
            return (False, qualif_play_in)


# copy_set_all_groups = list(set_all_groups)
copy_set_all_groups = set_all_groups.copy()
set_groups_with_compatibility = set((tirage, True) for tirage in list_set_all_groups)
print(set_groups_with_compatibility)
list_set_groups_with_compatibility = list(set_groups_with_compatibility)
for i in range(len(set_all_groups)):
    main_groups = list_set_all_groups[i]
# for main_groups in set_all_groups:
    for qualif_from_play_in in itertools.combinations(no_wildcard_play_in_teams, 4):
        if not check_valid_affect(qualif_from_play_in, list(main_groups))[0]:
            copy_set_all_groups.remove(main_groups)
            list_set_groups_with_compatibility[i] = (main_groups, False)
            break

# print(set_all_groups)
print(len(copy_set_all_groups))

print(set_all_groups.difference(copy_set_all_groups))
print()
print(list_set_groups_with_compatibility)
    

