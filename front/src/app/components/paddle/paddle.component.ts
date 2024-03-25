import {Component, Input, OnInit} from '@angular/core';
import {GAME_HEIGHT, GAME_WIDTH, PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_X_OFFSET, PADDLE_SPEED} from '../../constants';

@Component({
  selector: 'app-paddle',
  standalone: true,
  imports: [],
  templateUrl: './paddle.component.html',
  styleUrl: './paddle.component.css'
})
export class PaddleComponent implements OnInit {
  @Input() id: number = 0;
  paddleWidth = PADDLE_WIDTH;
  paddleHeight = PADDLE_HEIGHT;
  positionX = 0;
  positionY = (GAME_HEIGHT - PADDLE_HEIGHT) / 2;

  ngOnInit() {
    if (this.id == 1) {
      this.positionX = PADDLE_X_OFFSET;
    } else if (this.id == 2) {
      this.positionX = GAME_WIDTH - 2 * PADDLE_WIDTH - PADDLE_X_OFFSET;
    }
    console.log(`Paddle ${this.id} initialized:`, this.positionX, this.positionY);
  }

  moveUp() {
    if (this.positionY - PADDLE_SPEED >= 0) {
      this.positionY -= PADDLE_SPEED; // Move the paddle up
      this.updatePaddlePosition();
    }
  }

  moveDown() {
    if (this.positionY + PADDLE_HEIGHT + PADDLE_SPEED <= GAME_HEIGHT) {
      this.positionY += PADDLE_SPEED; // Move the paddle down
      this.updatePaddlePosition();
    }
  }

  private updatePaddlePosition() {
    // console.debug(`Paddle ${this.id} position updated:`, this.positionX, this.positionY);
  }
}
