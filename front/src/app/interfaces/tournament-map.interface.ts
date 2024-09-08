export interface TournamentMap {
  rounds_map: {
    [round: string]: {
      [game: number]: number[] | null;
    };
  };
  winner: number | null;
}
