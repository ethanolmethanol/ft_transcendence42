import { Component } from '@angular/core';
import {SignInComponent} from "../../sign-in/sign-in.component";
@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [
    SignInComponent
  ],
  templateUrl: './login-page.component.html',
  styleUrl: './login-page.component.css'
})
export class LoginPageComponent {

}
