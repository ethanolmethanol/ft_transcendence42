import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private socket: WebSocket | null;
  private connectionOpened: Subject<void> = new Subject<void>();
  private messages: Subject<string> = new Subject<string>();

  constructor() {
    this.socket = null;
  }

  public connect(channelID: string): void {
    const url = `wss://localhost:8001/ws/game/${channelID}/`;
    this.socket = new WebSocket(url);

    this.socket.onopen = (event) => {
      console.log('WebSocket connection opened:', event);
      this.connectionOpened.next();
    };

    this.socket.onmessage = (event) => this.messages.next(event.data);

    this.socket.onerror = (event) => {
      console.error('WebSocket error observed:', event);
      if (this.socket) {
        console.error('WebSocket state:', this.socket.readyState);
      }
    };

    this.socket.onclose = (event) => {
      console.log('WebSocket connection closed:', event);
      if (this.socket) {
        console.log('WebSocket state:', this.socket.readyState);
        console.log('Close event code:', event.code);
        console.log('Close event reason:', event.reason);
        console.log('Close event wasClean:', event.wasClean);
      } else {
        console.log('WebSocket was null');
      }
    };
  }

  public sendPaddleMovement(paddleId: number, position: number): void {
    console.log('Sending paddle movement:', { paddleId, position });
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.send('move_paddle', {paddleId, position});
    } else {
      console.log('WebSocket is not open when trying to send paddle movement');
    }
  }

  public join(arenaID: string): void {
    console.log('Join');
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.send('join', {"username": "Player", "arenaID": arenaID});
    } else {
      console.log('WebSocket is not open when trying to join arena');
    }
  }

  public send(type: string, message: Object): void {
    if (this.socket) {
      this.socket.send(JSON.stringify({
        type: type,
        message: message
      }))}
  }

  public getConnectionOpenedEvent(): Observable<void> {
    return this.connectionOpened.asObservable();
  }

  public getMessages(): Observable<string> {
    return this.messages.asObservable();
  }
}
