import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_GAME } from "../../constants";

interface Position {
  x: number;
  y: number;
}

interface Vector extends Position {}

interface Ball {
  position: Position;
  speed: Vector;
  radius: number;
}

interface Paddle {
  position: Position;
  speed: Vector;
  width: number;
  height: number;
}

interface Map {
  width: number;
  height: number;
}

export interface WebSocketUrlResponse {
  channelID: string;
  arena: {
    id: string;
    status: number;
    players: number[];
    scores: number[];
    ball: Ball;
    paddles: Paddle[];
    map: Map;
  };
}

@Injectable({
  providedIn: 'root'
})
export class MonitorService {

  constructor(private http: HttpClient) {}

  public getWebSocketUrl(postData: string): Observable<WebSocketUrlResponse> {
    return this.http.post<WebSocketUrlResponse>(`${API_GAME}/get_channel_id/`, postData);
  }
}
