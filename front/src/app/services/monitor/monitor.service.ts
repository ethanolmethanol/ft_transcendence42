import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_GAME } from "../../constants";
import { WebSocketUrlResponse } from "../../interfaces/web-socket-url-response.interface";

@Injectable({
  providedIn: 'root'
})
export class MonitorService {

  constructor(private http: HttpClient) {}

  public createWebSocketUrl(postData: string): Observable<WebSocketUrlResponse> {
    return this.http.post<WebSocketUrlResponse>(`${API_GAME}/create_channel/`, postData);
  }

  public joinWebSocketUrl(postData: string): Observable<WebSocketUrlResponse> {
    return this.http.post<WebSocketUrlResponse>(`${API_GAME}/join_channel/`, postData);
  }

  public isUserInGame(postData: string): Observable<{isInChannel: boolean}> {
    return this.http.post<{isInChannel: boolean}>(`${API_GAME}/is_user_in_channel/`, postData);
  }
}

