import { Component, Input } from '@angular/core';
import { AvatarComponent } from "../avatar/avatar.component";
import { FriendService } from "../../services/friend/friend.service";
import { HttpErrorResponse } from '@angular/common/http';
import { ONLINE } from "../../constants";

@Component({
  selector: 'app-friend-card',
  standalone: true,
  imports: [
    AvatarComponent
  ],
  templateUrl: './friend-card.component.html',
  styleUrl: './friend-card.component.css'
})
export class FriendCardComponent {
  @Input() friendName: string = "";
  @Input() friendStatus: number = ONLINE;

  constructor(private friendService: FriendService) {}

  public removeFriend() {
    this.friendService.removeFriend(this.friendName).subscribe({
      next: (response: any): void => {
        const message: string = response.status;
        console.log(message);
        this.friendService.refreshFriendData().subscribe();
      },
      error: (error: HttpErrorResponse) => {
        console.error("Failed to remove friend: ", error);
      }
    });
  }
}
