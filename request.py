import config
import requests as req

class api:
    class count:
        def __init__(self):
            url = f"https://api.{config.DOMAIN}/get_player_count"
            self.json = req.get(url).json()
            self.online = self.json['counts']['online']
            self.total = self.json['counts']['total']

    class pinfo:
        def __init__(self, who):
            try:
                arg = int(who)
                qe = "id"
            except ValueError:
                arg = str(who)
                qe = "name"
            url = f"https://api.{config.DOMAIN}/get_player_info?scope=info&{qe}={arg}"
            self.json = req.get(url).json()
            self.id = self.json['player']['info']['id']
            self.name = self.json['player']['info']['name']
            self.country = self.json['player']['info']['country']
            try:
                self.tag = '[' + str(self.json['player']['info']['clan']['tag']) + ']'
            except:
                self.tag = ''
    
    class pstats:
        def __init__(self, who):
            try:
                arg = int(who)
                qe = "id"
            except ValueError:
                arg = str(who)
                qe = "name"
            url = f"https://api.{config.DOMAIN}/get_player_info?scope=stats&{qe}={arg}"
            self.json = req.get(url).json()
            self.vn_std_json = self.json['player']['stats']["0"]
            self.vn_taiko_json = self.json['player']['stats']["1"]
            self.vn_catch_json = self.json['player']['stats']["2"]
            self.vn_mania_json = self.json['player']['stats']["3"]
            self.rx_std_json = self.json['player']['stats']["4"]
            self.rx_taiko_json = self.json['player']['stats']["5"]
            self.rx_catch_json = self.json['player']['stats']["6"]
            self.ap_std_json = self.json['player']['stats']["8"]
            self.full_pp = self.vn_std_json['pp'] + self.vn_taiko_json['pp'] + self.vn_catch_json['pp'] + self.vn_mania_json['pp'] + self.rx_std_json['pp'] + self.rx_taiko_json['pp'] + self.rx_catch_json['pp'] + self.ap_std_json['pp']
    
    class pscores:
        def __init__(self, who, mode, limit, scope):
            try:
                arg = int(who)
                qe = "id"
            except ValueError:
                arg = str(who)
                qe = "name"
            if mode == 0:
                self.gamemode = "vn!std"
            elif mode == 1:
                self.gamemode = "vn!taiko"
            elif mode == 2:
                self.gamemode = "vn!catch"
            elif mode == 3:
                self.gamemode = "vn!mania"
            elif mode == 4:
                self.gamemode = "rx!std"
            elif mode == 5:
                self.gamemode = "rx!taiko"
            elif mode == 6:
                self.gamemode = "rx!catch"
            elif mode == 8:
                self.gamemode = "ap!std"
            
            url = f"https://api.{config.DOMAIN}/get_player_scores?{qe}={arg}&scope={scope}&mode={mode}&limit={limit}"
            self.json = req.get(url).json()
            self.scores_list = {}
            lim = 0
            title_limit = 26
            artist_limit = 14
            self.player_id = self.json['player']['id']
            self.player_name = self.json['player']['name']
            while lim <= (limit-1):
                score_grade = self.json['scores'][lim]['grade']
                score_bid = self.json['scores'][lim]['beatmap']['id']
                score_title = self.json['scores'][lim]['beatmap']['title']
                if len(score_title) > title_limit:
                    score_title = score_title[0:title_limit] + '...'
                else:
                    score_title = score_title
                score_artist = self.json['scores'][lim]['beatmap']['artist']
                if len(score_artist) > artist_limit:
                    score_artist = score_artist[0:artist_limit] + '...'
                else:
                    score_artist = score_artist
                score_version = self.json['scores'][lim]['beatmap']['version']
                score_diff = round(self.json['scores'][lim]['beatmap']['diff'], 1)
                score_mods = self.json['scores'][lim]['mods_readable']
                score_pp = round(self.json['scores'][lim]['pp'])
                score_acc = round(self.json['scores'][lim]['acc'], 2)
                score_combo = self.json['scores'][lim]['max_combo']
                score_playtime = self.json['scores'][lim]['play_time']
                self.scores_list[lim] = {'bid': score_bid, 'grade': score_grade, 'title': score_title, 'artist': score_artist, 'diff': score_version,'stars': score_diff, 'mods': score_mods, 'pp': score_pp, 'acc': score_acc, 'combo': score_combo, 'playtime': score_playtime}
                lim += 1
    
    class pmostplayed:
        def __init__(self, who, mode, limit):
            try:
                arg = int(who)
                qe = "id"
            except ValueError:
                arg = str(who)
                qe = "name"
            if mode == 0:
                self.gamemode = "vn!std"
            elif mode == 1:
                self.gamemode = "vn!taiko"
            elif mode == 2:
                self.gamemode = "vn!catch"
            elif mode == 3:
                self.gamemode = "vn!mania"
            elif mode == 4:
                self.gamemode = "rx!std"
            elif mode == 5:
                self.gamemode = "rx!taiko"
            elif mode == 6:
                self.gamemode = "rx!catch"
            elif mode == 8:
                self.gamemode = "ap!std"
            
            url = f"https://api.{config.DOMAIN}/get_player_most_played?{qe}={arg}&mode={mode}&limit={limit}"
            self.json = req.get(url).json()

            lim = 0
            title_limit = 26
            artist_limit = 14
            self.map_list = {}
            while lim <= (limit-1):
                map_id = self.json['maps'][lim]['id']
                map_status = self.json['maps'][lim]['status']
                map_title = self.json['maps'][lim]['title']
                if len(map_title) > title_limit:
                    map_title = map_title[0:title_limit] + '...'
                else:
                    map_title = map_title
                map_artist = self.json['maps'][lim]['artist']
                if len(map_artist) > artist_limit:
                    map_artist = map_artist[0:artist_limit] + '...'
                else:
                    map_artist = map_artist
                map_diff = self.json['maps'][lim]['version']
                map_creator = self.json['maps'][lim]['creator']
                map_plays = self.json['maps'][lim]['plays']

                self.map_list[lim] = {'bid': map_id, 'status':map_status, 'title':map_title, 'artist':map_artist, 'creator':map_creator, 'diff':map_diff, 'plays': map_plays}
                lim += 1

if __name__ == '__main__':
    '''
    print('api')
    count = api.count()
    print('count:', count.online, count.total)
    print()
    pinfo = api.pinfo(369)
    print('pinfo:', pinfo.id, pinfo.name, pinfo.country, pinfo.tag)
    print()
    pstats = api.pstats(369)
    print('pstats:', pstats.full_pp, 'pp')
    print()
    pscores = api.pscores(369, 0, 5, 'best')
    print('pscores', pscores.gamemode, pscores.player_name, '\n', pscores.scores_list)
    print()
    '''
    pmostplayed = api.pmostplayed(369, 0, 5)
    print('pmostplayed', pmostplayed.gamemode, pmostplayed.map_list)
    print()
