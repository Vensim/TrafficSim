import math
import random

import pyglet
from pyglet import shapes


class Analytics:
    def __init__(self, batch):
        self.batch = batch
        self.velocity_meter = pyglet.text.Label('Velocity : {}'.format(1),
                                                font_size=10,
                                                x=width / 2,
                                                y=height / 7,
                                                anchor_x='center',
                                                anchor_y='center', batch=self.batch)
        self.distance_meter = pyglet.text.Label('Distance : {}'.format(1),
                                                font_size=10,
                                                x=width / 2,
                                                y=height / 7 - 11,
                                                anchor_x='center',
                                                anchor_y='center', batch=self.batch)

        self.acceleration_meter = pyglet.text.Label('Acceleration : {}'.format(1),
                                                    font_size=10,
                                                    x=width / 2,
                                                    y=height / 7 - 22,
                                                    anchor_x='center',
                                                    anchor_y='center', batch=self.batch)

    def update(self, Car):
        self.velocity_meter.text = ("Velocity : {:.2f}".format(Car.velocity))
        self.distance_meter.text = ("Distance : {:.2f}".format(Car.distance))
        self.acceleration_meter.text = ("Acceleration : {:.2f}".format(Car.acceleration))
        pass


class Car:
    def __init__(self, renderer, acceleration=1, max_speed=1, velocity=0.4, number=0):
        self.number = number
        self.current_position = (0, 0)
        self.velocity = random.random()
        self.distance = 0

        self.distance_to_bumper = 0

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

        self.distance_step = self.velocity * time
        self.distance += self.distance_step
        # if self.velocity < self.max_speed:
        #     self.velocity *= self.acceleration

        x_pos = self.width / 2 + math.cos(time * self.velocity) * self.height / 3
        y_pos = self.height / 2 + math.sin(time * self.velocity) * self.height / 3
        self.current_position = (x_pos, y_pos)
        # Todo : track model can be a seperate class
        self.car.position = (x_pos, y_pos)


class Window(pyglet.window.Window):

    def __init__(self, width, height):
        super().__init__(width, height, "TrafficSim")
        self.time = 0
        self.batch = pyglet.graphics.Batch()

        self.width = width
        self.height = height
        self.distance_difference = 30

        self.OuterRim = shapes.Circle(width / 2, height / 2, height / 3, color=(255, 225, 255), batch=self.batch)
        self.InnerRim = shapes.Circle(width / 2, height / 2, height / 3 - 2, color=(0, 0, 0), batch=self.batch)

        self.Lines = []
        self.line = shapes.Line(251, 0, 0, 480, width=1, color=(225, 20, 20), batch=self.batch)

        self.Cars = []

        for i in range(10):
            self.Cars.append(Car(self.batch, number=i))
            # self.Lines.append()

        self.CarInfo = Analytics(self.batch)


    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, delta_time):
        self.time += delta_time

        for car in self.Cars:
            car.update_position(self.time)

        for i in range(3):
            distance_diff = self.Cars[i].distance - self.Cars[i + 1].distance
            x1, y1 = self.Cars[i].current_position
            x2, y2 = self.Cars[i + 1].current_position
            self.line.position = (x1, y1, x2, y2)
            if distance_diff > self.distance_difference:
                self.Cars[i].velocity = (self.Cars[i + 1].velocity * 1.1)
            if distance_diff < self.distance_difference:
                self.Cars[i].velocity = self.Cars[i + 1].velocity * 0.91

        self.CarInfo.update(self.Cars[0])
        # for i in range(34):
        #     ds = self.Cars[i].distance - self.Cars[i+1].distance
        #     print(ds)
        #     if ds < self.distance_difference:
        #         self.Cars[i].velocity =+ 3
        #     if ds < self.distance_difference:
        #         self.Cars[i].velocity =- 3

        # Todo : Update meters
        # self.distance_step = self.velocity * delta_time
        # self.distance += self.distance_step
        # print("Speed({}) * Time({}) = Distance ({})".format(self.velocity, delta_time, self.distance_step))



# Distance is speed over time: s = v/t
# TODO: Implement velocity

height = 800
width = 600

if __name__ == "__main__":
    window = Window(width, height)
    pyglet.clock.schedule_interval(window.update, 1 / 120)
    pyglet.app.run()
