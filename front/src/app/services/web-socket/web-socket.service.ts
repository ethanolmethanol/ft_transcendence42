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
  private _logoutLobby: BroadcastChannel;
  private _username: string = '';
  private _usernameLoaded: Promise<void> | null = null;

  constructor(private userService: UserService) {
    console.log('WebSocketService created');
    this.socket = null;

    // Initialize the BroadcastChannel
    this._logoutLobby = new BroadcastChannel('_logoutLobby');

    // Listen for messages on the BroadcastChannel
    this._logoutLobby.onmessage = (message) => {
      if (message.data === 'logout') {
        this.giveUp();
      }
    };
  }

  public connect(lobby_id: string, isTournament: boolean): void {
    this.userService.whenUserDataLoaded().then(() => {
      this.whenUsernameLoaded().then(() => {
        this.attemptToConnect(lobby_id, isTournament);
      });
    });
  }

  private attemptToConnect(lobby_id: string, isTournament: boolean): void {
    if (this.socket) {
      console.log('WebSocket connection already open');
      return;
    }

    console.log('Connecting to WebSocket -> ', lobby_id);
    let url;
    if (isTournament) {
      url = `${API_GAME_SOCKET}/ws/game/tournament/${lobby_id}/`;
    } else {
      url = `${API_GAME_SOCKET}/ws/game/classic/${lobby_id}/`;
    }

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

  public join(arena_id: number | null): Observable<ArenaResponse> {
    if (arena_id === null) {
      console.log('Arena ID is null');
    } else {
      console.log(`Join ${arena_id}`);
    }
    const subject = new Subject<ArenaResponse>();
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.send('join', {"user_id": this.userService.getUserID(), "player": this._username, "arena_id": arena_id});
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
    this._username = await this.userService.getUsername();
    this._usernameLoaded = Promise.resolve();
  }

  public whenUsernameLoaded(): Promise<void> {
    if (!this._usernameLoaded) {
      this._usernameLoaded = this.ngOnInit();
    }
    return this._usernameLoaded;
  }

  ngOnDestroy(): void {
    this.disconnect();
    this._logoutLobby.close();
  }
}
