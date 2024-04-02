import { Component } from '@angular/core';
import {RouterLink} from "@angular/router";
import {LogoutComponent} from "../logout/logout.component";

@Component({
  selector: 'app-banner',
  standalone: true,
  imports: [
    RouterLink,
    LogoutComponent
  ],
  templateUrl: './banner.component.html',
  styleUrl: './banner.component.css'
})
export class BannerComponent {

}
