import { Component, Input, Output, EventEmitter } from '@angular/core';
import { AvatarComponent } from "../avatar/avatar.component";
import { AVATARS_BUCKET, DEFAULT_AVATAR_URL, MINIO_API } from "../../constants";

@Component({
  selector: 'app-request',
  standalone: true,
  imports: [
    AvatarComponent
  ],
  templateUrl: './request.component.html',
  styleUrl: './request.component.css'
})
export class RequestComponent {
  @Input() friendName: string = "friendName";
  avatarUrl: string = `${MINIO_API}/${AVATARS_BUCKET}/${this.friendName}_avatar.jpg`;
  readonly fallbackUrl: string = DEFAULT_AVATAR_URL;
  @Output() accept = new EventEmitter<{ friendName: string, accept: boolean }>();

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
