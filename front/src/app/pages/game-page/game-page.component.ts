import {Component, HostListener, OnInit, QueryList, ViewChildren, AfterViewInit} from '@angular/core';
import {PaddleComponent} from "../../components/paddle/paddle.component";
import {RouterLink} from "@angular/router";
import {GAME_HEIGHT, GAME_WIDTH} from "../../constants";

@Component({
  selector: 'app-game-page',
  standalone: true,
  imports: [
    PaddleComponent,
    RouterLink
  ],
  templateUrl: './game-page.component.html',
  styleUrl: './game-page.component.css'
})
export class GamePageComponent implements AfterViewInit {
  gameWidth = GAME_WIDTH;
  gameHeight = GAME_HEIGHT;
  @ViewChildren(PaddleComponent) paddles!: QueryList<PaddleComponent>;

  private paddleBinding = [
    { id: 1, upKey: 'w', downKey: 's' },
    { id: 2, upKey: 'ArrowUp', downKey: 'ArrowDown' },
  ];

  private pressedKeys = new Set<string>();

  @HostListener('window:keydown', ['$event'])
  private onKeyDown(event: KeyboardEvent) {
    this.pressedKeys.add(event.key);
  }

  @HostListener('window:keyup', ['$event'])
  private onKeyUp(event: KeyboardEvent) {
    this.pressedKeys.delete(event.key);
  }

  private gameLoop() {
    this.paddleBinding.forEach(paddleBinding => {
      const paddle = this.paddles.find(p => p.id === paddleBinding.id);
      if (paddle) {
        this.movePaddle(paddle, paddleBinding)
      }
    });

    // Call this function again on the next frame
    requestAnimationFrame(() => this.gameLoop());
  }

  private movePaddle(paddle: PaddleComponent, binding: { upKey: string; downKey: string }) {
    const isMovingUp = this.pressedKeys.has(binding.upKey) && !this.pressedKeys.has(binding.downKey);
    const isMovingDown = this.pressedKeys.has(binding.downKey) && !this.pressedKeys.has(binding.upKey);

    if (isMovingUp) {
      paddle.moveUp();
    } else if (isMovingDown) {
      paddle.moveDown();
    }
  }



  ngAfterViewInit() {
    this.gameLoop();
  }
}
