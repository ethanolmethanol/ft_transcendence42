import { Component, EventEmitter } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import { SliderComponent } from '../../components/slider/slider.component';
import * as Constants from '../../constants';
import { Router, NavigationExtras, RouterLink } from '@angular/router';
import { UserService } from '../../services/user/user.service';

@Component({
  selector: 'app-create-online-game-page',
  standalone: true,
  imports: [
    HeaderComponent,
    SliderComponent,
    RouterLink,
  ],
  templateUrl: './create-online-game-page.component.html',
  styleUrl: './create-online-game-page.component.css'
})
export class CreateOnlineGamePageComponent {
  constants = Constants;
  initialSettings: number[] = this.gameSettingsFromBackend;
  options: Option[] = [
    new Option('ballSpeed', this.constants.BALL_SPEED_OPTIONS, this.initialSettings[this.constants.BALL_SPEED]),
    new Option('paddleSize', this.constants.PADDLE_SIZE_OPTIONS, this.initialSettings[this.constants.PADDLE_SIZE]),
    new Option('numberPlayers', this.constants.NUMBER_PLAYERS_OPTIONS, this.initialSettings[this.constants.NUMBER_PLAYERS])
  ];
  saveConfig: boolean = false;
  settingsSaved: number[] = [];

  constructor(private router: Router, private userService: UserService) {}

  public handleOptionSelected(optionIndex: number, optionType: number): void {
    this.options[optionType].optionIndex = optionIndex;

    if (this._isBadSelection() && optionType === this.constants.PADDLE_SIZE) {
      this.options[this.constants.BALL_SPEED].optionIndex = 4;
    }
  }

  private _isBadSelection(): boolean {
    return false;
    return (this.options[this.constants.BALL_SPEED].value() === 'snail' && this.options[this.constants.PADDLE_SIZE].value() === 'jumbo');
  }

  get gameSettingsFromBackend(): number[] {
    if (!this.userService) {
      return [];
    }
    return this.userService.getGameSettings();
  }

  public saveSettings(event: Event): void {
    const inputElement = event.target as HTMLInputElement;
    const save: boolean = inputElement.checked;
    if (save) {
        this.saveConfig = true;
    }
    else {
      this.saveConfig = false;
    }
  }

  private _setSavedSettings(): void {
    this.settingsSaved = [
      this.options[this.constants.BALL_SPEED].optionIndex, 
      this.options[this.constants.PADDLE_SIZE].optionIndex, 
      this.options[this.constants.NUMBER_PLAYERS].optionIndex,
    ]
  }

  private _sendSettingsToBackend(): void {
    this._setSavedSettings();
    this.userService.setGameSettings(this.settingsSaved);
  }

  private _getSelectedOptions(): string[] {
    return [
      this.options[this.constants.BALL_SPEED].value(), 
      this.options[this.constants.PADDLE_SIZE].value(), 
      this.options[this.constants.NUMBER_PLAYERS].value()
    ];
  }

  public navigateToWaitPage(): void {
    const selectedOptions = this._getSelectedOptions();

    console.log('Navigating to join game');
    if (this.saveConfig)
      this._sendSettingsToBackend();
    const navigationExtras: NavigationExtras = {
      state: {
        options: selectedOptions
      }
    };

    this.router.navigate(['/online/create/waiting'], navigationExtras);
  }
}

export class Option {
  optionIndexChange = new EventEmitter<number>();

  constructor(public name: string, public options: string[], private _optionIndex: number) {}

  public get optionIndex(): number {
    return this._optionIndex;
  }

  public set optionIndex(optionIndex: number) {
    this._optionIndex = optionIndex;
    this.optionIndexChange.emit(this._optionIndex);
  }

  public value(): string {
    return this.options[this._optionIndex];
  }
}
