import { Injectable } from '@angular/core';
import { Subscription } from "rxjs";
import { Router } from "@angular/router";
import { MonitorService } from "../monitor/monitor.service";
import { WebSocketService } from "../web-socket/web-socket.service";
import { ErrorResponse } from "../../interfaces/error-response.interface";
import { ArenaResponse } from "../../interfaces/arena-response.interface";

@Injectable({
  providedIn: 'root'
})
export class ConnectionService {

  private connectionOpenedSubscription?: Subscription;
  private WebSocketSubscription?: Subscription;
  private WebSocketMessagesSubscription?: Subscription;
  private joinSubscription?: Subscription;

  constructor(private router: Router, private monitorService: MonitorService, private webSocketService: WebSocketService) {
    console.log('Connection service initialized');
  }

  public listenToWebSocketMessages(handleGameUpdate: (response: string) => void, handleGameError: (response: ErrorResponse) => void) {
    this.WebSocketMessagesSubscription = this.webSocketService.getMessages().subscribe(message => {
      console.log('Received WebSocket message:', message);
      const data = JSON.parse(message);
      if (data.type === 'game_update') {
        handleGameUpdate(data.update);
      } else if (data.type === 'game_error') {
        handleGameError(data.error);
      }
    });
  }

  public establishConnection(arenaSetter: (response: ArenaResponse) => void, channel_id?: string, arena_id?: number) {
    if (channel_id && arena_id) {
      // Connect to the existing arena
      this.accessArena(channel_id, arena_id, arenaSetter)
    }
  }

  private accessArena(channel_id: string, arena_id: number, arenaSetter: (response: ArenaResponse) => void) {
    this.webSocketService.connect(channel_id);
    this.handleWebSocketConnection(arena_id, arenaSetter);
  }

  private handleWebSocketConnection(arena_id: number, arenaSetter: (response: ArenaResponse) => void){
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
    this.WebSocketSubscription?.unsubscribe();
    this.WebSocketMessagesSubscription?.unsubscribe();
    this.joinSubscription?.unsubscribe();
    console.log('WebSocket connection closed');
  }
}
