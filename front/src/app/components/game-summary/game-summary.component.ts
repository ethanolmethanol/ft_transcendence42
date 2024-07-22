import {Component, Inject, Input} from '@angular/core';
import { GameSummaryResponse} from "../../interfaces/game-summary-response.interface";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-game-summary',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './game-summary.component.html',
  styleUrl: './game-summary.component.css'
})
export class GameSummaryComponent {

  @Input() gameSummary!: GameSummaryResponse;

  public get score1(): number {
    return this.gameSummary?.players[0]?.score;
  }

  public get score2(): number {
    return this.gameSummary?.players[1]?.score;
  }
}
