import {Component, HostListener} from '@angular/core';

@Component({
  selector: 'app-paddle',
  standalone: true,
  imports: [],
  templateUrl: './paddle.component.html',
  styleUrl: './paddle.component.css'
})
export class PaddleComponent {
  gameHeight = 500; // Height of the game component
  paddleHeight = 100; // Height of the paddle
  position = 0; // Initial position of the paddle

  @HostListener('window:keydown', ['$event'])
  onKeyDown(event: KeyboardEvent) {
    if (event.key === 'ArrowUp') {
      this.moveUp();
    } else if (event.key === 'ArrowDown') {
      this.moveDown();
    }
  }

  moveUp() {
    if (this.position > 0) {
      this.position -= 10; // Move the paddle up
      this.updatePaddlePosition();
    }
  }

  moveDown() {
    if (this.position < this.gameHeight - this.paddleHeight) {
      this.position += 10; // Move the paddle down
      this.updatePaddlePosition();
    }
  }

  updatePaddlePosition() {
    // Logic to update the paddle's position in the DOM
    // This could involve setting a CSS property or manipulating the DOM directly
    console.log('Paddle position updated:', this.position);
  }
}
