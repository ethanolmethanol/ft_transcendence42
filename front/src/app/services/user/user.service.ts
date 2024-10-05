import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {
  API_USER,
  DEFAULT_COLORS,
  DEFAULT_GAME_COUNTER,
  DEFAULT_SETTINGS,
  DEFAULT_TIME_PLAYED,
  DEFAULT_WIN_DICT
} from "../../constants";
import { Observable } from "rxjs";
import { GameHistoryResponse } from "../../interfaces/game-history-response.interface"
import {GameCounter, Times, User, Wins} from "../../interfaces/user";

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
      game_counter: DEFAULT_GAME_COUNTER,
      win_dict: DEFAULT_WIN_DICT,
      time_played: DEFAULT_TIME_PLAYED,
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
        game_counter: userData.game_counter,
        win_dict: userData.win_dict,
        time_played: userData.time_played,
        color_config: userData.color_config,
        game_settings: userData.game_settings,
      };
      console.log('User data loaded:', this._userData);
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

  public async getUsername(userID: number | null = null): Promise<string> {
    try {
      if (userID === null) {
        return this.getUserData().username;
      }
      const response = await this.http.post<string>(
        `${API_USER}/get_username/`, {"user_id": userID}
      ).toPromise();
      if (!response) {
        throw new Error('No username found');
      }
      return response;
    } catch (error) {
      console.error('Error fetching username:', error);
      throw error;
    }
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

  public getGameCounter(): GameCounter {
    return this.getUserData().game_counter;
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
