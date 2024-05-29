import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import {API_USER} from "../../constants";

interface User {
  id: number;
  username: string;
  email: string;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private _userData: any;
  private _userDataLoaded: Promise<void> | null;

  constructor(private http: HttpClient) {
    this._userDataLoaded = null;
  }

  private async loadUserData(): Promise<void> {
    try {
      this._userData = await this.http.get<User>(`${API_USER}/user_data/`).toPromise();
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  }

  public whenUserDataLoaded(): Promise<void> {
    if (!this._userDataLoaded) {
      this._userDataLoaded = this.loadUserData();
    }
    return this._userDataLoaded;
  }

  private getUserData(): User {
    return this._userData;
  }

  public getUsername(): string {
    return this.getUserData().username;
  }

  public getUserID(): number {
    return this.getUserData().id;
  }

  public clearUserData(): void {
    this._userData = null;
    this._userDataLoaded = null;
  }
}
