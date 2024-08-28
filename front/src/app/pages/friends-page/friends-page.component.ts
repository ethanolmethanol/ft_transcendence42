import { Component } from '@angular/core';
import {HeaderComponent} from "../../components/header/header.component";

@Component({
  selector: 'app-friends-page',
  standalone: true,
  imports: [
    HeaderComponent
  ],
  templateUrl: './friends-page.component.html',
  styleUrl: './friends-page.component.css'
})
export class FriendsPageComponent {

}
