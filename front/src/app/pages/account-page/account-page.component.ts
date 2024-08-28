import { Component, OnInit } from '@angular/core';
import { AvatarComponent } from "../../components/avatar/avatar.component";
import { HeaderComponent } from "../../components/header/header.component";
import { UserService } from "../../services/user/user.service";

@Component({
  selector: 'app-account-page',
  standalone: true,
  imports: [
    AvatarComponent,
    HeaderComponent,
  ],
  templateUrl: './account-page.component.html',
  styleUrl: './account-page.component.css'
})
export class AccountPageComponent implements OnInit {
  username: string = "";

  constructor(private userService: UserService) {}

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.username = this.userService.getUsername();
  }

  public updateUsername() {}

  public deleteAccount() {}
}
