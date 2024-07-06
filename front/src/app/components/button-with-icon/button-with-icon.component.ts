import {Component, Input} from '@angular/core';
import {RouterLink} from "@angular/router";

@Component({
  selector: 'app-button-with-icon',
  standalone: true,
  imports: [
    RouterLink
  ],
  templateUrl: './button-with-icon.component.html',
  styleUrl: './button-with-icon.component.css'
})
export class ButtonWithIconComponent {

  @Input() title: string = '';
  @Input() link: string = '/';
  @Input() icon: string = '';

  constructor() { }
}
