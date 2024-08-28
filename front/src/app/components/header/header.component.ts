import {Component, EventEmitter, Output} from '@angular/core';
import { RouterLink } from "@angular/router";
import { UserService } from "../../services/user/user.service";
import { AuthService } from "../../services/auth/auth.service";
import { NgIf } from "@angular/common";
import { ButtonWithIconComponent } from "../button-with-icon/button-with-icon.component";

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    RouterLink,
    NgIf,
    ButtonWithIconComponent,
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  @Output() scrollToTop = new EventEmitter<void>();
  isDropdownOpen = false;

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

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
    console.log("isDropdownOpen: ", this.isDropdownOpen);
  }

  selectOption(option: string) {
    console.log('Selected option:', option);
    this.isDropdownOpen = false;
  }
}
