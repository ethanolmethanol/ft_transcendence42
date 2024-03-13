import { Injectable } from '@angular/core';
import {Router} from "@angular/router";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {catchError, Observable, of} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class LogoutService {

  private apiUrl = 'http://localhost:8000/api';

  constructor(private router: Router, private http: HttpClient) {}

  public logout(csrfToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken,
    });

    const res = this.http.post(`${this.apiUrl}/logout/`, {}, {headers});
    this.removeCookie('csrftoken');
    return res;
  }

  private removeCookie(name: string): void {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  }

}
