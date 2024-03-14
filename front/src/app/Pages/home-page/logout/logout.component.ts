import { Component } from '@angular/core';
import {LogoutService} from "../../../services/log-out/log-out.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-logout',
  standalone: true,
  imports: [],
  templateUrl: './logout.component.html',
  styleUrl: './logout.component.css'
})
export class LogoutComponent {

  constructor(private logOutService: LogoutService, private router: Router) {}

  logOut() {
    const csrfToken = this.getCookie('csrftoken');
    if (csrfToken) {
      this.logOutService.logout(csrfToken).subscribe();
      console.log('Log out!');
      document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      document.cookie = 'sessionId=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      this.router.navigate(['/sign-in']);
    } else {
      console.error('CSRF token not found');
    }
  }

  private getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop()?.split(';').shift() || null;
    }
    return null;
  }
}
