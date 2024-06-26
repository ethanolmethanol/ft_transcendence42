import { Position } from './position.interface';

interface Vector extends Position {}

interface Ball {
  position: Position;
  speed: Vector;
  radius: number;
}

interface Paddle {
  slot: number;
  position: Position;
  speed: number;
  width: number;
  height: number;
}

interface Map {
  width: number;
  height: number;
}

export interface ArenaResponse {
  id: string;
  status: number;
  players: number[];
  scores: number[];
  ball: Ball;
  paddles: Paddle[];
  map: Map;
}
