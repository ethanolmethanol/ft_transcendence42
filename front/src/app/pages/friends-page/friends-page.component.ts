import { Component, OnInit } from '@angular/core';
import { HeaderComponent } from "../../components/header/header.component";
import { NgIf, NgFor, CommonModule } from "@angular/common"
import { FriendSearchComponent } from "../../components/friend-search/friend-search.component";
import { FriendService } from "../../services/friend/friend.service";
import { RequestComponent } from "../../components/request/request.component";
import { Observable } from 'rxjs';
import { AvatarComponent } from "../../components/avatar/avatar.component";
import { FriendCardComponent } from "../../components/friend-card/friend-card.component";
import { PLAYING, ONLINE, OFFLINE } from "../../constants";
import {FriendBoxComponent} from "../../components/friend-box/friend-box.component";

@Component({
  selector: 'app-friends-page',
  standalone: true,
  imports: [
    HeaderComponent,
    NgIf,
    NgFor,
    FriendSearchComponent,
    RequestComponent,
    AvatarComponent,
    CommonModule,
    FriendCardComponent,
    FriendBoxComponent,
  ],
  templateUrl: './friends-page.component.html',
  styleUrl: './friends-page.component.css'
})
export class FriendsPageComponent implements OnInit {
  friendData$: Observable<any>;

  constructor(private friendService: FriendService) {
    this.friendData$ = this.friendService.friendsData$; // Replace with the actual observable
  }

  ngOnInit(): void {
    this.friendData$ = this.friendService.friendsData$;

    this.friendService.refreshFriendData().subscribe({
      next: () => console.log('Friend data refreshed on init'),
      error: err => console.error('Failed to refresh friend data on init', err)
    });
  }

  async acceptOrDecline(event: { friendName: string, accept: boolean }): Promise<void> {
    const { friendName, accept } = event;

    if (accept) {
      this.friendService.acceptFriendship(friendName).subscribe({
        next: () => console.log(`Accepted friendship with ${friendName}`),
        error: err => console.error('Error accepting friendship:', err)
      });
    } else {
      this.friendService.declineFriendship(friendName).subscribe({
        next: () => console.log(`Declined friendship with ${friendName}`),
        error: err => console.error('Error declining friendship:', err)
      });
    }
  }

  protected readonly ONLINE = ONLINE;
  protected readonly PLAYING = PLAYING;
  protected readonly OFFLINE = OFFLINE;
}
