import {Component, EventEmitter, Output} from '@angular/core';
import { Router, RouterLink } from "@angular/router";
import { UserService } from "../../services/user/user.service";
import { AuthService } from "../../services/auth/auth.service";
import { NgIf } from "@angular/common";
import { ButtonWithIconComponent } from "../button-with-icon/button-with-icon.component";
import { ACCOUNT, GAME, RULES, FRIENDS } from "../../constants";

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
  protected readonly ACCOUNT = ACCOUNT;
  protected readonly GAME = GAME;
  protected readonly RULES = RULES;
  protected readonly FRIENDS = FRIENDS;

  constructor(private authService: AuthService, private userService: UserService, private router: Router) {}

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
  }

  selectOption(option: number) {
    const navPages: string[] = ["/account", "/custom", "/rules", "/friends"];

    this.router.navigate([navPages[option]]);

    this.isDropdownOpen = false;
  }
}
