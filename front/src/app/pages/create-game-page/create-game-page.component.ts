import { Component } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import { SliderComponent } from '../../components/slider/slider.component';
import * as Constants from '../../constants';
import {ActivatedRoute, RouterLink} from '@angular/router';
import { EventEmitter } from '@angular/core';
import { Router, NavigationExtras } from '@angular/router';

@Component({
  selector: 'app-create-game-page',
  standalone: true,
  imports: [
    HeaderComponent,
    SliderComponent,
    RouterLink,
  ],
  templateUrl: './create-game-page.component.html',
  styleUrl: './create-game-page.component.css'
})
export class CreateGamePageComponent {
  constants = Constants;
  options: Option[] = [
    new Option('ballSpeed', this.constants.BALL_SPEED_OPTIONS, this.constants.BALL_SPEED_DEFAULT),
    new Option('paddleSize', this.constants.PADDLE_SIZE_OPTIONS, this.constants.PADDLE_SIZE_DEFAULT),
    new Option('numberPlayers', this.constants.NUMBER_PLAYERS_OPTIONS, this.constants.NUMBER_PLAYERS_DEFAULT)
  ];
  urlDestination = '/';

  constructor(private router: Router, private route: ActivatedRoute) {
    const gameType = this.route.snapshot.data['gameType'];
    if (gameType === 'local') {
      this.urlDestination = '/local/waiting';
    } else if (gameType === 'online') {
      this.urlDestination = '/online/create/waiting';
    }
  }

  public handleOptionSelected(optionIndex: number, optionType: number): void {
    this.options[optionType].optionIndex = optionIndex;

    if (this._isBadSelection() && optionType === this.constants.PADDLE_SIZE) {
      this.options[this.constants.BALL_SPEED].optionIndex = 4;
    }
  }

  private _isBadSelection(): boolean {
    return false;
    // return (this.options[this.constants.BALL_SPEED].value() === 'snail' && this.options[this.constants.PADDLE_SIZE].value() === 'jumbo');
  }

  public navigateToWaitPage(): void {
    console.log('Navigating to join game');
    const selectedOptions = [
      this.options[this.constants.BALL_SPEED].value(),
      this.options[this.constants.PADDLE_SIZE].value(),
      this.options[this.constants.NUMBER_PLAYERS].value()
    ];
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
