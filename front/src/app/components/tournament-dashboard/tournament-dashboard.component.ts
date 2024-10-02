import {Component, ElementRef, Input, OnChanges, OnInit} from '@angular/core';
import {PlayerIconComponent} from "../player-icon/player-icon.component";
import {AsyncPipe, KeyValuePipe, NgClass, NgForOf, NgIf} from "@angular/common";
import {TournamentMap} from "../../interfaces/tournament-map.interface";
import { UserService } from '../../services/user/user.service';

@Component({
  selector: 'app-tournament-dashboard',
  standalone: true,
  imports: [
    PlayerIconComponent,
    NgForOf,
    KeyValuePipe,
    AsyncPipe,
    NgIf,
    NgClass
  ],
  templateUrl: './tournament-dashboard.component.html',
  styleUrl: './tournament-dashboard.component.css',
})
export class TournamentDashboardComponent implements OnInit, OnChanges {

  @Input() players: string[];
  @Input() capacity: number;
  @Input() tournamentMap!: TournamentMap;
  public userIDMap: { [key: number]: boolean } = {};
  public playerNamesMap: { [key: number]: string } = {};
  public personalUserID!: number;
  public winnerName!: string;
  public winnerID: number | null = null;
  public isDataLoaded = false;

  constructor(public userService: UserService, private elementRef: ElementRef) {
    this.players = [];
    this.capacity = 0;
    this.tournamentMap = {rounds_map: {}, winner: null};
  }

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.personalUserID = this.userService.getUserID();
    await this.fetchData();
  }

  async ngOnChanges(): Promise<void> {
    await this.fetchData();
  }

  private async fetchData(): Promise<void> {
    await this.fetchUsernames().then( async (): Promise<void> => {
      if (this.tournamentMap.winner !== undefined && this.tournamentMap.winner !== null) {
        this.winnerID = this.tournamentMap.winner;
        this.winnerName = await this.userService.getUsername(this.winnerID);
      }
      this.completeFetching();
      });
  }

  private async fetchUsernames(): Promise<void> {
    const roundsMap = this.tournamentMap.rounds_map;
    for (const round in roundsMap) {
      for (const game in roundsMap[round]) {
        let userIDs = roundsMap[round][game];
        if (userIDs) {
          for (const userID of userIDs) {
            if (userID && !this.playerNamesMap[userID]) {
              this.playerNamesMap[userID] = await this.userService.getUsername(userID);
              this.userIDMap[userID] = this.personalUserID.toString() === userID.toString();
            }
          }
        }
      }
    }
  }

  private completeFetching(): void {
    this.isDataLoaded = true;
  }

  protected readonly Number = Number;
}
