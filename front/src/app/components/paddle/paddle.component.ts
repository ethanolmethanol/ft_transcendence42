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
  private paddles = [
    { id: 1, upKey: 'ArrowUp', downKey: 'ArrowDown' },
    { id: 2, upKey: 'w', downKey: 's' },
    // Add more paddles as needed
  ];
  private gameHeight = 500; // Height of the game component
  private paddleHeight = 100; // Height of the paddle
  private speed = 10; // Speed at which the paddle moves
  position = (this.gameHeight - this.paddleHeight) / 2; // Initial position of the paddle
  @HostListener('window:keydown', ['$event'])
  private onKeyDown(event: KeyboardEvent) {
    // Find the paddle with the current id
    const paddle = this.paddles.find(p => p.id === this.id);

    if (paddle) {
      if (event.key === paddle.upKey) {
        this.moveUp();
      } else if (event.key === paddle.downKey) {
        this.moveDown();
      }
    }
  }

  private moveUp() {
    if (this.position > 0) {
      this.position -= this.speed; // Move the paddle up
      this.updatePaddlePosition();
    }
  }

  private moveDown() {
    if (this.position < this.gameHeight - this.paddleHeight) {
      this.position += this.speed; // Move the paddle down
      this.updatePaddlePosition();
    }
  }

  private updatePaddlePosition() {
    // Logic to update the paddle's position in the DOM
    // This could involve setting a CSS property or manipulating the DOM directly
    console.log('Paddle position updated:', this.position);
  }
}
