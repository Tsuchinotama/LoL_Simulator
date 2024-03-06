from networkx import Graph, min_weight_matching

class team:
    def __init__(self, name, nwins=0):
        self.name = name
        self.nwins = 0
        self.sos = 0
        self.sosos = 0

class DoubleSwissTournament:
    def __init__(self, list_of_team_names=()):
        self.n_teams = len(list_of_team_names)
        self.team_list = [team(name) for name in list_of_team_names]
        self.prev_matches = {i: set() for i in range(self.n_teams)}
        self.rounds = []
        self.coeffs = {'nwins':100, 'sos':10, 'sosos':1}

    def add_team(self, name, nwins=0):
        self.team_list.append(team(name,nwins=nwins))
        self.prev_matches[self.n_teams] = set()
        self.n_teams += 1

    def recompute_sos(self):
        for p,opponents in self.prev_matches.items():
            self.team_list[p].sos = sum(self.team_list[q].nwins for q in opponents)

    def recompute_sosos(self):
        for p,opponents in self.prev_matches.items():
            self.team_list[p].sosos = sum(self.team_list[q].sos for q in opponents)

    def dist(self, p, q):
        x,y = self.team_list[p], self.team_list[q]
        return sum(coeff * (getattr(x,score) - getattr(y,score))**2
                   for score,coeff in self.coeffs.items())
    
    def gen_next_round(self):
        g = Graph()
        g.add_nodes_from(range(self.n_teams))
        g.add_weighted_edges_from(
            (p, q, self.dist(p,q))
            for p,opponents in self.prev_matches.items()
            for q in set(range(p)).difference(opponents)
        )
        m1 = min_weight_matching(g)
        g.remove_edges_from(m1)
        m2 = min_weight_matching(g)
        round = m1.union(m2)
        self.rounds.append(round)
        return round
    
    def add_results(self, results):
        for p,q, winner in results:
            self.prev_matches[p].add(q)
            self.prev_matches[q].add(p)
            self.team_list[winner].nwins += 1
        self.recompute_sos()
        self.recompute_sosos()

    def get_standings(self):
        teams = sorted(self.team_list, key=lambda p:(p.nwins,p.sos,p.sosos), reverse=True)
        ranks = list(range(1,len(teams)+1))
        for i in range(1,len(teams)):
            if ((teams[i].nwins,teams[i].sos,teams[i].sosos)
             == (teams[i-1].nwins,teams[i-1].sos,teams[i-1].sosos)):
                ranks[i] = ranks[i-1]
        return [(r,p.name,p.nwins,p.sos,p.sosos) for r,p in zip(ranks,teams)]
    
    def str_standings(self):
        l = self.get_standings()
        l = [('','name','wins','sos','sosos')] + l
        maxlen = max(len(name) for _,name,_,_,_ in l)
        return '\n'.join('{:2}. {:{width}}  {:>4} {:>4} {:>4}'.format(*x, width=maxlen) for x in l)

from random import choice

def main():
    team_names = [
        "JDG", "BLG", "LNG", "WBG", 
        "G2", "FNC", "MAD", "BDS", 
        "GENG", "T1", "KT", "DK", 
        "NRG", "C9", "TL", "GAM"
    ]
    tournament = DoubleSwissTournament(team_names)
    print('STANDINGS BEFORE ROUND 1')
    print(tournament.str_standings())
    for round_number in (1,2,3):
        print('\nROUND {}: PAIRINGS'.format(round_number))
        round = tournament.gen_next_round()
        print([(tournament.team_list[p].name,tournament.team_list[q].name)
               for p,q in round])
        print('\nROUND {}: RESULTS'.format(round_number))
        results = [(p,q,choice((p,q))) for p,q in round]
        print(['{} {}-{} {}'.format(tournament.team_list[p].name,int(p==w),int(q==w),tournament.team_list[q].name)
               for p,q,w in results])
        tournament.add_results(results)
        print('\nSTANDINGS AFTER ROUND {}'.format(round_number))
        print(tournament.str_standings())
    return tournament

if __name__ == '__main__':
    tournament = main()