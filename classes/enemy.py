class Enemy:
    def __init__(self, x, y, velocity, health, status, killBounty, shieldLeftMs):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.health = health
        self.status = status
        self.killBounty = killBounty
        self.shieldLeftMs = shieldLeftMs
