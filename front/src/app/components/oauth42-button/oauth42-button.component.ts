import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-oauth42-button',
  standalone: true,
  imports: [],
  templateUrl: './oauth42-button.component.html',
  styleUrl: './oauth42-button.component.css'
})
export class Oauth42ButtonComponent {
  @Input() text: string = "";
}
