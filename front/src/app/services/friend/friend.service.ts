import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
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
  private _friendsDataSubject = new BehaviorSubject<FriendsInfo>({
    requests: [],
    playing: [],
    online: [],
    offline: []
  });

  constructor(private http: HttpClient) {}

  public get friendsData$(): Observable<FriendsInfo> {
    return this._friendsDataSubject.asObservable();
  }

  public refreshFriendData(): Observable<FriendsInfo> {
    return this.http.get<FriendsInfo>(`${API_FRIENDS}/get_friends_info/`).pipe(
      tap((friendData: FriendsInfo) => {
        this._friendsDataSubject.next(friendData);
      })
    );
  }

  public addFriend(friendName: string): Observable<any> {
    return this.http.post<any>(`${API_FRIENDS}/add_friend/`, { friendName });
  }

  public acceptFriendship(friendName: string): Observable<any> {
    return this.http.post<any>(`${API_FRIENDS}/accept_friendship/`, { friendName }).pipe(
      tap(() => {
        this.refreshFriendData().subscribe();
      })
    );
  }

  public declineFriendship(friendName: string): Observable<any> {
    return this.http.post<any>(`${API_FRIENDS}/decline_friendship/`, { friendName }).pipe(
      tap(() => {
        this.refreshFriendData().subscribe();
      })
    );
  }

  public removeFriend(friendName: string): Observable<any> {
    return this.http.post<any>(`${API_FRIENDS}/remove_friend/`, { friendName }).pipe(
      tap(() => {
        this.refreshFriendData().subscribe();
      })
    );
  }
}
