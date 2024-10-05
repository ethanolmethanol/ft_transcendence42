export interface TournamentMap {
  rounds_map: {
    [round: number]: {
      [game: number]: number[] | null;
    };
  };
  winner: number | null;
}
