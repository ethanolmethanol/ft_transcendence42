import { Component } from '@angular/core';
import {NavigationEnd, Router, RouterOutlet} from '@angular/router';
import {SignInPageComponent} from "./pages/sign-in-page/sign-in-page.component";
import {UserService} from "./services/user/user.service";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, SignInPageComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  constructor(private router: Router, private userService: UserService) {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        if (event.url === '/home') {
          setTimeout(() => {
            this.userService.refreshUserData().then(() => {
              console.log('User data refreshed successfully.');
            }).catch((error) => {
              console.error('Failed to refresh user data:', error);
            });
          }, 500);
        }
      }
    });
  }
}
