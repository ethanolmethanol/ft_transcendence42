import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {API_USER, DEFAULT_COLORS, DEFAULT_SETTINGS} from "../../constants";
import { Observable } from "rxjs";
import { GameHistoryResponse } from "../../interfaces/game-history-response.interface"
import {Times, User, Wins} from "../../interfaces/user";

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private _userData: User | null;
  private _userDataLoaded: Promise<void> | null;

  constructor(private http: HttpClient) {
    this._userDataLoaded = null;
    this._userData = {
      id: -1,
      username: '',
      email: '',
      win_dict: {win: 0, loss: 0, tie: 0},
      time_played: {local: 0, remote: 0},
      color_config: DEFAULT_COLORS,
      game_settings: DEFAULT_SETTINGS,
    };
  }

  public async refreshUserData(): Promise<void> {
    try {
      const userData = await this.http.get<User>(`${API_USER}/user_data/`).toPromise();
      if (!userData) {
        throw new Error('No user data found');
      }
      this._userData = {
        id: Object.freeze(userData.id),
        email: Object.freeze(userData.email),
        username: Object.freeze(userData.username),
        win_dict: userData.win_dict,
        time_played: userData.time_played,
        color_config: userData.color_config,
        game_settings: userData.game_settings,
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
      console.log('Loading user data -> send request')
      this._userDataLoaded = this.refreshUserData();
    }
    return this._userDataLoaded;
  }

  private getUserData(): User {
    return this._userData!;
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

  public getTimePlayed(): Times {
    return this.getUserData().time_played;
  }

  public getWinDict(): Wins {
    return this.getUserData().win_dict;
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

  public async getUser(userID: number): Promise<User> {
    try {
      const userData = await this.http.get<User>(`${API_USER}/user_data/${userID}`).toPromise();
      if (!userData) {
        throw new Error('No user data found');
      }
      return userData;
    } catch (error) {
      console.error('Error fetching user data:', error);
      throw error;
    }
  }

  public getSummaries(startIndex: number, endIndex: number, filter: string): Observable<GameHistoryResponse> {
    const postData: string = JSON.stringify({'user_id': this.getUserID(), 'start_index': startIndex, 'end_index': endIndex, filter: filter});
    return this.http.post<GameHistoryResponse>(`${API_USER}/get_game_summaries/`, postData);
  }
}
