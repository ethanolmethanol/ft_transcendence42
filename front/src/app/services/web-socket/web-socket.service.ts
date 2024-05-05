import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import {ArenaResponse} from "../../interfaces/arena-response.interface";

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {
  socket?: WebSocket | null;
  private connectionOpened: Subject<void> = new Subject<void>();
  private messages: Subject<string> = new Subject<string>();

  constructor() {
    this.socket = null;
  }

  public connect(channelID: string): void {
    if (this.socket) {
      console.log('WebSocket connection already open');
      return;
    }

    console.log('Connecting to WebSocket -> ', channelID);
    const url = `wss://localhost:8001/ws/game/${channelID}/`;

    const socket = new WebSocket(url);

    socket.onopen = (event) => {
      console.log('WebSocket connection opened:', event);
      this.connectionOpened.next();
    };

    socket.onmessage = (event) => this.messages.next(event.data);

    socket.onerror = (event) => {
      console.error('WebSocket error observed:', event);
      if (socket) {
        console.error('WebSocket state:', socket.readyState);
      }
    };

    socket.onclose = (event) => {
      console.log('WebSocket connection closed:', event);
      if (socket) {
        console.log('WebSocket state:', socket.readyState);
        console.log('Close event code:', event.code);
        console.log('Close event reason:', event.reason);
        console.log('Close event wasClean:', event.wasClean);
      } else {
        console.log('WebSocket was null');
      }
    };

    this.socket = socket;
  }

  public disconnect(): void {
    if (this.socket) {
      // Remove event listeners
      this.socket.onopen = null;
      this.socket.onmessage = null;
      this.socket.onerror = null;
      this.socket.onclose = null;

      // Close the WebSocket connection if it's open
      if (this.socket.readyState === WebSocket.OPEN) {
        this.socket.close(1000, "Client disconnect.");
      }

      this.socket = null;
    }
  }

  public sendPaddleMovement(playerName: string, direction: number): void {
    console.log('Sending paddle movement:', { playerName, direction });
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.send('move_paddle', {"player": playerName, "direction": direction});
    } else {
      console.log('WebSocket is not open when trying to send paddle movement');
    }
  }

  public giveUp(): void {
    console.log('Giving Up');
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.send('give_up', {});
    } else {
      console.log('WebSocket is not open when trying to give up');
    }
  }

  public rematch(): void {
    console.log('Rematching');
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.send('rematch', {});
    } else {
      console.log('WebSocket is not open when trying to rematch');
    }
  }

  public join(arenaID: string): Observable<ArenaResponse> {
    console.log(`Join ${arenaID}`);
    const subject = new Subject<ArenaResponse>();
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.send('join', {"username": "Player_name", "arenaID": arenaID});
      this.getMessages().subscribe(message => {
        const data = JSON.parse(message);
        if (data.type === 'arena') {
          subject.next(data.arena);
        }
      });
    } else {
      console.log('WebSocket is not open when trying to join arena');
    }
    return subject.asObservable();
  }

  public leave(): void {
    console.log('Leave');
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.send('leave', {});
    } else {
      console.log('WebSocket is not open when trying to leave arena');
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
