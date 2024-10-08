import { Injectable } from '@angular/core';
import { Subscription } from "rxjs";
import { WebSocketService } from "../web-socket/web-socket.service";
import { ErrorResponse } from "../../interfaces/error-response.interface";
import { ArenaResponse } from "../../interfaces/arena-response.interface";
import {AssignationsResponse} from "../../interfaces/assignation.interface";

@Injectable({
  providedIn: 'root'
})
export class ConnectionService {

  private connectionOpenedSubscription?: Subscription;
  private WebSocketSubscription?: Subscription;
  private WebSocketMessagesSubscription?: Subscription;
  private joinSubscription?: Subscription;
  private lobbyID: string = '';

  constructor(private webSocketService: WebSocketService) {
    console.log('Connection service initialized');
  }

  public async listenToWebSocketMessages(
    handleGameUpdate: (response: string) => Promise<void>,
    handleGameError: (response: ErrorResponse) => void
  ){
    this.WebSocketMessagesSubscription = this.webSocketService.getMessages().subscribe(async message => {
      // console.log('Received WebSocket message:', message);
      const data = JSON.parse(message);
      if (data.type === 'game_update') {
        await handleGameUpdate(data.update);
      } else if (data.type === 'game_error') {
        handleGameError(data.error);
      }
    });
  }

  public establishConnection(arenaSetter: (response: ArenaResponse) => void, lobby_id?: string, arena_id: number | null = null, isTournament: boolean =false) {
    if (lobby_id) {
      // Connect to the existing arena
      this.lobbyID = lobby_id;
      this.webSocketService.connect(lobby_id, isTournament);
      this.handleWebSocketConnection(arena_id, arenaSetter);
    }
  }

  private handleWebSocketConnection(arena_id: number | null = null, arenaSetter: (response: ArenaResponse) => void){
    this.connectionOpenedSubscription = this.webSocketService.getConnectionOpenedEvent().subscribe(() => {
      console.log('WebSocket connection opened');
      this.joinSubscription = this.webSocketService.join(arena_id).subscribe((arena: ArenaResponse) => {
        console.log('Joined arena:', arena);
        arenaSetter(arena);
      });
    });
  }

  public endConnection() {
    this.webSocketService.disconnect();
    this.connectionOpenedSubscription?.unsubscribe();
    this.joinSubscription?.unsubscribe();
    this.WebSocketSubscription?.unsubscribe();
    this.WebSocketMessagesSubscription?.unsubscribe();
    console.log('WebSocket connection closed');
  }

  public getLobbyID(): string {
    return this.lobbyID;
  }
}
