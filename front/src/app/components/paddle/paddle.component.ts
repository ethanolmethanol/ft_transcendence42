import {Component, Input} from '@angular/core';
import {PADDLE_HEIGHT, PADDLE_WIDTH} from '../../constants';
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
  width: number = PADDLE_WIDTH;
  height: number = PADDLE_HEIGHT;
  positionX: number = 0;
  positionY: number = 0;
  afkLeftTime : number | null = null;

  public updatePaddlePosition(position: Position) {
    this.positionX = position.x;
    this.positionY = position.y;
    console.debug(`Paddle ${this.id} position updated:`, this.positionX, this.positionY);
  }
}
