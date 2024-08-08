import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import {catchError, map, Observable, of} from 'rxjs';
import { Router } from "@angular/router";
import { API_AUTH } from "../../constants";
import * as CryptoJS from 'crypto-js';

interface SignInResponse {
  detail: string;
}

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  constructor(private http: HttpClient, private router: Router) {}

  public signIn(login: string, password: string): Observable<SignInResponse> {
    const hashedPassword = CryptoJS.SHA256(password).toString();
    return this.http.post<SignInResponse>(`${API_AUTH}/signin/`, { login, password: hashedPassword });
  }

  public signUp(username: string, email: string, password: string): Observable<any> {
    const hashedPassword = CryptoJS.SHA256(password).toString();
    console.log(`Hash password: ${hashedPassword}`)
    return this.http.post(`${API_AUTH}/signup/`, { username, email, password: hashedPassword });
  }

  public isLoggedIn(): Observable<boolean> {
    return this.http.get(`${API_AUTH}/is_logged/`, { observe: 'response' }).pipe(
      map((response: HttpResponse<any>) => {
        return (response.status === 200);
      }),
      catchError((error) => {
        console.error('Error checking login status', error);
        return of(false);
      })
    );
  }

  public logout(): void {
    this.processLogout().subscribe(() => {
      this.router.navigate(['/sign-in']);
    });
  }

  private processLogout() {
    return this.http.post(`${API_AUTH}/logout/`, {});
  }
}
