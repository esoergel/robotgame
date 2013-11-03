import random, math

class Robot:
    obstacles = [
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
        (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0),
        (15, 0),(16, 0), (17, 0), (18, 0), (0, 1), (1, 1), (2, 1), (3, 1),
        (4, 1), (5, 1), (6, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1),
        (17, 1), (18, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (14, 2),
        (15, 2), (16, 2), (17, 2), (18, 2), (0, 3), (1, 3), (2, 3), (16, 3),
        (17, 3), (18, 3), (0, 4), (1, 4), (2, 4), (16, 4), (17, 4), (18, 4),
        (0, 5), (1, 5), (17, 5), (18, 5), (0, 6), (1, 6), (8, 6), (9, 6),
        (10, 6), (17, 6), (18, 6), (0, 7), (7, 7), (8, 7), (9, 7), (10, 7),
        (11, 7), (18, 7), (0, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8),
        (11, 8), (12, 8), (18, 8), (0, 9), (6, 9), (7, 9), (8, 9), (9, 9),
        (10, 9), (11, 9), (12, 9), (18, 9), (0, 10), (6, 10), (7, 10), (8, 10),
        (9, 10), (10, 10), (11, 10), (12, 10), (18, 10), (0, 11), (7, 11),
        (8, 11), (9, 11), (10, 11), (11, 11), (18, 11), (0, 12), (1, 12),
        (8, 12), (9, 12), (10, 12), (17, 12), (18, 12), (0, 13), (1, 13),
        (17, 13), (18, 13), (0, 14), (1, 14), (2, 14), (16, 14), (17, 14),
        (18, 14), (0, 15), (1, 15), (2, 15), (16, 15), (17, 15), (18, 15),
        (0, 16), (1, 16), (2, 16), (3, 16), (4, 16), (14, 16), (15, 16),
        (16, 16), (17, 16), (18, 16), (0, 17), (1, 17), (2, 17), (3, 17),
        (4, 17), (5, 17), (6, 17), (12, 17), (13, 17), (14, 17), (15, 17),
        (16, 17), (17, 17), (18, 17), (0, 18), (1, 18), (2, 18), (3, 18),
        (4, 18), (5, 18), (6, 18), (7, 18), (8, 18), (9, 18), (10, 18),
        (11, 18), (12, 18), (13, 18), (14, 18), (15, 18), (16, 18), (17, 18),
        (18, 18)
    ]
    spawn_coords = [
        (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (5, 2), (6, 2), (12, 2),
        (13, 2), (3, 3), (4, 3), (14, 3), (15, 3), (3, 4), (15, 4), (2, 5),
        (16, 5), (2, 6), (16, 6), (1, 7), (17, 7), (1, 8), (17, 8), (1, 9),
        (17, 9), (1, 10), (17, 10), (1, 11), (17, 11), (2, 12), (16, 12),
        (2, 13), (16, 13), (3, 14), (15, 14), (3, 15), (4, 15), (14, 15),
        (15, 15), (5, 16), (6, 16), (12, 16), (13, 16), (7, 17), (8, 17),
        (9, 17), (10, 17), (11, 17)
    ]
    spawn_every = 10
    spawn_per_player = 5
    board_size = 19
    robot_hp = 50
    attack_range = (15, 20)
    collision_damage = 5
    suicide_damage = 10
    # game = {
        # # a dictionary of all robots on the field mapped
        # # by {location: robot}
        # 'robots': {
            # (x1, y1): {   
                # 'location': (x1, y1),
                # 'hp': hp,
                # 'player_id': player_id,
            # },
            # # ...and the rest of the robots
        # },
        # # number of turns passed (starts at 0)
        # 'turn': turn
    # }
    # location zero indexed from top left

    def adj_squares(self):
        return [
            (self.x-1, self.y),
            (self.x+1, self.y),
            (self.x, self.y-1),
            (self.x, self.y+1),
        ]

    def parse_robots(self):
        self.occupied = self.game['robots'].keys()
        self.enemies = []
        self.friends = []
        self.adj_enemies = []
        self.adj_friends = []
        for robot in self.game['robots'].values():
            if robot['player_id'] == self.player_id:
                self.friends.append(robot)
            else:
                self.enemies.append(robot)
            x, y = robot['location']
            if abs(self.x-x) + abs(self.y-y) == 1:
                if robot['player_id'] == self.player_id:
                    self.adj_friends.append(robot)
                else:
                    self.adj_enemies.append(robot)
    
    def is_good_square(self, x, y):
        stuff = self.occupied + self.obstacles
        turn = self.game['turn'] 
        if turn % self.spawn_every == self.spawn_every - 1:
            stuff += self.spawn_coords
        return (x, y) not in stuff

    def distance_to(self, x, y):
        return math.sqrt((self.x - x)**2 + (self.y - y)**2)

    def distance_to_bot(self, robot):
        if robot is None:
            return 10000
        return self.distance_to(*robot['location'])

    def closest_enemy(self):
        # return min(
            # self.enemies,
            # key=lambda robot: self.distance_to(*robot['location'])
        # )
        closest = None
        for robot in self.enemies:
            if self.distance_to_bot(robot) < self.distance_to_bot(closest):
                closest = robot
        return closest

    def act(self, game):
        self.game = game
        self.x, self.y = self.location
        self.parse_robots()
        # print "Robot %s, %s adjacent" % (self.location, len(self.adj_enemies)),
        if len(self.adj_enemies) > 1:
            # probably shouldn't do this until health is < 20
            # otherwise attack one with least health
            return self.suicide()
        elif len(self.adj_enemies) == 1:
            return self.attack(self.adj_enemies[0])
        # elif self.distance_to_bot(self.closest_enemy()) < 5:
            # return self.hunt(self.closest_enemy())
        else:
            # meander
            options = self.adj_squares()
            random.shuffle(options)
            while options:
                square = options.pop()
                if self.is_good_square(*square):
                    return self.move_to(*square)
            return self.guard()

    def move_to(self, x, y):
        return ['move', (x, y)]

    def move_towards(self, x, y):
        dx = abs(self.x - x)
        dy = abs(self.y - y)
        if dx >= dy:
            return self.move((x-self.x)/dx, 0)
        else:
            return self.move(0, (y-self.y)/dy)

    def hunt(self, robot):
        return self.move_towards(*robot['location'])

    def move(self, x, y):
        "one must be zero, the other 1 or -1"
        return ['move', (self.x+x, self.y+y)]

    def attack(self, robot):
        "one must be zero, the other 1 or -1"
        x, y = robot['location']
        return ['attack', (x, y)]

    def guard(self):
        return ['guard']

    def suicide(self):
        return ['suicide']

