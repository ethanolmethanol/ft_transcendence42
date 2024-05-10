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
  private userData: any;
  private userDataLoaded: Promise<void>;

  constructor(private http: HttpClient) {
    this.userDataLoaded = this.loadUserData();
  }

  private async loadUserData(): Promise<void> {
    try {
      this.userData = await this.http.get<User>(`${API_USER}/user_data/`).toPromise();
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  }

  public whenUserDataLoaded(): Promise<void> {
    return this.userDataLoaded;
  }

  private getUserData(): User {
    return this.userData;
  }

  public getUsername(): string {
    return this.getUserData().username;
  }
}
