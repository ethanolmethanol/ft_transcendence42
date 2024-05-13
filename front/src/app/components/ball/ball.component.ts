import {Component, Input} from '@angular/core';
import {BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH} from "../../constants";
import {Position} from "../../interfaces/position.interface";

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
  @Input() ballSize = BALL_RADIUS * 2;

  public updateBallPosition(position: Position) {
    this.positionX = Math.max(0, Math.min(position.x, GAME_WIDTH));
    this.positionY = Math.max(0, Math.min(position.y, GAME_HEIGHT));
  }
}
