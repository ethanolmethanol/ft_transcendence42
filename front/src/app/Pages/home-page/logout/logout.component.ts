import { Component } from '@angular/core';
import {LogoutService} from "../../../services/log-out/log-out.service";
import {routes} from "../../../app.routes";
import {Router} from "@angular/router";

@Component({
  selector: 'app-logout',
  standalone: true,
  imports: [],
  templateUrl: './logout.component.html',
  styleUrl: './logout.component.css'
})
export class LogoutComponent {

  username!: String;
  constructor(private logOutService: LogoutService, private router: Router) {}

  public isLogged(): boolean{
    // this.username = this.headerService.getUsername();
    // return this.logOutService.isLogged();
    return false;
  }
  public logOut(){
    this.logOutService.logout().subscribe(
      response => {
        console.log("Logged out successfully: ", response);
        this.router.navigate(['sign-in']).then(r => console.log("Navigated to login"));
      },
      error => {
        console.error("Error while logging out: ", error);
      }
    );
  }
}
