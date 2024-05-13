import { ArenaResponse } from './arena-response.interface';

export interface WebSocketUrlResponse {
  channelID: string;
  arena: ArenaResponse;
}
