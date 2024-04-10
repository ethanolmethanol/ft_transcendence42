import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_GAME } from "../../constants";

export interface WebSocketUrlResponse {
  arenaID: string;
}

@Injectable({
  providedIn: 'root'
})
export class MonitorService {

  constructor(private http: HttpClient) {}

  public getWebSocketUrl(postData: string): Observable<WebSocketUrlResponse> {
    return this.http.post<WebSocketUrlResponse>(`${API_GAME}/join/`, postData);
  }
}
