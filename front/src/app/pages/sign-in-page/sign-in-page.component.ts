import { Component } from '@angular/core';
import {SignInComponent} from "../../components/sign-in/sign-in.component";
import {RouterLink} from "@angular/router";
@Component({
  selector: 'app-sign-in-page',
  standalone: true,
  imports: [
    SignInComponent,
    RouterLink,
  ],
  templateUrl: './sign-in-page.component.html',
  styleUrls: ['./sign-in-page.component.css']
})
export class SignInPageComponent {

}
