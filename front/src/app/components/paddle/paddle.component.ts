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
  speed = PADDLE_SPEED;
  positionX = 0;
  positionY = (GAME_HEIGHT - PADDLE_HEIGHT) / 2;

  ngOnInit() {
    if (this.id == 1) {
      this.positionX = PADDLE_X_OFFSET;
    } else if (this.id == 2) {
      this.positionX = GAME_WIDTH - PADDLE_WIDTH - PADDLE_X_OFFSET;
    }
    console.log(`Paddle ${this.id} initialized:`, this.positionX, this.positionY);
  }

  moveUp() {
    const initialPosition = this.positionY;
    if (this.positionY - this.speed >= 0) {
      this.positionY -= this.speed; // Move the paddle up
    } else {
      this.positionY = 0; // Move the paddle up
    }
    if (initialPosition !== this.positionY) {
      this.updatePaddlePosition();
    }
  }

  moveDown() {
    const initialPosition = this.positionY;
    if (this.positionY + PADDLE_HEIGHT + this.speed <= GAME_HEIGHT) {
      this.positionY += this.speed; // Move the paddle down
    } else {
      this.positionY = GAME_HEIGHT - PADDLE_HEIGHT;
    }
    if (initialPosition !== this.positionY) {
      this.updatePaddlePosition();
    }
  }

  private updatePaddlePosition() {
    console.debug(`Paddle ${this.id} position updated:`, this.positionX, this.positionY);
  }
}