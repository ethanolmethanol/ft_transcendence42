import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-time-played',
  standalone: true,
  imports: [],
  templateUrl: './time-played.component.html',
  styleUrl: './time-played.component.css'
})
export class TimePlayedComponent {
  @Input() timePlayed: string = '';
}
