import math
from back_game.game_settings.game_constants import *
from back_game.game_physics.position import Position
from back_game.game_physics.vector import Vector


import logging
log = logging.getLogger(__name__)


class Paddle:
    def __init__(self, slot=1, num_players=2):
        self.slot = slot
        self.status = LISTENING
        self.speed = PADDLE_INITIAL_SPEED_RATE
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.rate = 0.5
        self.axis = self.__calculate_axis(num_players)
        self.__update_position()
        log.info(f"Paddle created at {self.position.to_dict()}")

    def __update_position(self):
        self.position = self.__convert_rate_to_position(self.rate)
        self.bottom = self.position.y + self.height / 2
        self.top = self.position.y - self.height / 2
        self.left = self.position.x - self.width / 2
        self.right = self.position.x + self.width / 2
        self.convexity_center = self.__get_convexity_center()

    def __calculate_axis(self, num_players):
        if (num_players == 2):
            return self.__calculate_axis_2_players()
        else:
            return self.__calculate_regular_axis(num_players)

    def __calculate_axis_2_players(self):
        demi_height = self.height / 2
        if (self.slot == 1):
            start = Position(PADDLE_OFFSET, demi_height)
            end = Position(PADDLE_OFFSET, GAME_HEIGHT - demi_height)
        else:
            start = Position(GAME_WIDTH - PADDLE_OFFSET, demi_height)
            end = Position(GAME_WIDTH - PADDLE_OFFSET, GAME_HEIGHT - demi_height)
        return {"start": start.round(), "end": end.round()}

    def __calculate_regular_axis(self, num_players):
        angle =  2 * math.pi * (self.slot - 1) / num_players

        start = Position(
            GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle),
            GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle)
        )
        end = Position(
            GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle + math.pi),
            GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle + math.pi)
        )
        log.info(f"Slot: {self.slot}, Angle: {angle}, Start: {start.to_dict()}, End: {end.to_dict()}")
        return {"start": start.round(), "end": end.round()}

    def __convert_rate_to_position(self, rate):
        return Position(
            self.axis["start"].x + (self.axis["end"].x - self.axis["start"].x) * rate,
            self.axis["start"].y + (self.axis["end"].y - self.axis["start"].y) * rate
        ).round()

    def __get_convexity_center(self):
        self.distance_from_center = self.height / (2 * math.tan(CONVEXITY / 2))
        if self.slot == LEFT_SLOT:
            center_x = self.right - self.distance_from_center
        elif self.slot == RIGHT_SLOT:
            center_x = self.left + self.distance_from_center
        return Position(center_x, self.position.y)

    def to_dict(self):
        return {
            "slot": self.slot,
            "position": self.position.to_dict(),
            "speed": self.speed,
            "width": self.width,
            "height": self.height,
        }

    def reset(self):
        self.rate = 0.5
        self.__update_position()

    def update(self, config):
        self.width = config["width"]
        self.height = config["height"]

    def move(self, direction):
        self.rate = min(max(self.rate + self.speed * direction, 0), 1)
        self.__update_position()

    def get_speed_after_collision(self, collision_point):
        speed_component = self.get_speed_direction(collision_point)
        u_speed = speed_component.unit_vector()
        return Vector(INITIAL_BALL_SPEED_COEFF * u_speed.x, INITIAL_BALL_SPEED_COEFF * u_speed.y)

    def get_speed_direction(self, collision_point):
        if self.slot == LEFT_SLOT:
            speed_component_x = self.distance_from_center
        elif self.slot == RIGHT_SLOT:
            speed_component_x = -self.distance_from_center
        speed_component_y = collision_point.y - self.convexity_center.y
        return Vector(speed_component_x, speed_component_y)
