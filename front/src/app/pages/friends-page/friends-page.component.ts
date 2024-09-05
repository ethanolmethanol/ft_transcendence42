import { Component, OnInit } from '@angular/core';
import { HeaderComponent } from "../../components/header/header.component";
import { NgIf, NgFor } from "@angular/common"
import { FriendSearchComponent } from "../../components/friend-search/friend-search.component";
import { FriendService } from "../../services/friend/friend.service";
import { RequestComponent } from "../../components/request/request.component";

@Component({
  selector: 'app-friends-page',
  standalone: true,
  imports: [
    HeaderComponent,
    NgIf,
    NgFor,
    FriendSearchComponent,
    RequestComponent,
  ],
  templateUrl: './friends-page.component.html',
  styleUrl: './friends-page.component.css'
})
export class FriendsPageComponent implements OnInit {
  friend_requests: string[] = [];
  playing_friends: string[] = [];
  online_friends: string[] = [];
  offline_friends: string[] = [];

  constructor(private friendService: FriendService) {}

  async ngOnInit(): Promise<void> {
    await this.friendService.whenFriendDataLoaded();
    this.setFriendsData();
  }

  async acceptRequest(event: { friendName: string, accept: boolean }): Promise<void> {
    const { friendName, accept } = event;

    if (accept)
      await this.acceptFriendship(friendName);
    else
      await this.declineFriendship(friendName);
    this.friend_requests = this.friend_requests.filter(friend => friend !== friendName);
  }

  private async refreshFriendData(): Promise<void> {
    this.friendService.refreshFriendData().then(() => {
      console.log('Friend data refreshed successfully.');
    }).catch((error) => {
      console.error('Failed to refresh friend data:', error);
    })
  }

  private setFriendsData(): void {
    this.friend_requests = this.friendService.getFriendsRequests();
    this.playing_friends = this.friendService.getPlayingFriends();
    this.online_friends = this.friendService.getOnlineFriends();
    this.offline_friends = this.friendService.getOfflineFriends();
  }

  public async acceptFriendship(friendName: string): Promise<void> {
    try {
      const response = await this.friendService.acceptFriendship(friendName).toPromise();
      console.log(response.status);
    } catch (error) {
      console.error("Failed to send friend request: ", error);
    }
  }

  public async declineFriendship(friendName: string): Promise<void> {
    try {
      const response = await this.friendService.declineFriendship(friendName).toPromise();
      console.log(response.status);
    } catch (error) {
      console.error("Failed to send friend request: ", error);
    }
  }
}
