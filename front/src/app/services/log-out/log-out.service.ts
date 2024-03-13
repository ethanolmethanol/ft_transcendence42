import { Injectable } from '@angular/core';
import {Router} from "@angular/router";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, of} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class LogoutService {

  private apiUrl = 'http://localhost:8000/api';

  constructor(private router: Router, private http: HttpClient) {}

  isLogged() {
    return !!localStorage.getItem('token');
  }

  public logout(): Observable<any> {
    const csrfToken = this.getCookie('csrftoken');
    if (csrfToken) {
      const headers = new HttpHeaders({
        'X-CSRFToken': csrfToken
      });
      return this.http.post(`${this.apiUrl}/logout/`, {}, {headers});
    } else {
      // Handle the case where the csrftoken cookie is not found
      console.error('CSRF token not found');
      return of(null);
    }
  }

  public getCookie(name: string): string | null {
    console.log(document.cookie); // Log the value of document.cookie
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      const poppedPart = parts.pop();
      if (poppedPart) {
        return poppedPart.split(';').shift() || '';
      }
    }
    return null;
  }
}
