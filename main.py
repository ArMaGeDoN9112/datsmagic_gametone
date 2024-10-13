import time
import pprint
import requests

import RewindClient
import gui
from classes.anomaly import Anomaly
from classes.carp import Carp
from classes.bounty import Bounty
from classes.enemy import Enemy

from gui import draw_obj, make_msg, draw_pop, draw_line

show_all = []

headers = {"X-Auth-Token": "_"}
URL = "https://games-test.datsteam.dev/"
ROUNDS_URL = "https://games.datsteam.dev/rounds/magcarp"
GAME_URL = "https://games.datsteam.dev/play/magcarp/player/move"


resp1 = requests.get(ROUNDS_URL, headers=headers).json()
pprint.pprint(resp1)
resp = requests.post(GAME_URL, headers=headers).json()
mapSize = resp['mapSize']
maxSpeed = resp["maxSpeed"]
maxAccel = resp["maxAccel"]


def create_carpets(response):
    carps = []
    for i in response["transports"]:
        carpet = Carp(x=i["x"], y=i["y"], id=i["id"], velocity=i["velocity"], selfAcceleration=i["selfAcceleration"],
                  anomalyAcceleration=i["anomalyAcceleration"], health=i["health"], status=i["status"],
                  deathCount=i["deathCount"], shieldLeftMs=i["shieldLeftMs"], shieldCooldownMs=i["shieldCooldownMs"],
                  attackCooldownMs=i["attackCooldownMs"], mapSize=mapSize, maxSpeed=maxSpeed, maxAccel=maxAccel, wantedList=response["wantedList"])
        carps.append(carpet)
        show_all.append(carpet)

    return carps

def create_anomalies(response):
    anomalies = []
    for i in response["anomalies"]:
        anomaly = Anomaly(x=i["x"], y=i["y"], radius=i["radius"], effectiveRadius=i["effectiveRadius"],
                              strength=i["strength"])
        anomalies.append(anomaly)
        show_all.append(anomaly)

    return anomalies


carps = create_carpets(resp)
anomalies = create_anomalies(resp)




while 1:
    bounties_data = resp["bounties"]
    enemies_data = resp["enemies"]
    carpets = resp["transports"]
    anomalies = resp["anomalies"]
    anoms = []
    carps = []
    enemies = []
    bounties = []

    request = {}
    request['transports'] = []

    for i in carpets:
        carpet = Carp(x=i["x"], y=i["y"], id=i["id"], velocity=i["velocity"], selfAcceleration=i["selfAcceleration"],
                  anomalyAcceleration=i["anomalyAcceleration"], health=i["health"], status=i["status"],
                  deathCount=i["deathCount"], shieldLeftMs=i["shieldLeftMs"], shieldCooldownMs=i["shieldCooldownMs"],
                  attackCooldownMs=i["attackCooldownMs"], mapSize=mapSize, maxSpeed=maxSpeed, maxAccel=maxAccel, wantedList=resp["wantedList"])
        carps.append(carpet)

        draw_obj(carpet, color=RewindClient.RewindClient.DARK_GREEN, radius=10, mapSize=mapSize, fill=True)
        draw_pop(carpet, radius=100, mapSize=mapSize,
                 msg=f"x_v: {carpet.velocity['x']} y_v:{carpet.velocity['y']};\n"
                     f"x_a: {carpet.selfAcceleration['x']} y_a: {carpet.selfAcceleration['y']};\n"
                     f"hp: {carpet.health} cd: {carpet.attackCooldownMs}")
        draw_line(carpet, mapSize)

        make_msg(carpet)

    for i in anomalies:
        anomaly = Anomaly(x=i["x"], y=i["y"], radius=i["radius"], effectiveRadius=i["effectiveRadius"],
                              strength=i["strength"])
        anoms.append(anomaly)
        draw_obj(anomaly, color=RewindClient.RewindClient.DARK_BLUE, radius=anomaly.effectiveRadius, mapSize=mapSize,)
        draw_obj(anomaly, color=RewindClient.RewindClient.BLUE, radius=anomaly.radius, mapSize=mapSize, fill=True)


    for i in bounties_data:
        bo = Bounty(x=i["x"], y=i["y"], points=i["points"], radius=i["radius"])
        bounties.append(bo)

        draw_obj(bo, RewindClient.RewindClient.GREEN, radius=bo.radius, mapSize=mapSize,fill=True)

    for i in enemies_data:
        enemy = Enemy(x=i["x"], y=i["y"], velocity=i["velocity"], health=i["health"], status=i["status"],
                      shieldLeftMs=i["shieldLeftMs"], killBounty=i["killBounty"])
        enemies.append(enemy)

        draw_obj(enemy, RewindClient.RewindClient.RED, radius=50, mapSize=mapSize, fill=True)
        draw_pop(enemy, radius=100, mapSize=mapSize,
                 msg=f"x_v: {enemy.velocity['x']} y_v:{enemy.velocity['y']};\n"
                     f"hp: {enemy.health}")

    for carpet in carps:
        carpet.set_enemies(enemies)
        bo = carpet.set_bounties(bounties)
        carpet.set_anomalies(anoms)
        # print(len(carpet.enemies), len(carpet.bounties), len(carpet.anomalies))
        carpet.attack_enemy()
        # carpet.save_vector()
        carpet.attack_bounty()

        if bo is not None:
            gui.a.line(carpet.x / mapSize['x'], carpet.y / mapSize['y'],
                       bo.x / mapSize['x'], bo.y / mapSize['y'], RewindClient.RewindClient.DARK_BLUE)

        carpet.check_hp()
        request["transports"].append(carpet.req)


    gui.a.message("Gold: " + str(resp['points']))
    resp = requests.post(GAME_URL, headers=headers, json=request).json()


    gui.a.end_frame()
    print("_______")
    time.sleep(0.3)


# for i in global_data:
#     carps.append(i["transports"])
#     anomalies.append(i["anomalies"])



# for i in carps[0]:
#     c.append(
#         carp.Carp(x=i["x"], y=i["y"], id=i["id"], velocity=i["velocity"], selfAcceleration=i["selfAcceleration"],
#                   anomalyAcceleration=i["anomalyAcceleration"], health=i["health"], status=i["status"],
#                   deathCount=i["deathCount"], shieldLeftMs=i["shieldLeftMs"], shieldCooldownMs=i["shieldCooldownMs"],
#                   attackCooldownMs=i["attackCooldownMs"]))
# for i in anomalies[0]:
#     a.append(anomaly.Anomaly(x=i["x"], y=i["y"], radius=i["radius"], effectiveRadius=i["effectiveRadius"],
#                              strength=i["strength"]))

# all_objs = []
# for response in global_data:
#     carps = response["transports"]
#     anomalies = response["anomalies"]
#     bounties = response["bounties"]
#     enemies = response["enemies"]
#
#     for i in carps:
#         for j in i:
#             carp = Carp(x=i["x"] / 9, y=i["y"] / 9, id=i["id"], velocity=i["velocity"], selfAcceleration=i["selfAcceleration"],
#                           anomalyAcceleration=i["anomalyAcceleration"], health=i["health"], status=i["status"],
#                           deathCount=i["deathCount"], shieldLeftMs=i["shieldLeftMs"], shieldCooldownMs=i["shieldCooldownMs"],
#                           attackCooldownMs=i["attackCooldownMs"])
#
#             # draw_obj(carp, color=RewindClient.RewindClient.DARK_BLUE, radius=100 / 9, fill=True)
#             draw_obj_pop(carp, color=RewindClient.RewindClient.DARK_BLUE, radius=100, message=carp.velocity)
#
#     for i in anomalies:
#         an = Anomaly(x=i["x"] / 9, y=i["y"] / 9, radius=i["radius"] / 9, effectiveRadius=i["effectiveRadius"] / 9, strength=i["strength"] / 9)
#
#         draw_obj(an, color=RewindClient.RewindClient.DARK_BLUE, radius=an.effectiveRadius)
#         draw_obj(an, color=RewindClient.RewindClient.BLUE, radius=an.radius, fill=True)
#
#     for i in bounties:
#         bo = Bounty(x=i["x"] / 9, y=i["y"] / 9, points=0, radius=i["radius"]/ 9)
#
#         draw_obj(bo, RewindClient.RewindClient.GREEN, radius=30 / 9,fill=True)
#
#     for i in enemies:
#         bo = Enemy(x=i["x"] / 9, y=i["y"] / 9, damage=0, velocity=i["velocity"], health=i["health"], status=i["status"],
#                    shieldLeftMs=i["shieldLeftMs"], killBounty=0)
#
#         draw_obj(bo, RewindClient.RewindClient.RED, radius=50 / 9, fill=True)
#
#
#     gui.a.end_frame()
#     time.sleep(1)




# while True:
#     req = requests.post(PARTICIPIATE_URL, headers=headers).json()
#     f.write(json.dumps(req))
#     f.write("\n")
#     time.sleep(3)

# map_size = req["mapSize"]
# print("Map size: ", map_size)
#
# print("Transport")
# my_crp = req["transports"]
# for i in my_crp:
#     print(i)
#
# anomalies = req["anomalies"]
# print("Anom")
#
# last_turn = -1
#
# z_colors = {'liner': "red", 'bomber': "orange", 'chaos_knight': "yellow", 'juggernaut': "lime", 'fast': "lightblue",
#             'normal': "green"}
# spot_colors = {'wall': "black", 'default': "olive"}
#
# plt.ion()
# plt.show()
#
#
# def draw_now(obj):
#     if not obj:
#         return
#     x_list = [o[0] for o in obj]
#     y_list = [o[1] for o in obj]
#     #print(obj)
#     c = obj[0][2]
#
#     plt.scatter(x_list, y_list, color=c)
#     plt.draw()
#     plt.pause(0.000001)


# def draw(world, units):
#     plt.clf()
#     obj = [[b['x'], b['y'], 'blue' if 'isHead' not in b else 'orchid'] for b in units['base']]
#     draw_now(obj)
#     hp = 0
#     for b in units.get('base', []):
#         if b.get('isHead'):
#             hp = b['health']
#             obj = [[b['x'], b['y'], 'black']]
#     draw_now(obj)
#     if hp:
#         plt.text(*obj[0][:2], hp)
#
# for ztype in z_colors.keys(): obj = [[z['x'], z['y'], z_colors[z['type']]] for z in filter(lambda z: z['type'] ==
# ztype, units['zombies'])] if units.get('zombies') else [] draw_now(obj)
#
# for type in spot_colors.keys(): obj = [[s['x'], s['y'], spot_colors[s['type']]] for s in filter(lambda x: x[
# 'type']==type, world['zpots'])] if world['zpots'] else [] draw_now(obj)
#
#     obj = [[s['x'], s['y'], "peru"] for s in units['enemyBlocks']] if units['enemyBlocks'] else []
#     draw_now(obj)
#     obj = [[s['x'], s['y'], "saddlebrown", s['health']] for s in filter(lambda x: x['attack']>20, units['enemyBlocks'])] if units['enemyBlocks'] else []
#     draw_now(obj)
#
#     for s in obj:
#         plt.text(s[0], s[1], s[3])
#
#     yint = []
#     xint = []
#     locs, labels = plt.yticks()
#     for each in locs:
#         yint.append(int(each))
#     locs, labels = plt.xticks()
#     for each in locs:
#         xint.append(int(each))
#
#     a = set(xint+yint)
#     # plt.xticks(sorted(a))
#     # plt.yticks(sorted(a))
#     plt.pause(0.01)
#
#
# # units = {'base': [{'x': 5, 'y': 5, 'isHead': True}, {'x': 6, 'y': 5}, {'x': 5, 'y': 4}, {'x': 6, 'y': 4}],
# 'zombies': [{'x': 3, 'y': 2, 'type': 'normal'}]} # draw(None, units) # units = {'base': [{'x': 5, 'y': 5,
# 'isHead': True}, {'x': 6, 'y': 5}, {'x': 5, 'y': 4}, {'x': 6, 'y': 4}], 'zombies': [{'x': 4, 'y': 2,
# 'type': 'normal'}]} # draw(None, units)
#
#
# def can_build_on(world, units, x, y):
#     for w in world["zpots"]:
#         if abs(w['x'] - x) + abs(w['y'] - y) <= 1:
#             return False
#     for b in units['base']:
#         if b['x'] == x and b['y'] == y:
#             return False
#     for z in units.get('zombies', []):
#         if z['x'] == x and z['y'] == y:
#             return False
#
#     return True
#
#
# t1_h_cords = [[-1, 0], [-1, -1], [0, 1], [1, 1]]
# bdirs = [[-1, 0], [1, 0], [0, 1], [0, -1]]
#
# def builds(world, units):
#     bds = []
#
#     if not units.get('base', None):
#         return []
#
#     gold = units['player']['gold']
#     if not gold:
#         return None
#
#     build = []
#
#     if units['turn'] == 1:
#         base = None
#         for i in units['base']:
#             print(i)
#             if 'isHead' in i and i['isHead']:
#                 base = i
#                 break
#         for t in t1_h_cords:
#             if can_build_on(world, units, base['x'] + t[0], base['y'] + t[1]):
#                 build.append({'x': base['x'] + t[0], 'y': base['y'] + t[1]})
#
#     if units['turn'] == 2:
#         base = None
#         for i in units['base']:
#             print(i)
#             if 'isHead' in i and i['isHead']:
#                 base = i
#                 break
#         build.append({'x': base['x'] - 1, 'y': base['y'] + 1})
#
#     if units['turn'] > 1:
#         shuffle(units['base'])
#         for b in units['base']:
#             if not gold:
#                 break
#             for c in [[-1, 0], [1, 0], [0, 1], [0, -1]] if bdir == -1 else [bdirs[bdir]]:
#                 x, y = b['x'] + c[0], b['y'] + c[1]
#                 if [x, y] in bds:
#                     continue
#                 if can_build_on(world, units, x, y):
#                     build.append({'x': x, 'y': y})
#                     gold -= 1
#                     bds.append([x, y])
#
#     return build or None
#
#
# move_x = move_y = None
# bdir = -1
#
# def input_moving():
#     global move_x
#     global move_y
#     global bdir
#
#     while 1:
#         cm, *vals = input("Enter command: ").split()
#         if cm == 'mb':
#             move_x, move_y = map(int, vals)
#         if cm == "bd":
#             bdir = int(vals[0])
#             if bdir != -1:
#                 print("Change build direction to", bdirs[bdir])
#
#
# def evaluate_moveBase(world, units):
#     global move_x
#
#     if move_x:
#         x, y = move_x, move_y
#         move_x = None
#         for b in units.get('base', []):
#             if b['x'] == x and b['y'] == y:
#                 print('Can move!')
#                 print("Move to:", x, y)
#                 return {'x': x, 'y': y}
#         print("Vant move to:", x, y)
#
#     return None
#
#
#     if not units.get('base', None):
#         return None
#     shuffle(units['base'])
#     for b in units['base']:
#         if b.get('isHead', False):
#             continue
#         return {'x': b['x'], 'y': b['y']}
#
#
# def evaluate_attack(world, units):
#
#     if not units.get('base', None):
#         return None
#
#     base = units['base']
#     zombies = units.get("zombies", None)
#
#     bmade_attack = []
#
#     attack = []
#     if zombies is None:
#         return None
#     # print(sorted(zombies, key=lambda z: sorting_z.index(z['type'])))
#     for z in sorted(zombies, key=lambda z: [-z['health'], sorting_z.index(z['type'])]):
#         for b in base:
#             if b['id'] in bmade_attack:
#                 continue
#
#             if b['range'] >= sqrt(abs(b['x'] - z['x'])**2 + abs(b['y'] - z['y'])**2):
#                 bmade_attack.append(b['id'])
#                 attack.append({'blockId': b['id'], 'target': {'x': z['x'], 'y': z['y']}})
#                 z['health'] -= b['attack']
#
#             if z['health'] <= 0:
#                 break
#
#     for eb in sorted(units.get('enemyBlocks', []) or [], key=lambda ba: [int(ba.get('attack', 0)), -ba.get('health', 100)]):
#         for b in base:
#             if b['id'] in bmade_attack:
#                 continue
#
#             if b['range'] >= sqrt(abs(b['x'] - eb['x'])**2 + abs(b['y'] - eb['y'])**2):
#                 bmade_attack.append(b['id'])
#                 attack.append({'blockId': b['id'], 'target': {'x': eb['x'], 'y': eb['y']}})
#                 eb['health'] -= b['attack']
#
#             if eb['health'] < 0:
#                 break
#
#     return attack
#
#
# sorting_z = ['liner', 'bomber', 'chaos_knight', 'juggernaut', 'fast', 'normal'][::-1]
#
#
# def evaluate_turn(world, units):
#     global last_turn
#     global turnMade
#
#     turn = units["turn"]
#
#     if turn == last_turn:
#         return {}
#
#     last_turn = turn
#
#     resp = {}
#     resp['build'] = builds(world, units)
#     resp['attack'] = evaluate_attack(world, units)
#     resp['moveBase'] = evaluate_moveBase(world, units)
#
#     # print(world)
#     # print(units)
#     # print(resp)
#
#     return resp
#
# started = True
# print("LETS BEGIN!")
# thr = Thread(target=input_moving, daemon=True)
# thr.start()
#
# while 1:
#     world = requests.get(WORLD_URL, headers=headers)
#
#     if world.status_code != 200:
#         if started:
#             print(world.json())
#         continue
#     started = True
#     units = requests.get(UNITS_URL, headers=headers)
#
#     if not units.json().get('base', True):
#         print("WE ARE DEAD")
#         break
#
#     resp = evaluate_turn(world.json(), units.json())
#     if resp:
#         r = requests.post("https://games.datsteam.dev/play/zombidef/command", json=json.dumps(resp),
#                           headers=headers)
#
#         # print(r)
#         # print(r.json())
#         # print(resp)
#         draw(world.json(), units.json())
