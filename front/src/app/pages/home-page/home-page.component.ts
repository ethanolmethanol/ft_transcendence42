import { Component, OnInit } from '@angular/core';
import { RouterLink } from "@angular/router";
import { HeaderComponent } from "../../components/header/header.component";
import { LeaderboardComponent } from "../../components/leaderboard/leaderboard.component";
import { UserService } from '../../services/user/user.service';
import { LoadingSpinnerComponent } from "../../components/loading-spinner/loading-spinner.component";
import {AsyncPipe, NgForOf, NgIf, NgStyle} from "@angular/common";
import {ButtonWithIconComponent} from "../../components/button-with-icon/button-with-icon.component";
import {MonitorService} from "../../services/monitor/monitor.service";
import {GameSummaryResponse} from "../../interfaces/game-summary-response.interface";
import {GameSummaryComponent} from "../../components/game-summary/game-summary.component";
import {Observable} from "rxjs";
import {GameSummaryListComponent} from "../../components/game-summary-list/game-summary-list.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    RouterLink,
    HeaderComponent,
    LeaderboardComponent,
    LoadingSpinnerComponent,
    NgStyle,
    ButtonWithIconComponent,
    NgForOf,
    GameSummaryComponent,
    AsyncPipe,
    NgIf,
    GameSummaryListComponent,
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent implements OnInit {
  welcome: string = '';
  userID: number | undefined;

  constructor(private userService: UserService) { }

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.welcome = `Welcome, ${this.userService.getUsername()}`;
    this.userID = this.userService.getUserID();
 }
}
