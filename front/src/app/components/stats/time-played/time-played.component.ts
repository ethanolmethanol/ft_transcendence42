import {Component, Input} from '@angular/core';
import {ChartModule} from "primeng/chart";

@Component({
  selector: 'app-time-played',
  standalone: true,
  templateUrl: './time-played.component.html',
  styleUrl: './time-played.component.css'
})
export class TimePlayedComponent {
  @Input() timePlayed: string = '';
}
