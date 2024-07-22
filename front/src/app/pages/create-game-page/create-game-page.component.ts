import { Component, OnInit } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import { SliderComponent } from '../../components/slider/slider.component';
import * as Constants from '../../constants';
import { ActivatedRoute, RouterLink } from '@angular/router';
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
  }

  public handleOptionSelected(optionIndex: number, optionType: number): void {
    this.options[optionType].optionIndex = optionIndex;

    if (this._isBadSelection())
      this._adjustSelection(optionType);
  }

  private _isBadSelection(): boolean {
    let totalOpponents: number = 0;
    if (this.isRemote)
      totalOpponents = this.options[this.constants.ONLINE_OPPONENTS].value() + this.options[this.constants.AI_OPPONENTS_ONLINE].value();
    else
      totalOpponents = this.options[this.constants.HUMAN_OPPONENTS].value() + this.options[this.constants.AI_OPPONENTS_LOCAL].value();
    return (totalOpponents > this.constants.MAX_OPPONENTS || (totalOpponents == 0 && !this.isRemote));
  }

  private _adjustLocalSelection(optionType: number): void {
    const totalOpponents = this.options[this.constants.HUMAN_OPPONENTS].value() + this.options[this.constants.AI_OPPONENTS_LOCAL].value();

    if (totalOpponents == 0 && optionType == this.constants.HUMAN_OPPONENTS) {
      this.options[this.constants.AI_OPPONENTS_LOCAL].optionIndex = 1;
    } else if (totalOpponents == 0 && optionType == this.constants.AI_OPPONENTS_LOCAL) {
      this.options[this.constants.HUMAN_OPPONENTS].optionIndex = 1;
    } else if (optionType === this.constants.HUMAN_OPPONENTS) {
      this.options[this.constants.AI_OPPONENTS_LOCAL].optionIndex = this.constants.MAX_OPPONENTS - this.options[this.constants.HUMAN_OPPONENTS].optionIndex;
    } else if (optionType === this.constants.AI_OPPONENTS_LOCAL) {
      this.options[this.constants.HUMAN_OPPONENTS].optionIndex = this.constants.MAX_OPPONENTS - this.options[this.constants.AI_OPPONENTS_LOCAL].optionIndex;
    }
  }

  private _adjustRemoteSelection(optionType: number): void {
    if (optionType === this.constants.ONLINE_OPPONENTS) {
      this.options[this.constants.AI_OPPONENTS_ONLINE].optionIndex = this.constants.MAX_OPPONENTS - this.options[this.constants.ONLINE_OPPONENTS].optionIndex - 1;
    } else if (optionType === this.constants.AI_OPPONENTS_ONLINE) {
      this.options[this.constants.ONLINE_OPPONENTS].optionIndex = this.constants.MAX_OPPONENTS - this.options[this.constants.AI_OPPONENTS_ONLINE].optionIndex - 1;
    }
  }
  
  private _adjustSelection(optionType: number): void {
    if (this.isRemote)
      this._adjustRemoteSelection(optionType);
    else
      this._adjustLocalSelection(optionType);
  }

  public saveSettings(event: Event): void {
    const inputElement = event.target as HTMLInputElement;
    this.saveConfig = inputElement.checked;
  }

  private _setSavedSettings(): void {
    this.settingsSaved = [
      this.options[this.constants.BALL_SPEED].optionIndex,
      this.options[this.constants.PADDLE_SIZE].optionIndex,
      this.options[this.constants.HUMAN_OPPONENTS].optionIndex,
      this.options[this.constants.ONLINE_OPPONENTS].optionIndex,
      this.options[this.constants.AI_OPPONENTS_LOCAL].optionIndex,
      this.options[this.constants.AI_OPPONENTS_ONLINE].optionIndex,
      this.options[this.constants.IS_PRIVATE].optionIndex,
    ]
  }

  private get _options(): Option[] {
    return [
      new Option('ballSpeed', this.constants.BALL_SPEED_OPTIONS, this.settingsSaved[this.constants.BALL_SPEED]),
      new Option('paddleSize', this.constants.PADDLE_SIZE_OPTIONS, this.settingsSaved[this.constants.PADDLE_SIZE]),
      new Option('humanPlayers', this.constants.HUMAN_OPPONENTS_OPTIONS, this.settingsSaved[this.constants.HUMAN_OPPONENTS]),
      new Option('onlinePlayers', this.constants.ONLINE_OPPONENTS_OPTIONS, this.settingsSaved[this.constants.ONLINE_OPPONENTS]),
      new Option('aiOpponentsLocal', this.constants.AI_OPPONENTS_LOCAL_OPTIONS, this.settingsSaved[this.constants.AI_OPPONENTS_LOCAL]),
      new Option('aiOpponentsOnline', this.constants.AI_OPPONENTS_ONLINE_OPTIONS, this.settingsSaved[this.constants.AI_OPPONENTS_ONLINE]),
      new Option('isPrivate', this.constants.IS_PRIVATE_OPTIONS, this.settingsSaved[this.constants.IS_PRIVATE]),
    ];
  }

  private get _localGameSettings(): any[] {
    return [
      { label: 'Ball Speed', optionType: this.constants.BALL_SPEED, options: this.constants.BALL_SPEED_OPTIONS },
      { label: 'Paddle Size', optionType: this.constants.PADDLE_SIZE, options: this.constants.PADDLE_SIZE_OPTIONS },
      { label: 'Human Players', optionType: this.constants.HUMAN_OPPONENTS, options: this.constants.HUMAN_OPPONENTS_OPTIONS },
      { label: 'AI Opponents', optionType: this.constants.AI_OPPONENTS_LOCAL, options: this.constants.AI_OPPONENTS_LOCAL_OPTIONS },
      { label: 'Visibility', optionType: this.constants.IS_PRIVATE, condition: this.isRemote, options: this.constants.IS_PRIVATE_OPTIONS },
    ];
  }

  private get _onlineGameSettings(): any[] {
    return [
      { label: 'Ball Speed', optionType: this.constants.BALL_SPEED, options: this.constants.BALL_SPEED_OPTIONS },
      { label: 'Paddle Size', optionType: this.constants.PADDLE_SIZE, options: this.constants.PADDLE_SIZE_OPTIONS },
      { label: 'Online Opponents', optionType: this.constants.ONLINE_OPPONENTS, options: this.constants.ONLINE_OPPONENTS_OPTIONS },
      { label: 'AI Opponents', optionType: this.constants.AI_OPPONENTS_ONLINE, options: this.constants.AI_OPPONENTS_ONLINE_OPTIONS },
      { label: 'Visibility', optionType: this.constants.IS_PRIVATE, condition: this.isRemote, options: this.constants.IS_PRIVATE_OPTIONS },
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
      this.options[this.constants.BALL_SPEED].optionIndex,
      this.options[this.constants.PADDLE_SIZE].optionIndex,
      this.options[this.constants.HUMAN_OPPONENTS].optionIndex,
      this.options[this.constants.ONLINE_OPPONENTS].optionIndex,
      this.options[this.constants.AI_OPPONENTS_LOCAL].optionIndex,
      this.options[this.constants.AI_OPPONENTS_ONLINE].optionIndex,
      this.options[this.constants.IS_PRIVATE].optionIndex,
    ];
  }

  public navigateToWaitPage(): void {
    console.log('Navigating to join game');
    const selectedOptions = this._getSelectedOptions();
    console.log('Selected options:', selectedOptions);
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
    return Number(this.options[this._optionIndex]);
  }
}
