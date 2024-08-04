interface Player {
  score: number;
  user_id: number;
}

export interface GameSummaryResponse {
  arena_id: string;
  end_time: string;
  id: number;
  players: Player[];
  winner_user_id: number | undefined;
  is_remote: boolean;
}

export interface GameHistoryResponse {
  has_more: boolean;
  summaries: GameSummaryResponse[];
}
