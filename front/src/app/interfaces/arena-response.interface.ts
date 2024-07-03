import { Position } from './position.interface';

interface Vector extends Position {}

interface Ball {
  position: Position;
  speed: Vector;
  radius: number;
}

interface Paddle {
  slot: number;
  player_name: string;
  position: Position;
  speed: number;
  width: number;
  height: number;
}

interface Map {
  width: number;
  height: number;
}

interface PlayersSpecs {
  nb_players: number;
  mode: number;
}

export interface ArenaResponse {
  id: number;
  status: number;
  players: string[];
  scores: number[];
  ball: Ball;
  paddles: Paddle[];
  map: Map;
  players_specs: PlayersSpecs;
}
