import { Injectable } from '@angular/core';
import {Router} from "@angular/router";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable, of} from "rxjs";
import {AuthService} from "../auth/auth.service";

@Injectable({
  providedIn: 'root'
})
export class LogoutService {

  private apiUrl = 'http://localhost:8000/api';

  constructor(private router: Router, private http: HttpClient, private authService: AuthService) {}

  public logout(csrfToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken,
    });
    return this.http.post(`${this.apiUrl}/logout/`, {}, {headers});
  }
}
