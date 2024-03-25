import {Component, HostListener, Input} from '@angular/core';

@Component({
  selector: 'app-paddle',
  standalone: true,
  imports: [],
  templateUrl: './paddle.component.html',
  styleUrl: './paddle.component.css'
})
export class PaddleComponent {
  @Input() id: number = 0;
  private gameHeight = 500; // Height of the game component
  private paddleHeight = 100; // Height of the paddle
  private speed = 10; // Speed at which the paddle moves
  // positionX = this.gameHeight * (this.id % 2); // Initial position of the paddle
  positionY = (this.gameHeight - this.paddleHeight) / 2; // Initial position of the paddle

  moveUp() {
    if (this.positionY > 0) {
      this.positionY -= this.speed; // Move the paddle up
      this.updatePaddlePosition();
    }
  }

  moveDown() {
    if (this.positionY < this.gameHeight - this.paddleHeight) {
      this.positionY += this.speed; // Move the paddle down
      this.updatePaddlePosition();
    }
  }

  private updatePaddlePosition() {
    // console.debug(`Paddle ${this.id} position updated:`, this.positionX, this.positionY);
  }
}

