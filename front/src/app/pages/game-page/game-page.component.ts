import {Component, HostListener, OnInit, QueryList, ViewChildren, AfterViewInit} from '@angular/core';
import {PaddleComponent} from "../../components/paddle/paddle.component";
import {RouterLink} from "@angular/router";

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
        if (this.pressedKeys.has(paddleBinding.upKey)) {
          paddle.moveUp();
        } else if (this.pressedKeys.has(paddleBinding.downKey)) {
          paddle.moveDown();
        }
      }
    });

    // Call this function again on the next frame
    requestAnimationFrame(() => this.gameLoop());
  }

  ngAfterViewInit() {
    this.gameLoop();
  }
}
