import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-time-played',
  standalone: true,
  templateUrl: './time-played.component.html',
  styleUrl: './time-played.component.css'
})
export class TimePlayedComponent {
  @Input() timePlayed: { local: string, remote: string } = { local: '0', remote: '0' };
}
