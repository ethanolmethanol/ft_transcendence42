import { Component, ViewEncapsulation, Output, EventEmitter } from '@angular/core';
import { ColorWheelComponent } from '../color-wheel/color-wheel.component';
import * as Constants from '../../constants';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-appearance-settings',
  standalone: true,
  imports: [
    ColorWheelComponent,
    NgFor,
  ],
  templateUrl: './appearance-settings.component.html',
  styleUrl: './appearance-settings.component.css',
  encapsulation: ViewEncapsulation.None
})
export class AppearanceSettingsComponent {
  @Output() colors = new EventEmitter<string[]>();
  selectedColors: string[] = Constants.DEFAULT_COLORS;

  tabs = [
    { id: 'background', name: 'Background', title: 'Change the bg color here', colors: [Constants.BACKGROUND_COLOR1, Constants.BACKGROUND_COLOR2] },
    { id: 'lines', name: 'Lines', title: 'Change the lines color here', colors: [Constants.LINE_COLOR] },
    { id: 'score', name: 'Score', title: 'Change the score color here', colors: [Constants.SCORE_COLOR] },
    { id: 'paddles', name: 'Paddles', title: 'Change paddle color here', colors: [Constants.PADDLE_COLOR] },
    { id: 'ball', name: 'Ball', title: 'Change the ball color here', colors: [Constants.BALL_COLOR] },
  ];
  currentTab: string = 'background'; // Default tab
  constants = Constants;
  
  onColorSelected(color: string, index: number) {
    this.selectedColors[index] = color;
    this.colors.emit(this.selectedColors);
  }
}
