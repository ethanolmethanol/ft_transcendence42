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
    { id: 'bg1', name: 'Bg1', title: 'Change top background color here', colors: [Constants.BACKGROUND_COLOR1] },
    { id: 'bg2', name: 'Bg2', title: 'Change bottom background color here', colors: [Constants.BACKGROUND_COLOR2] },
    { id: 'lines', name: 'Lines', title: 'Change lines color here', colors: [Constants.LINE_COLOR] },
    { id: 'score', name: 'Score', title: 'Change score color here', colors: [Constants.SCORE_COLOR] },
    { id: 'paddles', name: 'Paddles', title: 'Change paddle color here', colors: [Constants.PADDLE_COLOR] },
    { id: 'ball', name: 'Ball', title: 'Change ball color here', colors: [Constants.BALL_COLOR] },
  ];
  currentTab: string = 'bg1'; // Default tab
  constants = Constants;
  
  onColorSelected(color: string, index: number) {
    this.selectedColors[index] = color;
    this.colors.emit(this.selectedColors);
  }
}
