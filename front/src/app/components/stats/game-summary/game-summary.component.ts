import {Component, Inject, Input, OnInit} from '@angular/core';
import { GameSummaryResponse} from "../../../interfaces/game-history-response.interface";
import {DatePipe, NgClass, NgIf} from "@angular/common";
import {LOCALE, TIME_ZONE} from "../../../constants";
import {UserService} from "../../../services/user/user.service";
import {User} from "../../../interfaces/user";

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
export class GameSummaryComponent implements OnInit {

  @Input() userID?: number;
  @Input() gameSummary!: GameSummaryResponse;
  public opponentUsername!: string | undefined;

  constructor(private userService: UserService) {}

  async ngOnInit(): Promise<void> {
    await this.loadOpponentUsername();
  }

  public get win_status(): string {
    if (this.gameSummary.is_remote) {
      if (this.gameSummary?.winner_user_id) {
        return this.gameSummary?.winner_user_id === this.userID ? 'Won' : 'Lost';
      }
      return 'Tied';
    }
    return 'Local';
  }

  public get score1(): number {
    return this.gameSummary?.players[0]?.score;
  }

  public get score2(): number {
    return this.gameSummary?.players[1]?.score;
  }

  public async getOpponentUsername(): Promise<string> {
    if (this.gameSummary.is_remote) {
      const opponentUserID: number = this.gameSummary?.players.find(player => player.user_id !== this.userID)?.user_id!;
      const user: User = await this.userService.getUser(opponentUserID);
      return user.username;
    }
    return '-';
  }

  private async loadOpponentUsername(): Promise<void> {
    this.opponentUsername = await this.getOpponentUsername();
  }

  public get date(): string {
    const datePipe = new DatePipe(LOCALE); // Use your locale
    return datePipe.transform(this.gameSummary?.end_time, 'short', TIME_ZONE)!;
  }
}
