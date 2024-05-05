import { OnDestroy, Injectable } from '@angular/core';
import { WebSocketService } from "../../services/web-socket/web-socket.service";
import { MonitorService } from "../../services/monitor/monitor.service";
import { ArenaResponse } from "../../interfaces/arena-response.interface";
import { Subscription } from "rxjs";
import { ErrorResponse } from "../../interfaces/error-response.interface";
import { Router } from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class ConnectionComponent implements OnDestroy {
  private postData = JSON.stringify({
    "username": "Player_name",
    "playerSpecs": {"nbPlayers": 2, "mode": 0}
  })
  private connectionOpenedSubscription?: Subscription;
  private WebSocketSubscription?: Subscription;
  private WebSocketMessagesSubscription?: Subscription;
  private joinSubscription?: Subscription;

  constructor(private router: Router, private monitorService: MonitorService, private webSocketService: WebSocketService) {}

  public ngOnDestroy() {
    this.endConnection();
    this.connectionOpenedSubscription?.unsubscribe();
    this.WebSocketSubscription?.unsubscribe();
    this.WebSocketMessagesSubscription?.unsubscribe();
    this.joinSubscription?.unsubscribe();
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

  private endConnection() {
    this.webSocketService.disconnect();
    console.log('WebSocket connection closed');
  }
}
