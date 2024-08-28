import { Component } from '@angular/core';
import { AvatarComponent } from "../../components/avatar/avatar.component";
import { HeaderComponent } from "../../components/header/header.component";

@Component({
  selector: 'app-account-page',
  standalone: true,
  imports: [
    AvatarComponent,
    HeaderComponent
  ],
  templateUrl: './account-page.component.html',
  styleUrl: './account-page.component.css'
})
export class AccountPageComponent {

}
