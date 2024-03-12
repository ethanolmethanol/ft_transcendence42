import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {SignInPageComponent} from "./Pages/sign-in-page/sign-in-page.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, SignInPageComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'transcendence';
}
