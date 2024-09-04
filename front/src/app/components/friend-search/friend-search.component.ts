import { Component, OnInit } from '@angular/core';
import { ErrorMessageComponent } from "../error-message/error-message.component";
import { FormsModule } from '@angular/forms';
import { ERROR_MESSAGE, INFO_MESSAGE } from "../../constants";
import { CommonModule } from '@angular/common';
import { FriendService } from "../../services/friend/friend.service";
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-friend-search',
  standalone: true,
  imports: [
    ErrorMessageComponent,
    FormsModule,
    CommonModule,
  ],
  templateUrl: './friend-search.component.html',
  styleUrl: './friend-search.component.css'
})
export class FriendSearchComponent implements OnInit {
  friendName: string = "";
  message: string = "";
  messageClass: string = "";

  constructor(private friendService: FriendService) {}

  async ngOnInit(): Promise<void> {
    await this.friendService.whenFriendDataLoaded();
  }

  sendFriendRequest() {
    this.clearMessage();
    // send a friend request
    this.friendService.addFriend(this.friendName).subscribe({
      next: (response: any): void => {
        const message: string = response.status;
        console.log(message);
        this.showMessage(message, INFO_MESSAGE);
      },
      error: (error: HttpErrorResponse) => {
        console.error("Failed to send friend request: ", error);
        this.showMessage(error.error?.error || "An unknown error occurred.", ERROR_MESSAGE);
      }
    });
  }

  private clearMessage() {
    this.message = "";
    this.messageClass = "";
  }

  private showMessage(messageText: string, messageType: string) {
    this.message = messageText;
    this.messageClass = messageType + " show";

    setTimeout(() => {
      this.messageClass = messageType + " hide";
      setTimeout(() => this.message = "", 500); // Remove message after fading out
    }, 1000); // Display message for 1 second
  }
}
