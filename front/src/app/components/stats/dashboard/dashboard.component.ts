import {Component, OnInit} from '@angular/core';
import {UserService} from "../../../services/user/user.service";
import {NgIf} from "@angular/common";
import {TimePlayedComponent} from "../time-played/time-played.component";
import {LoadingSpinnerComponent} from "../../loading-spinner/loading-spinner.component";
import {WinRateComponent} from "../win-rate/win-rate.component";
import {GameCounter, Times, Wins} from "../../../interfaces/user";
import {GameCounterComponent} from "../game-counter/game-counter.component";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    TimePlayedComponent,
    LoadingSpinnerComponent,
    NgIf,
    WinRateComponent,
    GameCounterComponent
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent implements OnInit {

  isWaiting: boolean = true;
  timePlayed: Times | null = null;
  winDict: Wins | null = null;
  gameCounter: GameCounter | null = null;

  constructor(private userService: UserService) {
    console.log('DashboardComponent created');
  }

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    setTimeout(() => {
      this.initTimePlayed();
      this.initWinDict();
      this.initGameCounter();
      this.isWaiting = false;
    }, 1000);
  }


  private initTimePlayed(): void {
    this.timePlayed = this.userService.getTimePlayed();
  }

  private initWinDict(): void {
    this.winDict = this.userService.getWinDict();
  }

  private initGameCounter(): void {
    this.gameCounter = this.userService.getGameCounter();
  }

  public isWinDictEmpty(): boolean {
    return this.winDict === null ||
      this.winDict.total === 0;
  }
}
