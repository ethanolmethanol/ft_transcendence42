import { Component } from '@angular/core';
import {AuthService} from "../../services/auth/auth.service";
import { UserService } from '../../services/user/user.service';
import { WebSocketService } from '../../services/web-socket/web-socket.service';

@Component({
  selector: 'app-logout',
  standalone: true,
  imports: [],
  templateUrl: './logout.component.html',
  styleUrl: './logout.component.css'
})
export class LogoutComponent {

  constructor(private authService: AuthService, private userService: UserService) {}

  public logOut() {
    this.authService.logout();
    this.userService.clearUserData();
  }
}
