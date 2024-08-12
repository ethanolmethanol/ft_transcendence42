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

export interface Player {
  user_id: string;
  player_name: string;
  score: number;
}

export interface ChannelPlayersResponse {
  players: Player[];
  capacity: number;
}

export interface ArenaResponse {
  id: number;
  status: number;
  players: Player[];
  scores: number[];
  ball: Ball;
  paddles: Paddle[];
  map: Map;
  players_specs: PlayersSpecs;
}
