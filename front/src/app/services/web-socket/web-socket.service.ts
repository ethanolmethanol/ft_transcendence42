import {Injectable, OnDestroy} from '@angular/core';
import { Observable, Subject } from 'rxjs';
import {ArenaResponse} from "../../interfaces/arena-response.interface";
import {UserService} from "../user/user.service";
import { OnInit } from '@angular/core';
import { API_GAME_SOCKET } from "../../constants";

@Injectable({
  providedIn: 'root'
})
export class WebSocketService implements OnInit, OnDestroy {
  socket?: WebSocket | null;
  private _connectionOpened: Subject<void> = new Subject<void>();
  private _messages: Subject<string> = new Subject<string>();
  private _logoutChannel: BroadcastChannel;

  constructor(private userService: UserService) {
    console.log('WebSocketService created');
    this.socket = null;

    // Initialize the BroadcastChannel
    this._logoutChannel = new BroadcastChannel('_logoutChannel');

    // Listen for messages on the BroadcastChannel
    this._logoutChannel.onmessage = (message) => {
      if (message.data === 'logout') {
        this.giveUp();
      }
    };
  }

  public connect(channel_id: string): void {
    this.userService.whenUserDataLoaded().then(() => {
      this.attemptToConnect(channel_id);
    });
  }

  private attemptToConnect(channel_id: string): void {
    if (this.socket) {
      console.log('WebSocket connection already open');
      return;
    }

    console.log('Connecting to WebSocket -> ', channel_id);
    const url = `${API_GAME_SOCKET}/ws/game/${channel_id}/`;

    const socket = new WebSocket(url);

    socket.onopen = (event) => {
      console.log('WebSocket connection opened:', event);
      this._connectionOpened.next();
    };

    socket.onmessage = (event) => this._messages.next(event.data);

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

  public join(arena_id: number): Observable<ArenaResponse> {
    console.log(`Join ${arena_id}`);
    const subject = new Subject<ArenaResponse>();
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.send('join', {"user_id": this.userService.getUserID(), "player": this.userService.getUsername(), "arena_id": arena_id});
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

  public send(type: string, message: Object): void {
    if (this.socket) {
      this.socket.send(JSON.stringify({
        type: type,
        message: message
      }))}
  }

  public getConnectionOpenedEvent(): Observable<void> {
    return this._connectionOpened.asObservable();
  }

  public getMessages(): Observable<string> {
    return this._messages.asObservable();
  }

  async ngOnInit() : Promise<void> {
    await this.userService.whenUserDataLoaded();
  }

  ngOnDestroy(): void {
    this.disconnect();
    this._logoutChannel.close();
  }
}
