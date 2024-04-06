import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  private socket: WebSocket | null;
  private messages: Subject<string> = new Subject<string>();
  private heartbeatInterval: any;

  constructor() {
    this.socket = null;
  }

  public connect(roomName: string): void {
    const url = `wss://localhost:8001/ws/game/${roomName}/`;
    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      // this.heartbeatInterval = setInterval(() => {
      //   if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      //     this.socket.send('heartbeat');
      //   }
      // }, 5000);
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
      clearInterval(this.heartbeatInterval);
    };
  }

  public sendPaddleMovement(paddleId: number, position: number): void {
    console.log('Sending paddle movement:', { paddleId, position });
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ paddleId, position }));
    } else {
      console.log('WebSocket is not open when trying to send paddle movement');
    }
  }

  public send(message: string): void {
    if (this.socket) {
      this.socket.send(message);
    }
  }

  public getMessages(): Observable<string> {
    return this.messages.asObservable();
  }
}
