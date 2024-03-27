import {Component, Input} from '@angular/core';
import {BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH} from "../../constants";

@Component({
  selector: 'app-ball',
  standalone: true,
  imports: [],
  templateUrl: './ball.component.html',
  styleUrl: './ball.component.css'
})
export class BallComponent {
  @Input() positionX: number = 150;
  @Input() positionY: number = 150;
  protected readonly ballSize = BALL_RADIUS * 2;

  constructor() {
    this.updatePosition(this.positionX, this.positionY);
  }

  updatePosition(x: number, y: number) {
    this.positionX = Math.max(0, Math.min(x, GAME_WIDTH));
    this.positionY = Math.max(0, Math.min(y, GAME_HEIGHT));
  }
}
