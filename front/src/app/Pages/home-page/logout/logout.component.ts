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

  public logOut() {
    this.logOutService.logout().subscribe();
    console.log('Log out!');
    this.removeCookie('csrftoken');
    this.removeCookie('sessionId');
    this.router.navigate(['/sign-in']);
  }

  private removeCookie(name: string) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
  }
}
