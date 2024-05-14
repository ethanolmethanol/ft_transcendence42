import logging
import math

from back_game.game_physics.rectangle import Rectangle
from back_game.game_physics.position import Position
from back_game.game_physics.vector import Vector
from back_game.game_settings.game_constants import (
    GAME_HEIGHT,
    GAME_WIDTH,
    INITIAL_BALL_SPEED_COEFF,
    LEFT_SLOT,
    LISTENING,
    PADDLE_INITIAL_SPEED_RATE,
    PADDLE_HEIGHT,
    PADDLE_OFFSET,
    PADDLE_WIDTH,
    RIGHT_SLOT,
)

log = logging.getLogger(__name__)


class Paddle:
    def __init__(self, slot=1, num_players=2):
        self.slot = slot
        self.status = LISTENING
        self.speed = PADDLE_INITIAL_SPEED_RATE
        self.rectangle = Rectangle(slot, Position(0, 0), PADDLE_WIDTH, PADDLE_HEIGHT)
        self.rate = 0.5
        self.axis = self.__calculate_axis(num_players)
        self.__update_position()
        log.info("Paddle created at %s", self.rectangle.position.to_dict())

    def __update_position(self):
        new_position = self.__convert_rate_to_position(self.rate)
        self.rectangle.update_position(new_position)

    def __calculate_axis(self, num_players):
        if num_players == 2:
            return self.__calculate_axis_2_players()
        return self.__calculate_regular_axis(num_players)

    def __calculate_axis_2_players(self):
        demi_height = self.rectangle.height / 2
        if self.slot == 1:
            start = Position(PADDLE_OFFSET, demi_height)
            end = Position(PADDLE_OFFSET, GAME_HEIGHT - demi_height)
        else:
            start = Position(GAME_WIDTH - PADDLE_OFFSET, demi_height)
            end = Position(GAME_WIDTH - PADDLE_OFFSET, GAME_HEIGHT - demi_height)
        return {"start": start.round(), "end": end.round()}

    def __calculate_regular_axis(self, num_players):
        angle = 2 * math.pi * (self.slot - 1) / num_players

        start = Position(
            GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle),
            GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle),
        )
        end = Position(
            GAME_HEIGHT / 2 + GAME_HEIGHT / 2 * math.sin(angle + math.pi),
            GAME_WIDTH / 2 + GAME_WIDTH / 2 * math.cos(angle + math.pi),
        )
        log.info(
            "Slot: %s, Angle: %s, Start: %s, End: %s",
            self.slot,
            angle,
            start.to_dict(),
            end.to_dict(),
        )
        return {"start": start.round(), "end": end.round()}

    def __convert_rate_to_position(self, rate):
        return Position(
            self.axis["start"].x + (self.axis["end"].x - self.axis["start"].x) * rate,
            self.axis["start"].y + (self.axis["end"].y - self.axis["start"].y) * rate,
        ).round()

    def to_dict(self):
        return {
            "slot": self.slot,
            "position": self.rectangle.position.to_dict(),
            "speed": self.speed,
            "width": self.rectangle.width,
            "height": self.rectangle.height,
        }

    def get_dict_update(self):
        return {
            "slot": self.slot,
            "position": self.rectangle.position.to_dict(),
        }

    def get_edges(self):
        return self.rectangle.edges

    def get_position(self):
        return self.rectangle.position

    def reset(self):
        self.rate = 0.5
        self.__update_position()

    def update(self, config):
        self.rectangle.width = config["width"]
        self.rectangle.height = config["height"]

    def move(self, direction):
        self.rate = min(max(self.rate + self.speed * direction, 0), 1)
        self.__update_position()

    def get_ball_speed_after_paddle_collision(self, collision_point):
        speed_component = self.__get_ball_speed_direction(collision_point)
        u_speed = speed_component.unit_vector()
        return Vector(
            INITIAL_BALL_SPEED_COEFF * u_speed.x, INITIAL_BALL_SPEED_COEFF * u_speed.y
        )

    def __get_ball_speed_direction(self, collision_point):
        if self.slot == LEFT_SLOT:
            speed_component_x = self.rectangle.distance_from_center
        elif self.slot == RIGHT_SLOT:
            speed_component_x = -self.rectangle.distance_from_center
        speed_component_y = collision_point.y - self.rectangle.convexity_center.y
        return Vector(speed_component_x, speed_component_y)
