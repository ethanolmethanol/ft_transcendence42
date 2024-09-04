export interface TournamentMap {
  [round: number]: {
    [game: number]: number[] | null
  }
}
