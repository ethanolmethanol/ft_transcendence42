import { Component, ViewEncapsulation, Output, Input, EventEmitter } from '@angular/core';
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
  @Input() selectedColors: string[] = Constants.DEFAULT_COLORS;

  readonly tabs = [
    { id: 'bg1', name: 'Bg1', title: 'Change top background color here', colorIndex: Constants.BACKGROUND_COLOR1 },
    { id: 'bg2', name: 'Bg2', title: 'Change bottom background color here', colorIndex: Constants.BACKGROUND_COLOR2 },
    { id: 'border', name: 'Lines', title: 'Change lines color here', colorIndex: Constants.LINE_COLOR },
    { id: 'score', name: 'Score', title: 'Change score color here', colorIndex: Constants.SCORE_COLOR },
    { id: 'paddles', name: 'Paddles', title: 'Change paddle color here', colorIndex: Constants.PADDLE_COLOR },
    { id: 'ball', name: 'Ball', title: 'Change ball color here', colorIndex: Constants.BALL_COLOR },
  ];
  currentTab: string = 'bg1'; // Default tab
  constants = Constants;
  
  onColorSelected(color: string, index: number) {
    this.selectedColors[index] = color;
    this.colors.emit(this.selectedColors);
  }
}
