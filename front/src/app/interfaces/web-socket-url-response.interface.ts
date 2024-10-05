import { ArenaResponse } from './arena-response.interface';

export interface WebSocketUrlResponse {
  lobby_id: string;
  arena: ArenaResponse;
}
