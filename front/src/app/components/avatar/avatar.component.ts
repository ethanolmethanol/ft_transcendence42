import { Component, OnInit } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule, NgStyle } from "@angular/common"
import { UserService } from "../../services/user/user.service";

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

  constructor(private userService: UserService) {}
  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.loadAvatar();
  }

  private loadAvatar(): void {
    try {
      this.userService.getAvatarUrl().subscribe({
        next: (response: any): void => {
          this.fileUrl = response.url;
          console.log("Avatar url: ", this.fileUrl);
        },
        error: (error: Error) => {
          console.error("Failed to load avatar: ", error);
        }
      });
    }
    catch (error) {
      console.error("Failed to load avatar: ", error);
    }
  }

  public onFileChange(event: any) {
      const file: File = event.target.files[0];

      if (file) {
        this.fileUrl = URL.createObjectURL(file);
        this.userService.setAvatar(file).subscribe({
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
}
