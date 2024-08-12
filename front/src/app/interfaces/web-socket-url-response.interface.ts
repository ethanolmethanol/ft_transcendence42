import { ArenaResponse } from './arena-response.interface';

export interface WebSocketUrlResponse {
  channel_id: string;
  arena: ArenaResponse | null;
}
