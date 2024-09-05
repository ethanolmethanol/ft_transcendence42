import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { catchError, map, Observable, of } from 'rxjs';
import { Router } from "@angular/router";
import { API_FRIENDS } from "../../constants";

interface FriendsInfo {
  requests: string[];
  playing: string[];
  online: string[];
  offline: string[];
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
      requests: [],
      playing: [],
      online: [],
      offline: [],
    };
  }
  public async refreshFriendData(): Promise<void> {
    try {
      const friendData = await this.http.get<any>(`${API_FRIENDS}/get_friends_info/`).toPromise();
      if (!friendData) {
        throw new Error('No friend data found');
      }
      this._friendsData = friendData;
      // console.log('Friend data refreshed:', this._friendsData);
    } catch (error) {
      console.error('Error refreshing friend data:', error);
    }
  }

  public async whenFriendDataLoaded(): Promise<void> {
    if (!this._friendsDataLoaded) {
      console.log('Loading user data -> send request')
      this._friendsDataLoaded = this.refreshFriendData();
      await this._friendsDataLoaded;
      // console.log('Friend data loaded:', this._friendsData);
    }
    return this._friendsDataLoaded;
  }

  private getFriendData(): FriendsInfo {
    return this._friendsData!;
  }

  public getFriendsRequests(): string[] {
    return this.getFriendData().requests;
  }

  public getPlayingFriends(): string[] {
    return this.getFriendData().playing;
  }

  public getOnlineFriends(): string[] {
    return this.getFriendData().online;
  }

  public getOfflineFriends(): string[] {
    return this.getFriendData().offline;
  }

  public addFriend(friendName: string): Observable<any> {
    this.getFriendData().requests = this.getFriendsRequests().filter(friend => friend !== friendName);
    return this.http.post<any>(`${API_FRIENDS}/add_friend/`, { friendName });
  }

  public acceptFriendship(friendName: string): Observable<any> {
    return this.http.post<any>(`${API_FRIENDS}/accept_friendship/`, { friendName });
  }

  public declineFriendship(friendName: string): Observable<any> {
    return this.http.post<any>(`${API_FRIENDS}/decline_friendship/`, { friendName });
  }
}
