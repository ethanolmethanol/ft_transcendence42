export interface Wins {
  win: number;
  loss: number;
  tie: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
  win_dict: Wins;
  time_played: number;
  color_config: string[];
  game_settings: number[];
}
