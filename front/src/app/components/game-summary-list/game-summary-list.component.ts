import {Component, Input, OnInit} from '@angular/core';
import {Observable} from "rxjs";
import {GameSummaryResponse} from "../../interfaces/game-summary-response.interface";
import {AsyncPipe, NgForOf, NgIf} from "@angular/common";
import {GameSummaryComponent} from "../game-summary/game-summary.component";
import {UserService} from "../../services/user/user.service";

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
export class GameSummaryListComponent implements OnInit {
  @Input() userID?: number;
  gameSummaries$: Observable<GameSummaryResponse[]> | undefined;

  constructor(private userService: UserService) {}

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.gameSummaries$ = this.getSummaries();
  }

  public getSummaries(): Observable<GameSummaryResponse[]> {
    return this.userService.getSummaries();
  }
}
