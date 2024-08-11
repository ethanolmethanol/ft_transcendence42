import {Position} from "./position.interface";

export interface PaddleUpdateResponse {
  slot: number;
  position: Position;
}

export interface BallUpdateResponse {
  position: Position;
}

export interface ScoreUpdateResponse {
  player_name: string;
}

export interface StartTimerResponse {
  time: number;
  message: string;
}

export interface GameOverUpdateResponse {
  players: string[];
  winner: string;
  time: number;
  message: string;
}

export interface AFKResponse {
  player_name: string;
  time_left: number;
}
