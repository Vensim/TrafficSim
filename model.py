import math
import pyglet
from pyglet import shapes


class Map(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Map")
        self.time = 0
        self.batch = pyglet.graphics.Batch()

        self.width = width
        self.height = height

        self.old_position = (0, 0)
        self.new_position = (0, 0)
        self.velocity = 1
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

        self.car = shapes.Circle(width / 2, height / 2, 10, color=(255, 170, 170), batch=self.batch, group=None)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def update(self, delta_time):
        self.time += delta_time

        if self.velocity < 7:
            self.velocity *= self.acceleration
        self.new_position = (self.width / 2 + math.cos(self.time * self.velocity) * self.height / 3,
                             self.height / 2 + math.sin(self.time * self.velocity) * self.height / 3)
        self.car.position = self.new_position

        self.velocity_meter.text = ("Velocity : {:.2f}".format(self.velocity))

        self.distance_step = self.velocity * delta_time
        self.distance += self.distance_step
        print("Speed({}) * Time({}) = Distance ({})".format(self.velocity, delta_time, self.distance_step))
        self.distance_meter.text = ("Distance : {:.2f}".format(self.distance))
        self.old_position = self.new_position

        self.acceleration_meter.text = ("Acceleration : {:.2f}".format(self.acceleration))


# Distance is speed over time: s = v/t
# TODO: Implement velocity

class Car:
    pass


if __name__ == "__main__":
    map = Map(800, 600)
    pyglet.clock.schedule_interval(map.update, 1 / 120)
    pyglet.app.run()
