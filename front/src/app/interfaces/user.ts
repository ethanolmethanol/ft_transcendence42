export interface Wins {
  win: number;
  loss: number;
  tie: number;
}

export interface Times {
  local: number;
  remote: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
  win_dict: Wins;
  time_played: Times;
  color_config: string[];
  game_settings: number[];
}
