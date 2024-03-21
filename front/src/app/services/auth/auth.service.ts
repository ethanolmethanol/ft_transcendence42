import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import {map, Observable, tap} from 'rxjs';

interface SignInResponse {
  detail: string;
}

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  private apiUrl = 'https://localhost:8000/api';
  private isLoggedInStatus: boolean = false;

  constructor(private http: HttpClient) {}

  public signIn(login: string, password: string): Observable<SignInResponse> {
    return this.http.post<SignInResponse>(`${this.apiUrl}/signin/`, { login, password }).pipe(
      tap(() => this.isLoggedInStatus = true)
    );
  }

  public signUp(username: string, email: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/signup/`, { username, email, password });
  }

  public isLoggedIn(): boolean {
    this.checkLoggedInStatus();
    console.log('isLoggedInStatus', this.isLoggedInStatus);
    return this.isLoggedInStatus;
  }

  private checkLoggedInStatus(): void {
    this.http.get(`${this.apiUrl}/is_logged/`, { observe: 'response', withCredentials: true }).pipe(
      map((response: HttpResponse<any>) => response.status === 200)
    ).subscribe(isLoggedIn => {
      this.isLoggedInStatus = isLoggedIn;
    });
  }

}
