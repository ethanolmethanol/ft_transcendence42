import {AfterViewInit, ChangeDetectorRef, Component, Input, OnInit} from '@angular/core';
import {Observable, of} from "rxjs";
import {GameSummaryResponse} from "../../../interfaces/game-history-response.interface";
import {AsyncPipe, NgClass, NgForOf, NgIf} from "@angular/common";
import {GameSummaryComponent} from "../game-summary/game-summary.component";
import {UserService} from "../../../services/user/user.service";
import {GAME_HISTORY_COUNT_REQUEST} from "../../../constants";
import {ChangeDetection} from "@angular/cli/lib/config/workspace-schema";
import {LoadingSpinnerComponent} from "../../loading-spinner/loading-spinner.component";
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-game-summary-list',
  standalone: true,
  imports: [
    NgIf,
    GameSummaryComponent,
    AsyncPipe,
    NgForOf,
    LoadingSpinnerComponent,
    NgClass,
    FormsModule
  ],
  templateUrl: './game-summary-list.component.html',
  styleUrl: './game-summary-list.component.css'
})
export class GameSummaryListComponent implements AfterViewInit {
  @Input() userID?: number;
  gameSummaries$: Observable<GameSummaryResponse[]> | undefined;
  public isComplete: boolean = false;
  public isWaiting: boolean = true;
  private startIndex: number = 0;
  private endIndex: number = GAME_HISTORY_COUNT_REQUEST - 1;
  private allSummaries: GameSummaryResponse[] = [];
  public filterType: 'all' | 'local' | 'online' = 'all';


  constructor(private userService: UserService, private cdr: ChangeDetectorRef) {}

  async ngAfterViewInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    setTimeout(() => {
      this.refreshSummaries();
      this.isWaiting = false;
    }, 1000);
  }

  public loadMoreSummaries(): void {
    this.userService.getSummaries(this.startIndex, this.endIndex + 1, this.filterType).subscribe(summaries => {
      this.allSummaries = [...this.allSummaries, ...summaries.summaries];
      this.gameSummaries$ = of(this.allSummaries);
      if (summaries.has_more) {
        this.startIndex = this.endIndex + 1;
        this.endIndex += GAME_HISTORY_COUNT_REQUEST;
        this.isComplete = false;
      } else {
        this.isComplete = true;
      }
      this.cdr.detectChanges();
    });
  }

  public refreshSummaries(): void {
    console.log('refreshing game summaries');
    this.startIndex = 0;
    this.endIndex = GAME_HISTORY_COUNT_REQUEST - 1;
    this.allSummaries = [];
    this.loadMoreSummaries();
  }

  public applyFilterType(): void {
    this.refreshSummaries();
  }
}
