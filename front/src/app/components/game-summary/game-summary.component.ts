import {Component, Inject, Input} from '@angular/core';
import { GameSummaryResponse} from "../../interfaces/game-history-response.interface";
import {DatePipe, NgClass, NgIf} from "@angular/common";
import {LOCALE, TIME_ZONE} from "../../constants";

@Component({
  selector: 'app-game-summary',
  standalone: true,
  imports: [
    NgIf,
    NgClass,
  ],
  templateUrl: './game-summary.component.html',
  styleUrl: './game-summary.component.css'
})
export class GameSummaryComponent {

  @Input() userID?: number;
  @Input() gameSummary!: GameSummaryResponse;

  public get win_status(): string {
    if (this.gameSummary?.winner) {
      return this.gameSummary?.winner.user_id === this.userID ? 'Won' : 'Lost';
    }
    return 'Tied';
  }

  public get score1(): number {
    return this.gameSummary?.players[0]?.score;
  }

  public get score2(): number {
    return this.gameSummary?.players[1]?.score;
  }

  public get opponent(): string {
    return this.gameSummary?.players.find(player => player.user_id !== this.userID)?.player_name!;
  }

  public get date(): string {
    const datePipe = new DatePipe(LOCALE); // Use your locale
    return datePipe.transform(this.gameSummary?.end_time, 'short', TIME_ZONE)!;
  }
}