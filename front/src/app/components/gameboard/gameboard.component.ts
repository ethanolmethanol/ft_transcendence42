import { Component, Input, Renderer2, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  GAME_HEIGHT,
  GAME_WIDTH,
  LINE_THICKNESS,
} from "../../constants";
import { GameOverComponent } from '../gameover/gameover.component';
import { LoadingSpinnerComponent } from "../loading-spinner/loading-spinner.component";
import * as Constants from '../../constants';

@Component({
  selector: 'app-gameboard',
  standalone: true,
  imports: [
    GameOverComponent,
    LoadingSpinnerComponent,
    CommonModule,
  ],
  templateUrl: './gameboard.component.html',
  styleUrl: './gameboard.component.css'
})
export class GameboardComponent {
  @Input() gameboardColors: string[] = Constants.DEFAULT_COLORS;

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

  constructor(private renderer: Renderer2, private el: ElementRef) {}

  ngDoCheck() {
    this.updateStyles();
  }

  updateStyles() {
    this.setGameContainerStyle();
    this.setGameStyle();
    this.setDottedLineStyle();
    this.setScoreDisplayStyle();
    this.setPaddleRightStyle();
    this.setPaddleLeftStyle();
    this.setBallStyle();
  }
  
  setStyle(selector: string, styleName: string, styleValue: string) {
    const element = this.el.nativeElement.querySelector(selector);
    this.renderer.setStyle(element, styleName, styleValue);
  }
  
  setGameContainerStyle() {
    this.setStyle('.game-container', 
                  'background', 
                  `linear-gradient(${this.backgroundColor1}, ${this.backgroundColor2})`
    );
    this.setStyle('.game-container', 
                  'border', 
                  `6px solid ${this.lineColor}`
    );
  }
  
  setGameStyle() {
    this.setStyle('.game', 
                  'background', 
                  `linear-gradient(${this.backgroundColor1}, ${this.backgroundColor2})`
    );
  }
  
  setDottedLineStyle() {
    this.setStyle('.dotted-line', 
                  '--line-thickness', 
                  `${this.lineThickness}px`
    );
    this.setStyle('.dotted-line', 
                  'background', 
                  `linear-gradient(to bottom, ${this.lineColor} 60%, transparent 10%)`
    );
    this.setStyle('.dotted-line', 
                  'background-size', 
                  '100% 40px'
    );
  }
  
  setScoreDisplayStyle() {
    this.setStyle('.score-display', 'color', this.scoreColor);
  }

  setPaddleLeftStyle() {
    this.setStyle('.paddle-left', 'background-color', this.paddleColor);
  }

  setPaddleRightStyle() {
    this.setStyle('.paddle-right', 'background-color', this.paddleColor);
  }
  
  setBallStyle() {
    this.setStyle('.ball', 'background-color', this.ballColor);
  }

  get ballColor(): string {
    return this.gameboardColors[Constants.BALL_COLOR];
  }
  
  get paddleColor(): string {
    return this.gameboardColors[Constants.PADDLE_COLOR];
  }
  
  get backgroundColor1(): string {
    return this.gameboardColors[Constants.BACKGROUND_COLOR1];
  }
  
  get backgroundColor2(): string {
    return this.gameboardColors[Constants.BACKGROUND_COLOR2];
  }

  get lineColor(): string {
    return this.gameboardColors[Constants.LINE_COLOR];
  }

  get scoreColor(): string {
    return this.gameboardColors[Constants.SCORE_COLOR];
  }
}
