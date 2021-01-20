import math
import numpy as np
import random
from matplotlib import pyplot as plt


class dragon:
    weight = 0
    age = 0
    health = 1
    grow = 1
    food = 1
    climate = 1
    month = 1
    grow_rate = 0
    cnt = 1
    pi = math.acos(-1)
    alive = 1
    max_weight = 0

    l1 = []
    l2 = []

    def __init__(self) -> None:
        self.weight = 10 * (1 + random.random() / 10)
        self.age = 1
        ra = random.random()
        if ra < 0.6:
            self.health = random.random() / 5 + 0.8
        elif ra < 0.95:
            self.health = random.random() / 5 + 0.6
        else:
            self.health = random.random() / 10 * 3
        
        self.month = random.randint(1, 13)
        self.alive = 1
        self.max_weight = self.weight

        self.l1 = []
        self.l2 = []


    def CF(self, a, b):
        if a >= 0 and b >= 0: 
            return a + b - a * b
        if a < 0 and b < 0:
            return a + b + a * b
        return (a + b) / (1 - min(abs(a), abs(b)))
                    
    def get_grow_rate(self):
        self.grow_rate = 0
        
        age_rate = self.age_change()
        health_rate = self.health_change() / 10
        climate_rate = self.climate_change() / 1000
        food_rate = self.food_change() / 1000
        
        self.grow_rate = self.CF(self.grow_rate, age_rate)
        self.grow_rate = self.CF(self.grow_rate, health_rate)
        self.grow_rate = self.CF(self.grow_rate, climate_rate)
        self.grow_rate = self.CF(self.grow_rate, food_rate)

    def climate_change(self):
        month = (self.month - 3 + 12) % 12
        det_climate = math.cos(2 * self.pi / 12 * month)
        return det_climate * (random.random() / 2.5  + 0.6)

    def food_change(self):
        month = (self.month - 1 + 6) % 6
        del_food = math.cos(2 * self.pi / 6 * month)
        return del_food * (random.random() / 2.5 + 0.6)


    def age_change(self):
        age_rate = 0
        if self.age <= 10:
            age_rate = 1.0 / 2 / self.age / self.age / self.age
        elif self.age <= 30:
            age_rate = 1.0 / 3 / (self.age * self.age * self.age)
        elif self.age <= 50:
            age_rate = random.random() / 100 - 0.005
        else:
            age_rate = - 1.0 / (self.age * self.age)
        return age_rate

    def health_change(self):
        det_health = 0
        ra = random.random()
        health_change = random.random()
        health = 0
        if self.age <= 50:
            if self.health > 0.8:
                if ra < 0.8:
                    health = min(1, self.health + random.random() / 20)
                else:
                    health = max(0, self.health - random.random() / 20)
            elif self.health > 0.6:
                if ra < 0.5:
                    health = min(1, self.health + random.random() / 10)
                else:
                    health = min(0, self.health - random.random() / 10)
            else:
                if ra < 0.3:
                    health = min(1, self.health + random.random() / 5)
                else:
                    health = max(0, self.health + random.random() / 5)
        else:
            if self.health > 0.8:
                if ra < 0.2:
                    health = min(1, self.health + random.random() / 20)
                else:
                    health = max(0, self.health - random.random() / 10)
            elif self.health > 0.6:
                if ra < 0.3:
                    health = min(1, self.health + random.random() / 30)
                else:
                    health = min(0, self.health - random.random() / 10)
            else:
                if ra < 0.1:
                    health = min(1, self.health  + random.random() / 50)
                else:
                    health = max(0, self.health + random.random() / 5)
        det_health = health - self.health
        if self.health < 0.3:
            if random.random() < 0.6:
                self.alive = 0
        return det_health / 5
                

    def grow(self) -> None:
        # age count
        self.cnt = self.cnt + 1
        if self.cnt == 13:
            self.cnt = 1
            self.age = self.age + 1

        self.get_grow_rate()

        self.weight = self.weight * (self.grow_rate + 1)

        self.max_weight = max(self.weight, self.max_weight)

        # month count
        self.month = self.month + 1
        if self.month == 13:
            self.month = 1

    def next_month(self):
        cnt = 1
        self.month = 0
        while self.alive == 1 and self.weight >= 0.7 * self.max_weight:
            self.grow()
            self.l1.append(cnt)
            self.l2.append(self.weight)
            cnt = cnt + 1

    def draw(self):
        plt.plot(self.l1, self.l2)
        # if len(self.l1) >= 12:
        #     x = self.l1[11]
        #     y = self.l2[11]
        #     # plt.plot([x, 0], [y, y])
        #     plt.plot([x, x], [0, y])
        #     plt.bar(x, y)
        #     plt.plot(x, y, color='b', linestyle='-')
        #     plt.text(x, y, "(" + str(int(x)) + ", " + str(int(y)) + ")", color='r')
        #
        # if len(self.l1) >= 120:
        #     x = self.l1[119]
        #     y = self.l2[119]
        #     # plt.plot([x, 0], [y, y])
        #     plt.plot([x, x], [0, y])
        #     plt.bar(x, y)
        #     plt.plot(x, y, color='b', linestyle='-')
        #     plt.text(x, y, "(" + str(int(x)) + ", " + str(int(y)) + ")", color='r')
        #
        # if len(self.l1) >= 12 * 30:
        #     x = self.l1[12 * 30 -1]
        #     y = self.l2[12 * 30 -1]
        #     # plt.plot([x, 0], [y, y])
        #     plt.plot([x, x], [0, y])
        #     plt.bar(x, y)
        #     plt.plot(x, y, color='b', linestyle='-')
        #     plt.text(x, y, "(" + str(int(x)) + ", " + str(int(y)) + ")", color='r')
        #
        # if len(self.l1) >= 12 * 50:
        #     x = self.l1[12 * 50 -1]
        #     y = self.l2[12 * 50 -1]
        #     # plt.plot([x, 0], [y, y])
        #     plt.plot([x, x], [0, y])
        #     plt.bar(x, y)
        #     plt.plot(x, y, color='b', linestyle='-')
        #     plt.text(x, y, "(" + str(int(x)) + ", " + str(int(y)) + ")", color='r')


if __name__ == "__main__":
    test1 = dragon()
    test1.next_month()
    test1.draw()

    test2 = dragon()
    test2.next_month()
    test2.draw()

    test3 = dragon()
    test3.next_month()
    test3.draw()

    plt.xlabel("month")
    plt.ylabel("weight")

    plt.show()