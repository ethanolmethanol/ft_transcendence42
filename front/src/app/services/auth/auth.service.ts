import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import {catchError, map, Observable, of} from 'rxjs';
import { Router } from "@angular/router";
import { API_AUTH } from "../../constants";
// import { OAuthService } from 'angular-oauth-oidc';
interface SignInResponse {
  detail: string;
}

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  constructor(private http: HttpClient, private router: Router) {}

  public signIn(login: string, password: string): Observable<SignInResponse> {
    return this.http.post<SignInResponse>(`${API_AUTH}/signin/`, { login, password });
  }

  // public signIn42() {
  //   this.oauthService.initCodeFlow();
  // }

  public signUp(username: string, email: string, password: string): Observable<any> {
    return this.http.post(`${API_AUTH}/signup/`, { username, email, password });
  }

  // public signUp42() {
  //   this.oauthService.initCodeFlow();
  // }

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

  // public logout42() {
  //   this.oauthService.logOut();
  // }

  private processLogout() {
    return this.http.post(`${API_AUTH}/logout/`, {});
  }
}
