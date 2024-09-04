import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-player-icon',
  standalone: true,
  imports: [],
  templateUrl: './player-icon.component.html',
  styleUrl: './player-icon.component.css'
})
export class PlayerIconComponent {
  @Input() playerName: string = '';

  constructor() {}
}
