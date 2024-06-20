import { Component } from '@angular/core';
import {
  GAME_HEIGHT,
  GAME_WIDTH,
  LINE_THICKNESS,
} from "../../constants";
import { GameOverComponent } from '../gameover/gameover.component';
import { LoadingSpinnerComponent } from "../loading-spinner/loading-spinner.component";

@Component({
  selector: 'app-gameboard',
  standalone: true,
  imports: [
    GameOverComponent,
    LoadingSpinnerComponent,
  ],
  templateUrl: './gameboard.component.html',
  styleUrl: './gameboard.component.css'
})
export class GameboardComponent {
  paddle1Y = 0;
  paddle2Y = GAME_HEIGHT;
  ballX = GAME_WIDTH / 2;
  ballY = GAME_HEIGHT / 2;
  ballSpeedX = 2;
  ballSpeedY = 2;

  readonly lineThickness: number = LINE_THICKNESS;
  gameWidth: number = GAME_WIDTH;
  gameHeight: number = GAME_HEIGHT;
  waitingPlayers: string[] = [];
}
