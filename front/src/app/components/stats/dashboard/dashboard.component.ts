import {Component, OnInit} from '@angular/core';
import {UserService} from "../../../services/user/user.service";
import {DatePipe, NgIf} from "@angular/common";
import {formatTimePlayed} from "../../../utils/time";
import {TimePlayedComponent} from "../time-played/time-played.component";
import {LoadingSpinnerComponent} from "../../loading-spinner/loading-spinner.component";
import {WinRateComponent} from "../win-rate/win-rate.component";
import {Wins} from "../../../interfaces/user";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    TimePlayedComponent,
    LoadingSpinnerComponent,
    NgIf,
    WinRateComponent
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent implements OnInit {

  isWaiting = true;
  timePlayed: string = '';
  winDict: Wins | null = null

  constructor(private userService: UserService) {
    console.log('DashboardComponent created');
  }

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    setTimeout(() => {
      this.initTimePlayed();
      this.initWinDict();
      this.isWaiting = false;
    }, 1000);
  }


  initTimePlayed(): void {
    const timePlayedInSeconds = this.userService.getTimePlayed();
    this.timePlayed = formatTimePlayed(timePlayedInSeconds)
  }

  initWinDict(): void {
    this.winDict = this.userService.getWinDict();
    console.log(this.winDict)
  }
}
