import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { catchError, map, Observable, of } from 'rxjs';
import { Router } from "@angular/router";
import {API_FRIENDS, API_USER} from "../../constants";

interface FriendsInfo {
  friend_requests: string[];
  playing_friends: string[];
  online_friends: string[];
  offline_friends: string[];
}

@Injectable({
  providedIn: 'root'
})
export class FriendService {
  private _friendsData: FriendsInfo | null;
  private _friendsDataLoaded: Promise<void> | null;

  constructor(private http: HttpClient) {
    this._friendsDataLoaded = null;
    this._friendsData = {
      friend_requests: [],
      playing_friends: [],
      online_friends: [],
      offline_friends: [],
    };
  }
  public async refreshFriendData(): Promise<void> {
    try {
      const friendData = await this.http.get<any>(`${API_FRIENDS}/get_friends_info/`).toPromise();
      if (!friendData) {
        throw new Error('No friend data found');
      }
      this._friendsData = {
        friend_requests: friendData.friend_requests,
        playing_friends: friendData.playing_friends,
        online_friends: friendData.online_friends,
        offline_friends: friendData.offline_friends,
      };
      console.log('Friend data loaded:', this._friendsData);
    } catch (error) {
      console.error('Error loading friend data:', error);
    }
  }

  private async saveFriendData(): Promise<void> {
    try {
      await this.http.post(`${API_FRIENDS}/user_data/`, this._friendsData).toPromise();
    } catch (error) {
      console.error('Error saving user data:', error);
    }
  }

  public whenFriendDataLoaded(): Promise<void> {
    if (!this._friendsDataLoaded) {
      console.log('Loading user data -> send request')
      this._friendsDataLoaded = this.refreshFriendData();
    }
    return this._friendsDataLoaded;
  }

  private getFriendData(): FriendsInfo {
    return this._friendsData!;
  }

  public getFriendsRequests(): string[] {
    return this.getFriendData().friend_requests;
  }

  public getPlayingFriends(): string[] {
    return this.getFriendData().playing_friends;
  }

  public getOnlineFriends(): string[] {
    return this.getFriendData().online_friends;
  }

  public getOfflineFriends(): string[] {
    return this.getFriendData().offline_friends;
  }

  public addFriend(friendName: string): Observable<any> {
    return this.http.post<any>(`${API_FRIENDS}/add_friend/`, { friendName });
  }
}
