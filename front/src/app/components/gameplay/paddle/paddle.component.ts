import {Component, Input, Renderer2, ElementRef, SimpleChanges, OnInit} from '@angular/core';
import {GAME_HEIGHT, GAME_WIDTH, PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_X_OFFSET, PADDLE_SPEED} from '../../../constants';
import {Position} from '../../../interfaces/position.interface';
import {NgIf} from "@angular/common";
import * as Constants from '../../../constants';

@Component({
  selector: 'app-paddle',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './paddle.component.html',
  styleUrl: './paddle.component.css'
})
export class PaddleComponent {
  @Input() id: number = 0;
  playerName: string = '';
  width: number = PADDLE_WIDTH;
  height: number = PADDLE_HEIGHT;
  positionX: number = 0;
  positionY: number = 0;
  afkLeftTime : number | null = null;

  constructor(private renderer: Renderer2, private el: ElementRef) {}

  public setColor(paddleColor: string) {
    this._setStyle('.paddle', 'background-color', paddleColor);
  }

  private _setStyle(selector: string, styleName: string, styleValue: string) {
    const element = this.el.nativeElement.querySelector(selector);
    this.renderer.setStyle(element, styleName, styleValue);
  }

  public updatePaddlePosition(position: Position) {
    this.positionX = position.x;
    this.positionY = position.y;
    console.debug(`Paddle ${this.id} position updated:`, this.positionX, this.positionY);
  }
}
