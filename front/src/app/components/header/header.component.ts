import { Component } from '@angular/core';
import {RouterLink} from "@angular/router";
import {LogoutComponent} from "../logout/logout.component";

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    RouterLink,
    LogoutComponent
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {

}
