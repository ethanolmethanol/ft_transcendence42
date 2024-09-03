interface Player {
  user_id: number,
  score: number,
}

export interface TournamentMap {
  [round: number]: {
    [game: number]: {
      players: Player[] | null
    }
  }
}
