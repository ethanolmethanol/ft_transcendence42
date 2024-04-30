import { OnDestroy, Injectable } from '@angular/core';
import { WebSocketService } from "../../services/web-socket/web-socket.service";
import { MonitorService } from "../../services/monitor/monitor.service";
import { ArenaResponse } from "../../interfaces/arena-response.interface";
import { Subscription } from "rxjs";

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

    constructor(private monitorService: MonitorService, private webSocketService: WebSocketService) {}

    public ngOnDestroy() {
        this.endConnection();
        this.connectionOpenedSubscription?.unsubscribe();
        this.WebSocketSubscription?.unsubscribe();
        this.WebSocketMessagesSubscription?.unsubscribe();
    }

    public listenToWebSocketMessages(handleGameUpdate: (response: string) => void) {
        this.WebSocketMessagesSubscription = this.webSocketService.getMessages().subscribe(message => {
            console.log('Received WebSocket message:', message);
            const data = JSON.parse(message);
            if (data.type === 'game_update') {
                handleGameUpdate(data.update);
            }
        });
    }

    public establishConnection(arenaSetter: (response: ArenaResponse) => void) {
        this.WebSocketSubscription = this.monitorService.getWebSocketUrl(this.postData).subscribe(response => {
            console.log(response);
            this.webSocketService.connect(response.channelID);
            this.handleWebSocketConnection(response.arena, arenaSetter);
        });
    }

    private handleWebSocketConnection(arena: ArenaResponse, arenaSetter: (response: ArenaResponse) => void){
        this.connectionOpenedSubscription = this.webSocketService.getConnectionOpenedEvent().subscribe(() => {
            console.log('WebSocket connection opened');
            this.webSocketService.join(arena.id);
            arenaSetter(arena);
        });
    }

    private endConnection() {
        console.log('WebSocket connection closed');
        this.webSocketService.disconnect();
    }
}
