import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable, tap} from 'rxjs';

interface SignInResponse {
  detail: string;
  sessionId: string;
  csrfToken: string;
}
@Injectable({
  providedIn: 'root'
})

export class AuthService {
  private apiUrl = 'https://localhost:8000/api'; // Replace with your Django server URL

  constructor(private http: HttpClient) {}


  signIn(login: string, password: string): Observable<SignInResponse> {
    return this.http.post<SignInResponse>(`${this.apiUrl}/signin/`, { login, password }).pipe(
      tap(response => {
        if (response.detail === 'Successfully signed in.') {
          console.log('csrfToken', response.csrfToken);
        }
      })
    );
  }

  signUp(username: string, email: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/signup/`, { username, email, password });
  }
  isLoggedIn(): boolean {
    return this.getCookie('csrftoken') !== null; // TO DO: ASk to back if the sessionId is correct
  }

  private getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop()?.split(';').shift() || null;
    }
    return null;
  }
}
