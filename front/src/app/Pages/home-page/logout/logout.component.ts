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
    this.logOutService.logout();
    console.log('Log out!');
    this.router.navigate(['/sign-in']);
  }
}
