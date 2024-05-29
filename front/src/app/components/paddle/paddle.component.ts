import {Component, Input, OnInit} from '@angular/core';
import {GAME_HEIGHT, GAME_WIDTH, PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_X_OFFSET, PADDLE_SPEED} from '../../constants';
import {Position} from '../../interfaces/position.interface';
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-paddle',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './paddle.component.html',
  styleUrl: './paddle.component.css'
})
export class PaddleComponent {
  @Input() id: number = 0;
  playerName: string = '';
  width = PADDLE_WIDTH;
  height = PADDLE_HEIGHT;
  positionX = 0;
  positionY = 0;
  afkLeftTime : number | null = null;

  public updatePaddlePosition(position: Position) {
    this.positionX = position.x;
    this.positionY = position.y;
    console.debug(`Paddle ${this.id} position updated:`, this.positionX, this.positionY);
  }
}
