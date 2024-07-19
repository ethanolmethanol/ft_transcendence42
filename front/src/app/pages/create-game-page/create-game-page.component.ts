import { Component, OnInit } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import { SliderComponent } from '../../components/slider/slider.component';
import * as Constants from '../../constants';
import {ActivatedRoute, RouterLink} from '@angular/router';
import { EventEmitter } from '@angular/core';
import { Router, NavigationExtras } from '@angular/router';
import { NgIf, NgFor } from "@angular/common";
import { UserService } from "../../services/user/user.service";

@Component({
  selector: 'app-create-game-page',
  standalone: true,
  imports: [
    HeaderComponent,
    SliderComponent,
    RouterLink,
    NgIf,
    NgFor,
  ],
  templateUrl: './create-game-page.component.html',
  styleUrl: './create-game-page.component.css'
})
export class CreateGamePageComponent implements OnInit {
  constants = Constants;
  isRemote = false;
  urlDestination = '/';
  settingsSaved: number[] = [];
  options: Option[] = [];
  saveConfig: boolean = false;
  gameSettings: any[] = [];

  constructor(private router: Router, private route: ActivatedRoute, private userService: UserService) {
    const gameType = this.route.snapshot.data['gameType'];
    this.isRemote = (gameType === 'online');
    if (this.isRemote) {
      this.urlDestination = '/online/create/waiting';
    } else {
      this.urlDestination = '/local/waiting';
    }
  }

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.settingsSaved = this.userService.getGameSettings();
    this.options = this._options;
    this.gameSettings = this._gameSettings;
    console.log('Settings from backend: ', this.settingsSaved);
  }

  public handleOptionSelected(optionIndex: number, optionType: number): void {
    console.log('Option selected:', optionIndex, optionType);
    this.options[optionType].optionIndex = optionIndex;

    if (this._isBadSelection() && optionType === this.constants.PADDLE_SIZE) {
      this.options[this.constants.BALL_SPEED].optionIndex = 4;
    }
  }

  private _isBadSelection(): boolean {
    return false;
    // return (this.options[this.constants.BALL_SPEED].value() === 'snail' && this.options[this.constants.PADDLE_SIZE].value() === 'jumbo');
  }

  public saveSettings(event: Event): void {
    const inputElement = event.target as HTMLInputElement;
    this.saveConfig = inputElement.checked;
  }

  private _setSavedSettings(): void {
    this.settingsSaved = [
      this.options[this.constants.BALL_SPEED].optionIndex,
      this.options[this.constants.PADDLE_SIZE].optionIndex,
      this.options[this.constants.HUMAN_PLAYERS].optionIndex,
      this.options[this.constants.ONLINE_PLAYERS].optionIndex,
      this.options[this.constants.AI_OPPONENTS].optionIndex,
      this.options[this.constants.IS_PRIVATE].optionIndex,
    ]
  }

  private get _options(): Option[] {
    return [
      new Option('ballSpeed', this.constants.BALL_SPEED_OPTIONS, this.settingsSaved[this.constants.BALL_SPEED]),
      new Option('paddleSize', this.constants.PADDLE_SIZE_OPTIONS, this.settingsSaved[this.constants.PADDLE_SIZE]),
      new Option('numberPlayers', this.constants.HUMAN_PLAYERS_OPTIONS, this.settingsSaved[this.constants.HUMAN_PLAYERS]),
      new Option('numberPlayers', this.constants.ONLINE_PLAYERS_OPTIONS, this.settingsSaved[this.constants.ONLINE_PLAYERS]),
      new Option('aiOpponents', this.constants.AI_OPPONENTS_OPTIONS, this.settingsSaved[this.constants.AI_OPPONENTS]),
      new Option('isPrivate', this.constants.IS_PRIVATE_OPTIONS, this.settingsSaved[this.constants.IS_PRIVATE]),
    ];
  }

  private get _localGameSettings(): any[] {
    return [
      { label: 'Ball Speed', optionIndex: this.options[this.constants.BALL_SPEED].optionIndex, options: this.constants.BALL_SPEED_OPTIONS, optionType: this.constants.BALL_SPEED },
      { label: 'Paddle Size', optionIndex: this.options[this.constants.PADDLE_SIZE].optionIndex, options: this.constants.PADDLE_SIZE_OPTIONS, optionType: this.constants.PADDLE_SIZE },
      { label: 'Human Players', optionIndex: this.options[this.constants.HUMAN_PLAYERS].optionIndex, options: this.constants.HUMAN_PLAYERS_OPTIONS, optionType: this.constants.HUMAN_PLAYERS },
      { label: 'AI Opponents', optionIndex: this.options[this.constants.AI_OPPONENTS].optionIndex, options: this.constants.AI_OPPONENTS_OPTIONS, optionType: this.constants.AI_OPPONENTS },
      { label: 'Visibility', optionIndex: this.options[this.constants.IS_PRIVATE].optionIndex, condition: this.isRemote, options: this.constants.IS_PRIVATE_OPTIONS, optionType: this.constants.IS_PRIVATE },
    ];
  }

  private get _onlineGameSettings(): any[] {
    return [
      { label: 'Ball Speed', optionIndex: this.options[this.constants.BALL_SPEED].optionIndex, options: this.constants.BALL_SPEED_OPTIONS, optionType: this.constants.BALL_SPEED },
      { label: 'Paddle Size', optionIndex: this.options[this.constants.PADDLE_SIZE].optionIndex, options: this.constants.PADDLE_SIZE_OPTIONS, optionType: this.constants.PADDLE_SIZE },
      { label: 'Online Opponents', optionIndex: this.options[this.constants.ONLINE_PLAYERS].optionIndex, options: this.constants.ONLINE_PLAYERS_OPTIONS, optionType: this.constants.ONLINE_PLAYERS },
      { label: 'AI Opponents', optionIndex: this.options[this.constants.AI_OPPONENTS].optionIndex, options: this.constants.AI_OPPONENTS_OPTIONS, optionType: this.constants.AI_OPPONENTS },
      { label: 'Visibility', optionIndex: this.options[this.constants.IS_PRIVATE].optionIndex, condition: this.isRemote, options: this.constants.IS_PRIVATE_OPTIONS, optionType: this.constants.IS_PRIVATE },
    ];
  }

  private get _gameSettings(): any[] {
    if (this.isRemote) {
      return this._onlineGameSettings;
    }
    return this._localGameSettings;
  }

  private _sendSettingsToBackend(): void {
    this._setSavedSettings();
    this.userService.setGameSettings(this.settingsSaved);
  }

  private _getSelectedOptions(): number[] {
   return [
      this.options[this.constants.BALL_SPEED].value(),
      this.options[this.constants.PADDLE_SIZE].value(),
      this.options[this.constants.HUMAN_PLAYERS].value(),
      this.options[this.constants.ONLINE_PLAYERS].value(),
      this.options[this.constants.AI_OPPONENTS].value(),
      this.options[this.constants.IS_PRIVATE].value()
    ];
  }

  public navigateToWaitPage(): void {
    console.log('Navigating to join game');
    const selectedOptions = this._getSelectedOptions();
    console.log('Selected options:', selectedOptions);
    console.log('Options:', this.options);
    if (this.saveConfig)
      this._sendSettingsToBackend();
    const navigationExtras: NavigationExtras = {
      state: {
        options: selectedOptions
      }
    };
    this.router.navigate([this.urlDestination], navigationExtras);
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

  public value(): number {
    return this._optionIndex;
  }
}
