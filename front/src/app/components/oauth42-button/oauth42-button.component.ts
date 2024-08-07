import { Component, Input } from '@angular/core';
import { API_42_REDIRECT_URL } from "../../constants";

@Component({
  selector: 'app-oauth42-button',
  standalone: true,
  imports: [],
  templateUrl: './oauth42-button.component.html',
  styleUrl: './oauth42-button.component.css'
})
export class Oauth42ButtonComponent {
  @Input() text: string = "";

  public navigate_to_42_api(): void {
    window.open(API_42_REDIRECT_URL, '_self');
  }
}
