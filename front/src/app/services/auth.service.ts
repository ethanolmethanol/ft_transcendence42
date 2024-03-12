import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  private apiUrl = 'http://localhost:8000/api'; // Replace with your Django server URL

  constructor(private http: HttpClient) {}

  signIn(login: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/signin/`, { login, password });
  }
}
