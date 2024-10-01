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
    return this.http.post<WebSocketUrlResponse>(`${API_GAME}/create_lobby/`, postData).pipe(
      catchError(this.handleError<WebSocketUrlResponse>('createWebSocketUrl'))
    );
  }

  public joinWebSocketUrl(postData: string): Observable<WebSocketUrlResponse> {
    return this.http.post<WebSocketUrlResponse>(`${API_GAME}/join_lobby/`, postData).pipe(
      catchError(this.handleError<WebSocketUrlResponse>('joinWebSocketUrl'))
    );
  }

  public joinSpecificWebSocketUrl(postData: string): Observable<WebSocketUrlResponse> {
    console.log("Joining specific lobby with data: " + postData);
    return this.http.post<WebSocketUrlResponse>(`${API_GAME}/join_specific_lobby/`, postData).pipe(
      catchError(this.handleError<WebSocketUrlResponse>('joinSpecificWebSocketUrl'))
    );
  }

  public joinTournamentWebSocketUrl(postData: string): Observable<WebSocketUrlResponse> {
    return this.http.post<WebSocketUrlResponse>(`${API_GAME}/join_tournament/`, postData).pipe(
      catchError(this.handleError<WebSocketUrlResponse>('joinTournamentWebSocket')))
  }
}
