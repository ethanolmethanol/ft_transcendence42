import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';
import { UserService } from "../services/user/user.service";
import { PLAYING_STATUS } from "../constants";

@Injectable({
  providedIn: 'root'
})
export class EnterGameGuard implements CanActivate {
  constructor(private userService: UserService) {}

  canActivate(): boolean {
    this.userService.updateStatus(PLAYING_STATUS).subscribe();
    return true;
  }
}
