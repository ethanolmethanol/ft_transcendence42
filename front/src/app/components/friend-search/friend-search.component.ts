import { Component } from '@angular/core';
import { ErrorMessageComponent } from "../error-message/error-message.component";
import { FormsModule } from '@angular/forms';
import { ERROR_MESSAGE, INFO_MESSAGE } from "../../constants";
import { CommonModule } from '@angular/common';

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
export class FriendSearchComponent {
  friendName: string = "";
  message: string = "";
  messageClass: string = "";

  sendFriendRequest() {
    this.clearMessage();
    // send a friend request
    this.showMessage("youpiiii", INFO_MESSAGE);
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
