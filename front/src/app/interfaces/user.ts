export interface Wins {
  win: number;
  loss: number;
  tie: number;
}

export interface Times {
  local: number;
  remote: number;
}

export interface GameCounter {
  local: number;
  remote: number;
  total: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
  game_counter: GameCounter;
  win_dict: Wins;
  time_played: Times;
  color_config: string[];
  game_settings: number[];
}
