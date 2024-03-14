import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable, tap} from 'rxjs';

interface SignInResponse {
  detail: string;
}
@Injectable({
  providedIn: 'root'
})

export class AuthService {
  private apiUrl = 'http://localhost:8000/api'; // Replace with your Django server URL

  constructor(private http: HttpClient) {}


  signIn(login: string, password: string): Observable<SignInResponse> {
    return this.http.post<SignInResponse>(`${this.apiUrl}/signin/`, { login, password }).pipe(
      tap(response => {
        if (response.detail === 'Successfully signed in.') {
          document.cookie = 'csrftoken=true'; // Set the csrftoken cookie
        }
      })
    );
  }
  isLoggedIn(): boolean {
    return this.getCookie('csrftoken') !== null;
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
