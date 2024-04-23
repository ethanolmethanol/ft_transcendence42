import { Component, Input } from '@angular/core';
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-gameover',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './gameover.component.html',
  styleUrl: './gameover.component.css'
})
export class GameOverComponent {
  @Input() show: boolean = false;
  @Input() message: string = "";
}
