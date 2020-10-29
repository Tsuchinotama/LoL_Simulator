class head_to_head :
    def __init__(self, p_wins, p_losses, p_ratio) :
        self.wins = p_wins
        self.losses = p_losses
        self.ratio = p_ratio

    def __str__(self) :
        return ("victoires : " + str(self.wins) + " , defaites : " + str(self.losses) + " , ratio : " + str(self.ratio))

team_regions = {"TES" : "CHN", "JDG" : "CHN", "SN" : "CHN", "LGD" : "CHN", "G2" : "EU", "FNC" : "EU", "RGE" : "EU", "MAD" : "EU", "DWG" : "KR", "DRX" : "KR", "GEN" : "KR", "TSM" : "NA", "FLY" : "NA", "TL" : "NA", "MCX" : "PCS", "PSG" : "PCS", "LGC" : "OCE", "SUP" : "TUR", "INZ" : "BRE", "V3" : "JPN", "UOL" : "RUS", "R7" : "LAT"}

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