import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http'
import { MatIconModule } from '@angular/material/icon';
import { CommonModule, NgStyle } from "@angular/common"
import { UserService } from "../../services/user/user.service";
import { MINIO_API, AVATARS_BUCKET, DEFAULT_AVATAR_URL} from "../../constants"

@Component({
  selector: 'app-avatar',
  standalone: true,
  imports: [
    MatIconModule,
    CommonModule,
    NgStyle,
  ],
  templateUrl: './avatar.component.html',
  styleUrl: './avatar.component.css'
})
export class AvatarComponent implements OnInit {
  public  fileUrl: string = "";
  private  fallbackUrl: string = DEFAULT_AVATAR_URL;

  constructor(private userService: UserService, private http: HttpClient) {}

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.loadAvatar();
  }

  private loadAvatar(): void {
    const userID: string = String(this.userService.getUserID());
    this.fileUrl =  `${MINIO_API}/${AVATARS_BUCKET}/${userID}_avatar.jpg`;
  }

  public onFileChange(event: any) {
      const file: File = event.target.files[0];

      if (file) {
        this.fileUrl = URL.createObjectURL(file);
        this.userService.updateAvatar(file).subscribe({
          next: (response: any): void => {
            console.log(response);
          },
          error: (error: Error) => {
            console.error("Failed to load avatar: ", error);
          }
        });
      }
      this.resetInput();
  }

  private resetInput(){
    const input: HTMLInputElement = document.getElementById('avatar-input-file') as HTMLInputElement;
    if(input){
      input.value = "";
    }
  }

  public onImageError(event: Event) {
    console.log('Image failed to load, using fallback URL.');
    (event.target as HTMLImageElement).src = this.fallbackUrl;
  }
}
