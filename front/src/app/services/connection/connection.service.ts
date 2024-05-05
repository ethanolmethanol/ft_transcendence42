import { Injectable } from '@angular/core';
import {Subscription} from "rxjs";
import {Router} from "@angular/router";
import {MonitorService} from "../monitor/monitor.service";
import {WebSocketService} from "../web-socket/web-socket.service";
import {ErrorResponse} from "../../interfaces/error-response.interface";
import {ArenaResponse} from "../../interfaces/arena-response.interface";

@Injectable({
  providedIn: 'root'
})
export class ConnectionService {

  private postData = JSON.stringify({
    "username": "Player_name",
    "playerSpecs": {"nbPlayers": 2, "mode": 0}
  })
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

  public getGameUrl(channelID: string, arenaID: string): string {
    return `/local-game/${channelID}/${arenaID}`;
  }

  public establishConnection(arenaSetter: (response: ArenaResponse) => void, channelID?: string, arenaID?: string) {
    if (this.webSocketService.socket && this.webSocketService.socket.readyState !== WebSocket.CLOSED) {
      // If a connection is currently open, close it and wait a bit before opening a new one
      this.endConnection();
      setTimeout(() => this.connectAndJoin(arenaSetter, channelID, arenaID), 1000);  // Wait for 1 second
    } else {
      // If no connection is currently open, just open a new one
      this.connectAndJoin(arenaSetter, channelID, arenaID);
    }
  }

  private connectAndJoin(arenaSetter: (response: ArenaResponse) => void, channelID?: string, arenaID?: string) {
    if (channelID && arenaID) {
      // Connect to the existing arena
      this.accessArena(channelID, arenaID, arenaSetter)
    } else {
      // Request a new arena
      this.WebSocketSubscription = this.monitorService.getWebSocketUrl(this.postData).subscribe(response => {
        this.accessArena(response.channelID, response.arena.id, arenaSetter);
      });
    }
  }
  private accessArena(channelID: string, arenaID: string, arenaSetter: (response: ArenaResponse) => void) {
    this.webSocketService.connect(channelID);
    this.handleWebSocketConnection(arenaID, arenaSetter);
    const gameUrl = this.getGameUrl(channelID, arenaID);
    this.router.navigateByUrl(gameUrl);
  }

  private handleWebSocketConnection(arenaID: string, arenaSetter: (response: ArenaResponse) => void){
    this.connectionOpenedSubscription = this.webSocketService.getConnectionOpenedEvent().subscribe(() => {
      console.log('WebSocket connection opened');
      this.joinSubscription = this.webSocketService.join(arenaID).subscribe((arena: ArenaResponse) => {
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
