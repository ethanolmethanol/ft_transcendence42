import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { API_GAME } from "../../constants";
import { WebSocketUrlResponse } from "../../interfaces/web-socket-url-response.interface";

@Injectable({
  providedIn: 'root'
})
export class MonitorService {

  constructor(private http: HttpClient) {}

  private handleError<T>(operation = 'operation') {
    return (error: any): Observable<T> => {
      console.error(`${operation} failed: ${error.message}`);
      throw error;
    };
  }

  public createWebSocketUrl(postData: string): Observable<WebSocketUrlResponse> {
    return this.http.post<WebSocketUrlResponse>(`${API_GAME}/create_channel/`, postData).pipe(
      catchError(this.handleError<WebSocketUrlResponse>('createWebSocketUrl'))
    );
  }

  public joinWebSocketUrl(postData: string): Observable<WebSocketUrlResponse> {
    return this.http.post<WebSocketUrlResponse>(`${API_GAME}/join_channel/`, postData).pipe(
      catchError(this.handleError<WebSocketUrlResponse>('joinWebSocketUrl'))
    );
  }

  public isUserInGame(postData: string): Observable<{isInChannel: boolean}> {
    return this.http.post<{isInChannel: boolean}>(`${API_GAME}/is_user_in_channel/`, postData).pipe(
      catchError(this.handleError<{isInChannel: boolean}>('isUserInGame'))
    );
  }
}
