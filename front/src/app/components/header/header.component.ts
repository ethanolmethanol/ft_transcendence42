import { Component } from '@angular/core';
import { RouterLink } from "@angular/router";
import { UserService } from "../../services/user/user.service";
import { AuthService } from "../../services/auth/auth.service";

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    RouterLink,
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {

  constructor(private authService: AuthService, private userService: UserService) {}

  public logOut() {
    this.authService.logout();
    this.userService.clearUserData();
    const logoutChannel = new BroadcastChannel('logoutChannel');
    logoutChannel.postMessage('logout');
    logoutChannel.close();
  }
  constructor(private authService: AuthService, private userService: UserService) {}

  public logOut() {
    this.authService.logout();
    this.userService.clearUserData();
    const logoutChannel = new BroadcastChannel('logoutChannel');
    logoutChannel.postMessage('logout');
    logoutChannel.close();
  }
}
