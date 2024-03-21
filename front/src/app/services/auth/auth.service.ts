import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { Router } from "@angular/router";

interface SignInResponse {
  detail: string;
}

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  private apiUrl = 'https://localhost:8000/api';

  constructor(private http: HttpClient, private router: Router) {}

  public signIn(login: string, password: string): Observable<SignInResponse> {
    return this.http.post<SignInResponse>(`${this.apiUrl}/signin/`, { login, password });
  }

  public signUp(username: string, email: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/signup/`, { username, email, password });
  }

  public isLoggedIn(): Observable<boolean> {
    return this.http.get(`${this.apiUrl}/is_logged/`, { observe: 'response' }).pipe(
      map((response: HttpResponse<any>) => response.status === 200)
    );
  }

  public logout(): void {
    this.processLogout().subscribe();
    this.router.navigate(['sign-in']);
  }

  private processLogout() {
    return this.http.post(`${this.apiUrl}/logout/`, {});
  }
}
