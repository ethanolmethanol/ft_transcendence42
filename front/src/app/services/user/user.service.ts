import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import {catchError, map, Observable, of} from 'rxjs';
import { Router } from "@angular/router";
import {API_USER} from "../../constants";

@Injectable({
  providedIn: 'root'
})

export class UserService {
  constructor(private http: HttpClient) {}

  public getUsername(): Observable<any> {
    return this.http.get<any>(`${API_USER}/username/`);
  }

}
