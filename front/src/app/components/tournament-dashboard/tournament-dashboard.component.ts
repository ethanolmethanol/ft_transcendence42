import {Component, Input, OnInit} from '@angular/core';
import {PlayerIconComponent} from "../player-icon/player-icon.component";
import {AsyncPipe, KeyValuePipe, NgForOf, NgIf} from "@angular/common";
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
    NgIf
  ],
  templateUrl: './tournament-dashboard.component.html',
  styleUrl: './tournament-dashboard.component.css',
})
export class TournamentDashboardComponent implements OnInit {

  @Input() players: string[];
  @Input() capacity: number;
  @Input() tournamentMap!: TournamentMap;
  public playerNamesMap: { [key: number]: string } = {};
  public isDataLoaded = false;

  constructor(public userService: UserService) {
    this.players = [];
    this.capacity = 0;
    this.tournamentMap = {};
  }

  async ngOnInit(): Promise<void> {
    await this.fetchUsernames().then(
      () => {
        console.log('fetchUsernames done');
        this.isDataLoaded = true;
      }
    );
  }

  ngOnChanges(): void {
    this.fetchUsernames().then(
      () => {
        console.log('fetchUsernames done');
        this.isDataLoaded = true
      });
  }

  private async fetchUsernames(): Promise<void> {
    for (const round in this.tournamentMap) {
      for (const game in this.tournamentMap[round]) {
        let userIDs = this.tournamentMap[round][game];
        if (userIDs) {
          for (const userID of userIDs) {
            if (userID && !this.playerNamesMap[userID]) {
              this.playerNamesMap[userID] = await this.userService.getUsername(userID);
            }
          }
        }
      }
    }
  }
}
