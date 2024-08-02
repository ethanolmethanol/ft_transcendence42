import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {API_USER, DEFAULT_COLORS, DEFAULT_SETTINGS} from "../../constants";
import { Observable } from "rxjs";
import { GameHistoryResponse } from "../../interfaces/game-history-response.interface"

interface User {
  id: number;
  username: string;
  email: string;
  color_config: string[];
  game_settings: number[];
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private _userData: any;
  private _userDataLoaded: Promise<void> | null;

  constructor(private http: HttpClient) {
    this._userDataLoaded = null;
    this._userData = {
      id: -1,
      username: '',
      email: '',
      color_config: DEFAULT_COLORS,
      game_settings: DEFAULT_SETTINGS,
    };
  }

  private async loadUserData(): Promise<void> {
    try {
      const userData = await this.http.get<User>(`${API_USER}/user_data/`).toPromise();
      if (!userData) {
        throw new Error('No user data found');
      }
      this._userData = {
        id: Object.freeze(userData.id),
        email: Object.freeze(userData.email),
        username: Object.freeze(userData.username),
        color_config: userData.color_config,
        game_settings: Object.freeze(userData.game_settings),
      };
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  }

  private async saveUserData(): Promise<void> {
    try {
      await this.http.post(`${API_USER}/user_data/`, this._userData).toPromise();
    } catch (error) {
      console.error('Error saving user data:', error);
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

  public getColorConfig(): string[] {
    return this.getUserData().color_config;
  }

  public setColorConfig(colors: string[]): void {
    this.getUserData().color_config = colors;
    this.saveUserData();
  }

  public getGameSettings(): number[] {
    return this.getUserData().game_settings;
  }

  public setGameSettings(settings: number[]): void {
    this.getUserData().game_settings = settings;
    this.saveUserData();
  }

  public clearUserData(): void {
    this._userData = null;
    this._userDataLoaded = null;
  }

  public getSummaries(startIndex: number, endIndex: number): Observable<GameHistoryResponse> {
    const postData: string = JSON.stringify({'user_id': this.getUserID(), 'start_index': startIndex, 'end_index': endIndex});
    return this.http.post<GameHistoryResponse>(`${API_USER}/get_game_summaries/`, postData);
  }
}
