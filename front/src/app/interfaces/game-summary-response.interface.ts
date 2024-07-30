interface Player {
  score: number;
  user_id: number;
  player_name: string;
}

interface Winner {
  user_id: number;
  player_name: string;
}

export interface GameSummaryResponse {
  arena_id: string;
  end_time: string;
  id: number;
  players: Player[];
  winner: Winner;
}