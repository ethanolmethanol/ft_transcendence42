import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { AvatarComponent } from "../avatar/avatar.component";
import { UserService } from "../../services/user/user.service";
import { AVATARS_BUCKET, DEFAULT_AVATAR_URL, MINIO_API } from "../../constants";
import { FriendService } from "../../services/friend/friend.service";

@Component({
  selector: 'app-request',
  standalone: true,
  imports: [
    AvatarComponent
  ],
  templateUrl: './request.component.html',
  styleUrl: './request.component.css'
})
export class RequestComponent implements OnInit {
  @Input() friendName: string = "friendName";
  avatarUrl: string = DEFAULT_AVATAR_URL;
  readonly fallbackUrl: string = DEFAULT_AVATAR_URL;
  @Output() accept = new EventEmitter<{ friendName: string, accept: boolean }>();

  constructor(private userService: UserService, private friendService: FriendService) {}

  async ngOnInit() {
    await this.userService.whenUserDataLoaded();
    await this.friendService.whenFriendDataLoaded();
    this.avatarUrl =  `${MINIO_API}/${AVATARS_BUCKET}/${this.friendName}_avatar.jpg`;
  }

  public onImageError(event: Event) {
    console.log('Image failed to load, using fallback URL.', this.avatarUrl);
    (event.target as HTMLImageElement).src = this.fallbackUrl;
  }

  onAccept() {
    this.accept.emit({ friendName: this.friendName, accept: true });
  }

  onDecline() {
    this.accept.emit({ friendName: this.friendName, accept: false });
  }
}
