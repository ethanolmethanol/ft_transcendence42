import {ArenaResponse} from "./arena-response.interface";

export interface TournamentPlayer {
  user_id: number;
  arena: ArenaResponse | null;
}
