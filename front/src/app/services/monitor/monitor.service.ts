import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_GAME } from "../../constants";

@Injectable({
  providedIn: 'root'
})
export class MonitorService {

  constructor(private http: HttpClient) {}

  public getWebSocketUrl(postData: string): Observable<string> {
    return this.http.post<string>(`${API_GAME}/join/`, postData);
  }
}
