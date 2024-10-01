import { Component, EventEmitter, Output } from '@angular/core';
import { Router, RouterLink } from "@angular/router";
import { UserService } from "../../services/user/user.service";
import { AuthService } from "../../services/auth/auth.service";
import { NgIf } from "@angular/common";
import { ACCOUNT, GAME, FRIENDS, HOME } from "../../constants";

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    RouterLink,
    NgIf,
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  @Output() scrollToTop = new EventEmitter<void>();
  isDropdownOpen = false;
  protected readonly ACCOUNT = ACCOUNT;
  protected readonly GAME = GAME;
  protected readonly FRIENDS = FRIENDS;
  protected readonly HOME = HOME;

  constructor(private authService: AuthService, private userService: UserService, private router: Router) {}

  onTitleClick(): void {
    this.scrollToTop.emit();
  }

  public logOut() {
    this.authService.logout();
    this.userService.clearUserData();
    const logoutLobby = new BroadcastChannel('logoutLobby');
    logoutLobby.postMessage('logout');
    logoutLobby.close();
  }

  toggleDropdown() {
    this.isDropdownOpen = true;
  }

  unToggleDropdown() {
    this.isDropdownOpen = false;
  }

  selectOption(option: number) {
    const navPages: string[] = ["/account", "/custom", "/friends", "/home"];

    this.router.navigate([navPages[option]]);

    this.isDropdownOpen = false;
  }
}
