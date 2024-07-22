interface Players {
  score: number;
  user_id: number;
  player_name: string;
}

export interface GameSummaryResponse {
  arena_id: string;
  end_time: string;
  id: number;
  players: Players[];
  winner: string;
}
