import { Component } from '@angular/core';
import { HeaderComponent } from "../../components/header/header.component";
import { NgIf } from "@angular/common"
import {FriendSearchComponent} from "../../components/friend-search/friend-search.component";

@Component({
  selector: 'app-friends-page',
  standalone: true,
  imports: [
    HeaderComponent,
    NgIf,
    FriendSearchComponent
  ],
  templateUrl: './friends-page.component.html',
  styleUrl: './friends-page.component.css'
})
export class FriendsPageComponent {
  friend_requests: string[] = [];
  playing_friends: string[] = [];
  online_friends: string[] = [];
  offline_friends: string[] = [];

}
