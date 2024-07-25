import { Component, Input, Renderer2, ElementRef } from '@angular/core';
import { BALL_RADIUS, GAME_HEIGHT, GAME_WIDTH } from "../../constants";
import { Position } from "../../interfaces/position.interface";
import * as Constants from '../../constants';

@Component({
  selector: 'app-ball',
  standalone: true,
  imports: [],
  templateUrl: './ball.component.html',
  styleUrl: './ball.component.css'
})
export class BallComponent {
  @Input() positionX: number = 150;
  @Input() positionY: number = 150;
  @Input() ballSize = BALL_RADIUS * 2;

  constructor(private renderer: Renderer2, private el: ElementRef) {}

  public setColor(ballColor: string) {
    this._setStyle('.ball', 'background-color', ballColor);
  }

  private _setStyle(selector: string, styleName: string, styleValue: string) {
    const element = this.el.nativeElement.querySelector(selector);
    this.renderer.setStyle(element, styleName, styleValue);
  }

  public updateBallPosition(position: Position) {
    this.positionX = Math.max(0, Math.min(position.x, GAME_WIDTH));
    this.positionY = Math.max(0, Math.min(position.y, GAME_HEIGHT));
  }
}
