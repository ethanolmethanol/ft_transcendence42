import {Component, HostListener, QueryList, ViewChildren} from '@angular/core';
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
export class GamePageComponent {
  @ViewChildren(PaddleComponent) paddles!: QueryList<PaddleComponent>;

  private paddleBinding = [
    { id: 1, upKey: 'ArrowUp', downKey: 'ArrowDown' },
    { id: 2, upKey: 'w', downKey: 's' },
  ];

  @HostListener('window:keydown', ['$event'])
  private onKeyDown(event: KeyboardEvent) {
    const paddleBinding = this.paddleBinding.find(p => event.key === p.upKey || event.key === p.downKey);

    if (paddleBinding) {
      const paddle = this.paddles.find(p => p.id === paddleBinding.id);
      if (paddle) {
        if (event.key === paddleBinding.upKey) {
          paddle.moveUp();
        } else if (event.key === paddleBinding.downKey) {
          paddle.moveDown();
        }
      }
    }
  }
}
