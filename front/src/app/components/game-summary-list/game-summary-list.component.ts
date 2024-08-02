import {AfterViewInit, Component, Input, OnInit} from '@angular/core';
import {Observable, of} from "rxjs";
import {GameSummaryResponse} from "../../interfaces/game-history-response.interface";
import {AsyncPipe, NgForOf, NgIf} from "@angular/common";
import {GameSummaryComponent} from "../game-summary/game-summary.component";
import {UserService} from "../../services/user/user.service";
import {GAME_HISTORY_COUNT_REQUEST} from "../../constants";

@Component({
  selector: 'app-game-summary-list',
  standalone: true,
  imports: [
    NgIf,
    GameSummaryComponent,
    AsyncPipe,
    NgForOf
  ],
  templateUrl: './game-summary-list.component.html',
  styleUrl: './game-summary-list.component.css'
})
export class GameSummaryListComponent implements AfterViewInit {
  @Input() userID?: number;
  gameSummaries$: Observable<GameSummaryResponse[]> | undefined;
  public isComplete: boolean = false;
  private startIndex: number = 0;
  private endIndex: number = GAME_HISTORY_COUNT_REQUEST - 1;
  private allSummaries: GameSummaryResponse[] = [];

  constructor(private userService: UserService) {}

  async ngAfterViewInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.refreshSummaries();
  }

  public loadMoreSummaries(): void {
    this.userService.getSummaries(this.startIndex, this.endIndex + 1).subscribe(summaries => {
      this.allSummaries = [...this.allSummaries, ...summaries.summaries];
      this.gameSummaries$ = of(this.allSummaries);
      if (summaries.has_more) {
        this.startIndex = this.endIndex + 1;
        this.endIndex += GAME_HISTORY_COUNT_REQUEST;
      } else {
        this.isComplete = true;
      }
    });
  }

  public refreshSummaries(): void {
    this.startIndex = 0;
    this.endIndex = GAME_HISTORY_COUNT_REQUEST - 1;
    this.allSummaries = [];
    this.isComplete = false;
    this.loadMoreSummaries();
  }
}
