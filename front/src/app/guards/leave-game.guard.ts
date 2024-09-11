import { Injectable } from '@angular/core';
import { CanDeactivate } from '@angular/router';
import { UserService } from "../services/user/user.service";
import { ONLINE_STATUS } from "../constants";

@Injectable({
  providedIn: 'root'
})
export class LeaveGameGuard implements CanDeactivate<any> {
  constructor(private userService: UserService) {}

  canDeactivate(): boolean {
    this.userService.updateStatus(ONLINE_STATUS).subscribe();
    return true;
  }
}
