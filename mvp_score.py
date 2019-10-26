import heroprotocol, sys, os, os.path, pprint
from heroprotocol.mpyq import mpyq
sys.path.append(os.path.join(os.getcwd(), "heroprotocol"))

from heroprotocol import protocol29406

archive = mpyq.MPQArchive(sys.argv[-1])

contents = archive.header['user_data_header']['content']
header = protocol29406.decode_replay_header(contents)
baseBuild = header['m_version']['m_baseBuild']
try:
    protocol = __import__('protocol%s' % (baseBuild,))
except:
    print >> sys.stderr, 'Unsupported base build: %d' % baseBuild
    sys.exit(1)

tracker_events = protocol.decode_replay_tracker_events(archive.read_file('replay.tracker.events'))
details = protocol.decode_replay_details(archive.read_file('replay.details'))

players = []
for player in details['m_playerList']:
    players.append({
        "name": player["m_name"],
        "hero": player["m_hero"],
        "winner": player["m_result"] == 1,
        "team": player["m_teamId"],
        "score": {}
    })

for event in tracker_events:
    if event['_eventid'] == 11:
        for stat in event['m_instanceList']:
            for index in range(len(players)):
                players[index]['score'][stat['m_name']] = stat['m_values'][index][0]['m_value']

# libGame_gf_GetMVPAwardAmount
# mods\heroesdata.stormmod\base.stormdata\TriggerLibs\GalaxyLib.galaxy
# line 2051
def get_mvp_assist_award_amount(character):
    if character == "D.Va" or character == "The Lost Vikings" or character == "Abathur": return 0.75
    return 1.0

# libGame_gf_GetMVPAwardAmount
# mods\heroesdata.stormmod\base.stormdata\TriggerLibs\GalaxyLib.galaxy
# line 2068
def get_mvp_time_spend_dead_award_amount(character):
    if character == 'Murky' or character == 'Gall': return -1.0
    if character == 'Cho': return -0.85
    return -0.5

#             hero,      siege,     tank,      heal,      experience
max_amount = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
MAX_HERO = 0
MAX_SIEGE = 1
MAX_TANK = 2
MAX_HEAL = 3
MAX_EXP = 4
#         name, hero
max_width = [0, 0]

# first pass
for player in players:
    max_amount[MAX_HERO][player['team']] = float(max([max_amount[MAX_HERO][player['team']], player['score']['HeroDamage']]))
    max_amount[MAX_SIEGE][player['team']] = float(max([max_amount[MAX_SIEGE][player['team']], player['score']['SiegeDamage']]))
    max_amount[MAX_TANK][player['team']] = float(max([max_amount[MAX_TANK][player['team']], player['score']['DamageSoaked']]))
    max_amount[MAX_HEAL][player['team']] = float(max([max_amount[MAX_HEAL][player['team']], player['score']['Healing']]))
    max_amount[MAX_EXP][player['team']] = float(max([max_amount[MAX_EXP][player['team']], player['score']['ExperienceContribution']]))
    max_width[0] = max([max_width[0], len(player['name'])])
    max_width[1] = max([max_width[1], len(player['hero'])])

# second pass
for amount in max_amount:
    amount[2] = max(amount)

# third pass
for player in players:
    mvp_score = 0
    score = player['score']
    if player['winner'] == 1: mvp_score += 2
    mvp_score += score['SoloKill'] * 1.0
    mvp_score += score['Assists'] * get_mvp_assist_award_amount(player['hero'])
    mvp_score_ok = mvp_score
    penalty = float(score['TimeSpentDead']) / header['m_elapsedGameLoops'] * 100 * get_mvp_time_spend_dead_award_amount(player['hero'])
    mvp_score += penalty
    mvp_score_base = mvp_score
    if score['HeroDamage'] >= max_amount[MAX_HERO][player['team']]: mvp_score += 1
    if score['SiegeDamage'] >= max_amount[MAX_SIEGE][player['team']]: mvp_score += 1
    if player['winner'] == 1 and score['PlaysWarrior'] == 1 and score['DamageSoaked'] >= max_amount[MAX_TANK][player['team']]: mvp_score += 0.5 # might be DamageTaken
    if score['PlaysSupport'] == 1 and score['Healing'] >= max_amount[MAX_HEAL][player['team']]: mvp_score += 1
    if score['ExperienceContribution'] >= max_amount[MAX_EXP][player['team']]: mvp_score += 1
    throughput = 0.0
    throughput += 2.0 * (float(score['HeroDamage']) /  max_amount[MAX_HERO][2])
    throughput += 2.0 * (float(score['SiegeDamage']) /  max_amount[MAX_SIEGE][2])
    if score['PlaysWarrior'] == 1: throughput += 2.0 * (float(score['DamageSoaked']) /  max_amount[MAX_TANK][2]) # might be DamageTaken
    if score['PlaysSupport'] == 1: throughput += 2.0 * (float(score['Healing']) /  max_amount[MAX_HEAL][2])
    throughput += 2.0 * (float(score['ExperienceContribution']) /  max_amount[MAX_EXP][2])
    player['mvp'] = [mvp_score, throughput, penalty, mvp_score_ok, mvp_score - mvp_score_base]

top = True

for player in sorted(players, key = lambda x: int(x['mvp'][0] + x['mvp'][1]), reverse = True):
    team_name = 'Blue'
    if player['team'] == 1: team_name = 'Red '
    mvp_score = player['mvp'][0]
    throughput = player['mvp'][1]
    penalty = player['mvp'][2]
    mvp_score_ok = player['mvp'][3]
    mvp_score_base = player['mvp'][4]
    mvp = ''
    if top: 
        mvp = ' - MVP'
        top = False
    print('Team %s - %s - %s - %.2f - BTPKSF %.2f / %.2f / %.2f / %02d / %01d / %.2fs%s' % (team_name, player['name'].rjust(max_width[0], ' '), player['hero'].rjust(max_width[1], ' '), mvp_score + throughput, mvp_score, throughput, penalty, mvp_score_ok, mvp_score_base, float(player['score']['OnFireTimeOnFire']) / 4, mvp))
