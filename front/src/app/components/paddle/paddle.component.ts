import {Component, Input, OnInit} from '@angular/core';
import {GAME_HEIGHT, GAME_WIDTH, PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_X_OFFSET, PADDLE_SPEED} from '../../constants';
import {Position} from '../../interfaces/position.interface';

@Component({
  selector: 'app-paddle',
  standalone: true,
  imports: [],
  templateUrl: './paddle.component.html',
  styleUrl: './paddle.component.css'
})
export class PaddleComponent implements OnInit {
  @Input() id: number = 0;
  width = PADDLE_WIDTH;
  height = PADDLE_HEIGHT;
  offset = this.height / 2;
  gameWidth = GAME_WIDTH;
  gameHeight = GAME_HEIGHT;
  speed = PADDLE_SPEED;
  positionX = 0;
  positionY = (this.gameHeight - PADDLE_HEIGHT) / 2;
  ngOnInit() {
    if (this.id == 1) {
      this.positionX = PADDLE_X_OFFSET;
    } else if (this.id == 2) {
      this.positionX = this.gameWidth - this.width - PADDLE_X_OFFSET;
    }
    console.log(`Paddle ${this.id} initialized:`, this.positionX, this.positionY);
  }

  public updatePaddlePosition(position: Position) {
    this.positionX = position.x;
    this.positionY = position.y;
    console.debug(`Paddle ${this.id} position updated:`, this.positionX, this.positionY);
  }
}
