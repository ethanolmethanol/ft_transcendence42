import { Component } from '@angular/core';
import { SignUpComponent } from "../../components/sign-up/sign-up.component";
import { RouterLink } from "@angular/router";

@Component({
  selector: 'app-sign-up-page',
  standalone: true,
  imports: [
    SignUpComponent,
    RouterLink,
  ],
  templateUrl: './sign-up-page.component.html',
  styleUrl: './sign-up-page.component.css'
})
export class SignUpPageComponent {

}
