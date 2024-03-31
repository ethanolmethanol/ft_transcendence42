import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import {catchError, map, Observable, of} from 'rxjs';
import { Router } from "@angular/router";

@Injectable({
  providedIn: 'root'
})

export class UserService {
  private apiUrl = 'https://localhost:8002/user';

  constructor(private http: HttpClient, private router: Router) {}

  public getUsername(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/username/`);
  }

}
