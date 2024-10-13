from classes import anomaly
from classes import enemy
from classes import bounty


class Carp:
    def __init__(self, x, y, id, velocity, selfAcceleration, anomalyAcceleration, health, status, deathCount,
                 shieldLeftMs, shieldCooldownMs, attackCooldownMs, mapSize, maxAccel, maxSpeed, wantedList):
        self.x = x
        self.y = y
        self.id = id
        self.velocity = velocity
        self.selfAcceleration = selfAcceleration
        self.anomalyAcceleration = anomalyAcceleration
        self.health = health
        self.status = status
        self.deathCount = deathCount
        self.shieldLeftMs = shieldLeftMs
        self.shieldCooldownMs = shieldCooldownMs
        self.attackCooldownMs = attackCooldownMs
        self.anomalies = []
        self.deadlyanomalies = []
        self.enemies = []
        self.req = {}
        self.bounties = []
        self.goToBounty = False
        self.maxSpeed = maxSpeed
        self.maxAccel = maxAccel
        self.mapSize = mapSize
        self.wantedList = wantedList



    def set_anomalies(self, newAnomalies: list[anomaly.Anomaly]):
        for anomaly_ in newAnomalies:
            if ((anomaly_.x - self.x) ** 2 + (anomaly_.y - self.y) ** 2) ** 0.5 <= anomaly_.radius:
                self.deadlyanomalies.append(anomaly_)
            elif ((anomaly_.x - self.x) ** 2 + (anomaly_.y - self.y) ** 2) ** 0.5 <= anomaly_.effectiveRadius:
                self.anomalies.append(anomaly_)

    def check_hp(self):
        if self.health <= 40 and self.shieldCooldownMs == 0:
            self.req['activeShield'] = True
        else:
            self.req['activeShield'] = False

    def set_enemies(self, newEnemies: list[enemy.Enemy]):
        for enemy_ in newEnemies:
            if ((enemy_.x - self.x) ** 2 + (enemy_.y - self.y) ** 2) ** 0.5 <= 400:
                self.enemies.append(enemy_)

        enemies_hp = {}
        for enemy_ in self.enemies:
            enemies_hp[enemy_] = enemy_.health

        self.enemies = [i[0] for i in sorted(enemies_hp.items(), key=lambda item: item[1])]

        # wantedEnemies = []
        # for enemy_ in self.wantedList:
        #     if ((enemy_.x - self.x) ** 2 + (enemy_.y - self.y) ** 2) ** 0.5 <= 400:
        #         wantedEnemies.append(enemy_)
        #
        # self.enemies = wantedEnemies + self.enemies

    def attack_enemy(self):
        for enemy_ in self.enemies:
            if self.attackCooldownMs == 0 and ((enemy_.x - self.x) ** 2 + (enemy_.y - self.y) ** 2) ** 0.5 <= 200 and enemy_.health <= 30:
                self.req["attack"] = {"x": enemy_.x, "y": enemy_.y}
                break

    def set_bounties(self, newBounties: list[bounty.Bounty]):
        for bounty_ in newBounties:
            if ((bounty_.x - self.x) ** 2 + (bounty_.y - self.y) ** 2) ** 0.5 <= 400 - bounty_.radius:
                self.bounties.append(bounty_)

    def attack_bounty(self):
        distance_bounty = {}

        # if abs(self.velocity["x"]) > self.maxAccel ** 0.5 and abs(self.velocity["y"]) > self.maxAccel ** 0.5:
        #     self.full_stop()
        # else:
        if abs(self.velocity['x']) > 20 or abs(self.velocity['y']) > 20:
            self.full_stop()
            return

        for bounty_ in self.bounties:
            dictance_to_bounty = ((bounty_.x - self.x) ** 2 + (bounty_.y - self.y) ** 2) ** 0.5
            distance_bounty[bounty_] = dictance_to_bounty

        sorted_bounty = sorted(distance_bounty.items(), key=lambda item: item[1])

        if sorted_bounty:
            first_bounty = sorted_bounty[0][0]

            vector_x = first_bounty.x - self.x + self.anomalyAcceleration["x"] * -1 + self.selfAcceleration["x"] * -1 + \
                       self.velocity["x"] * -1
            vector_y = first_bounty.y - self.y + self.anomalyAcceleration["y"] * -1 + self.selfAcceleration["y"] * -1 + \
                       self.velocity["y"] * -1
            vector_len = (vector_x ** 2 + vector_y ** 2) ** 0.5
            k = self.maxAccel / vector_len if vector_len > self.maxAccel else vector_len
            new_vector_x = vector_x * k
            new_vector_y = vector_y * k
            self.set_acc(new_vector_x, new_vector_y)
            # else:
            #     self.save_vector()
            return first_bounty
        return None

    def set_acc(self, x_acc, y_acc):
        self.req["acceleration"] = {"x": x_acc, "y": y_acc}
        # self.req['acceleration'] = [x_acc, y_acc]
        self.req["id"] = self.id

    def cur_req(self):
        return self.req

    def active_shield(self):
        self.req["activateShield"] = True

    def print_id(self):
        print(self.id)

    def save_vector(self):
        po_siebam_x = 0
        po_siebam_y = 0
        for anomaly_ in self.anomalies:
            if ((anomaly_.x - self.x) ** 2 + (anomaly_.y - self.y) ** 2) ** 0.5 <= anomaly_.effectiveRadius:
                break
            else:
                po_siebam_x += (anomaly_.x - self.x) * -1
                po_siebam_y += (anomaly_.y - self.y) * -1
        else:
            vector_len = (po_siebam_x ** 2 + po_siebam_y ** 2) ** 0.5
            k = self.maxAccel / vector_len if vector_len > self.maxAccel else vector_len
            new_vector_x = po_siebam_x * k
            new_vector_y = po_siebam_y * k
            self.set_acc(new_vector_x, new_vector_y)

    def full_stop(self):
        if abs(self.velocity["x"]) > 0 and abs(self.velocity["y"]) > 0:
            result_x = -1 * self.velocity["x"] + self.anomalyAcceleration["x"] * -1 + self.selfAcceleration["x"] * -1
            result_y = -1 * self.velocity["y"] + self.anomalyAcceleration["y"] * -1 + self.selfAcceleration["y"] * -1
            vector_len = (result_x ** 2 + result_y ** 2) ** 0.5
            k = self.maxAccel / vector_len if vector_len > self.maxAccel else vector_len
            new_vector_x = result_x * k
            new_vector_y = result_y * k

            self.set_acc(new_vector_x,
                         new_vector_y)
