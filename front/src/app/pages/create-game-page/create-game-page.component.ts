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
  isRemote: boolean = false;
  urlDestination: string = '/';
  options: Option[] = [];
  saveConfig: boolean = false;

  constructor(private router: Router, private route: ActivatedRoute, private userService: UserService) {
    const gameType = this.route.snapshot.data['gameType'];
    this.isRemote = (gameType === 'online');
    if (this.isRemote) {
      this.urlDestination = '/online/create/waiting';
    } else {
      this.urlDestination = '/local/waiting';
    }
    this.options = this._options;
  }

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.options = this._options;
  }

  public handleOptionSelected(optionIndex: number, optionType: number): void {
    this.options[optionType].optionIndex = optionIndex;

    if (this._isBadSelection())
      this._adjustSelection(optionType);
  }

  private get _totalOpponents(): number {
    let totalOpponents: number = 0;
    if (this.isRemote)
      totalOpponents = this.options[this.constants.OPPONENTS_ONLINE].value() + this.options[this.constants.AI_OPPONENTS_ONLINE].value();
    else
      totalOpponents = this.options[this.constants.OPPONENTS_LOCAL].value() + this.options[this.constants.AI_OPPONENTS_LOCAL].value();
    return totalOpponents;
  }

  private _isBadSelection(): boolean {
    return (this._totalOpponents > this.constants.MAX_OPPONENTS || (this._totalOpponents == 0 && !this.isRemote));
  }

  private _addOpponent(toAdjust: number): void {
    this.options[toAdjust].optionIndex = 1;
  }

  private _removeOpponent(toAdjust: number): void {
    this.options[toAdjust].optionIndex -= this._totalOpponents - this.constants.MAX_OPPONENTS;
  }

  private _adjustSetting(toAdjust: number): void {
    if (this._totalOpponents == 0) {
      this._addOpponent(toAdjust);
    } else {
      this._removeOpponent(toAdjust);
    }
  }

  private _adjustLocalSelection(optionType: number): void {
    if (optionType === this.constants.OPPONENTS_LOCAL) {
      this._adjustSetting(this.constants.AI_OPPONENTS_LOCAL);
    }
    else if (optionType === this.constants.AI_OPPONENTS_LOCAL) {
      this._adjustSetting(this.constants.OPPONENTS_LOCAL);
    }
  }

  private _adjustRemoteSelection(optionType: number): void {
    if (optionType === this.constants.OPPONENTS_ONLINE) {
      this._adjustSetting(this.constants.AI_OPPONENTS_ONLINE);
    } else if (optionType === this.constants.AI_OPPONENTS_ONLINE) {
      this._adjustSetting(this.constants.OPPONENTS_ONLINE);
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


  private get _options(): Option[] {
    const settingsSaved: number[] = this.userService.getGameSettings();
    const options: Option[] = [];
    for (let i = 0; i < this.constants.OPTIONS.length; i++) {
      options.push(new Option(
        this.constants.OPTIONS_LABELS[i],
        i,
        this.constants.OPTIONS[i],
        settingsSaved[i]
      ));
    }
    return options;
  }

  private get _localGameSettings(): Option[] {
    return [
      this.options[this.constants.BALL_SPEED],
      this.options[this.constants.PADDLE_SIZE],
      this.options[this.constants.OPPONENTS_LOCAL],
      this.options[this.constants.AI_OPPONENTS_LOCAL],
    ];
  }
  private get _onlineGameSettings(): Option[] {
    return [
      this.options[this.constants.BALL_SPEED],
      this.options[this.constants.PADDLE_SIZE],
      this.options[this.constants.OPPONENTS_ONLINE],
      this.options[this.constants.AI_OPPONENTS_ONLINE],
      this.options[this.constants.IS_PRIVATE],
    ];
  }

  public get gameSettings(): Option[] {
    if (this.isRemote) {
      return this._onlineGameSettings;
    }
    return this._localGameSettings;
  }

  private _sendSettingsToBackend(): void {
    this.userService.setGameSettings(this._selectedOptions);
  }

  private get _selectedOptions(): number[] {
    return [
      this.options[this.constants.BALL_SPEED].optionIndex,
      this.options[this.constants.PADDLE_SIZE].optionIndex,
      this.options[this.constants.OPPONENTS_LOCAL].optionIndex,
      this.options[this.constants.OPPONENTS_ONLINE].optionIndex,
      this.options[this.constants.AI_OPPONENTS_LOCAL].optionIndex,
      this.options[this.constants.AI_OPPONENTS_ONLINE].optionIndex,
      this.options[this.constants.IS_PRIVATE].optionIndex,
    ];
  }

  public navigateToWaitPage(): void {
    console.log('Navigating to join game');
    console.log('Selected options:', this._selectedOptions);
    if (this.saveConfig)
      this._sendSettingsToBackend();
    const navigationExtras: NavigationExtras = {
      state: {
        options: this._selectedOptions
      }
    };
    this.router.navigate([this.urlDestination], navigationExtras);
  }
}

export class Option {
  optionIndexChange = new EventEmitter<number>();

  constructor(public label: string, public optionType: number, public options: string[], private _optionIndex: number) {}

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
