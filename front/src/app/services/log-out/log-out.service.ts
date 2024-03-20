import { Injectable } from '@angular/core';
import {Router} from "@angular/router";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import { Observable } from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class LogoutService {

  private apiUrl = 'http://localhost:8000/api';

  constructor(private router: Router, private http: HttpClient) {}

  public logout(): Observable<any> {
    // Make the HTTP request with the headers
    return this.http.post(`${this.apiUrl}/logout/`, {}, { withCredentials: true });
  }
}
