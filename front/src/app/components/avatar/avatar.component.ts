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
  public  fileUrl: string = DEFAULT_AVATAR_URL;
  private  isAvatarSet: boolean = false;

  constructor(private userService: UserService, private http: HttpClient) {}

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.loadAvatar();
  }

  private loadAvatar(): void {
    const user_id: string = String(this.userService.getUserID());
    const new_url: string = `${MINIO_API}/${AVATARS_BUCKET}/${user_id}_avatar.jpg`

    if (!this.isAvatarSet)
      this.fileUrl = new_url;
  }

  public onFileChange(event: any) {
      const file: File = event.target.files[0];

      if (file) {
        this.fileUrl = URL.createObjectURL(file);
        this.userService.updateAvatar(file).subscribe({
          next: (response: any): void => {
            console.log(response);
            this.isAvatarSet = true;
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
}
