import math
import random
from typing import List

import pyglet
from pyglet import shapes

class Car:
    def __init__(self, renderer, acceleration=1.001, max_speed=5, velocity=0.4, number=0):
        self.old_position = (0, 0)
        self.new_position = (0, 0)
        self.velocity = random.random()
        self.distance = 0

        self.width = width
        self.height = height
        self.acceleration = acceleration
        self.max_speed = max_speed

        # Random colour car
        RGB = tuple(int((random.random() * 255)) for _ in range(3))
        self.car = shapes.Circle(height / 2, width / 2, 10, color=RGB, batch=renderer)

    def update_position(self, time):
        """
        Updates new position of car
        :param dt: difference in time
        :return:
        """

        if self.velocity < self.max_speed:
            self.velocity *= self.acceleration

        # Todo : track model can be a seperate class
        self.car.position = (self.width / 2 + math.cos(time * self.velocity) * self.height / 3,
                             self.height / 2 + math.sin(time * self.velocity) * self.height / 3)


class Window(pyglet.window.Window, Car):
    Cars: List[Car]

    def __init__(self, width, height):
        super().__init__(width, height, "TrafficSim")
        self.time = 0
        self.batch = pyglet.graphics.Batch()

        self.width = width
        self.height = height

        self.old_position = (0, 0)
        self.new_position = (0, 0)
        self.velocity = 0.5
        self.distance = 0
        self.acceleration = 1.001

        self.velocity_meter = pyglet.text.Label('Velocity : {}'.format(int(self.velocity)),
                                                font_size=10,
                                                x=self.width / 2,
                                                y=self.height / 7,
                                                anchor_x='center',
                                                anchor_y='center', batch=self.batch)
        self.distance_meter = pyglet.text.Label('Distance : {}'.format(int(self.distance)),
                                                font_size=10,
                                                x=self.width / 2,
                                                y=self.height / 7 - 11,
                                                anchor_x='center',
                                                anchor_y='center', batch=self.batch)

        self.acceleration_meter = pyglet.text.Label('Acceleration : {}'.format(int(self.distance)),
                                                    font_size=10,
                                                    x=self.width / 2,
                                                    y=self.height / 7 - 22,
                                                    anchor_x='center',
                                                    anchor_y='center', batch=self.batch)

        self.OuterRim = shapes.Circle(width / 2, height / 2, height / 3, color=(255, 225, 255), batch=self.batch)
        self.InnerRim = shapes.Circle(width / 2, height / 2, height / 3 - 2, color=(0, 0, 0), batch=self.batch)

        # Ideal oval shape has axis ratio of 2/1, minor/major.
        # self.track = shapes.Ellipse(width/2, height/2, 300, 150, color=(122, 133, 122), batch=self.batch, group=None)
        self.Cars = []

        for i in range(5):
            self.Cars.append(Car(self.batch, number=i))

        self.car1 = Car(self.batch, max_speed=2, velocity=0.6)
        self.car2 = Car(self.batch, max_speed=4, velocity=0.4)
        self.car3 = Car(self.batch, max_speed=10, velocity=0.1)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, delta_time):
        self.time += delta_time

        for car in self.Cars:
            car.update_position(self.time)


        self.car1.update_position(self.time)
        self.car2.update_position(self.time)
        self.car3.update_position(self.time)

        self.velocity_meter.text = ("Velocity : {:.2f}".format(self.velocity))

        # Todo : Update meters
        # self.distance_step = self.velocity * delta_time
        # self.distance += self.distance_step
        # print("Speed({}) * Time({}) = Distance ({})".format(self.velocity, delta_time, self.distance_step))
        # self.distance_meter.text = ("Distance : {:.2f}".format(self.distance))
        # self.old_position = self.new_position
        #
        # self.acceleration_meter.text = ("Acceleration : {:.2f}".format(self.acceleration))


# Distance is speed over time: s = v/t
# TODO: Implement velocity

height = 800
width = 600
if __name__ == "__main__":
    window = Window(width, height)
    pyglet.clock.schedule_interval(window.update, 1 / 120)
    pyglet.app.run()
