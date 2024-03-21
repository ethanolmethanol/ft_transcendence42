import { Injectable } from '@angular/core';
import {Router} from "@angular/router";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class LogoutService {

  private apiUrl = 'https://localhost:8000/api';

  constructor(private router: Router, private http: HttpClient) {}

  public logout(): void {
    this.processLogout().subscribe();
  }

  private processLogout() {
    return this.http.post(`${this.apiUrl}/logout/`, {}, { withCredentials: true });
  }
}
