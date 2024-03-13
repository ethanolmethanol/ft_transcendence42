import { Component } from '@angular/core';
import {LogoutComponent} from "./logout/logout.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    LogoutComponent
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {

}
