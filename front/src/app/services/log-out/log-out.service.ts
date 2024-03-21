import { Injectable } from '@angular/core';
import {Router} from "@angular/router";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import { Observable } from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class LogoutService {

  private apiUrl = 'https://localhost:8000/api';

  constructor(private router: Router, private http: HttpClient) {}

  public logout(): void {
    // Make the HTTP request with the headers
    this.processLogout().subscribe();
    // this.removeCookie('csrftoken');
    // this.removeCookie('sessionid');
  }

  private processLogout() {
    return this.http.post(`${this.apiUrl}/logout/`, {}, { withCredentials: true });
  }
  private removeCookie(name: string) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
  }
}
