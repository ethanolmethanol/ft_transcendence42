import {Component, EventEmitter, Output} from '@angular/core';
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
  @Output() scrollToTop = new EventEmitter<void>();

  constructor(private authService: AuthService, private userService: UserService) {}

  onTitleClick(): void {
    this.scrollToTop.emit();
  }

  public logOut() {
    this.authService.logout();
    this.userService.clearUserData();
    const logoutChannel = new BroadcastChannel('logoutChannel');
    logoutChannel.postMessage('logout');
    logoutChannel.close();
  }
}
