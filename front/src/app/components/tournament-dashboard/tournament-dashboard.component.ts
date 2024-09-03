import {Component, Input} from '@angular/core';
import {PlayerIconComponent} from "../player-icon/player-icon.component";
import {KeyValuePipe, NgForOf} from "@angular/common";
import {TournamentMap} from "../../interfaces/tournament-map.interface";

@Component({
  selector: 'app-tournament-dashboard',
  standalone: true,
  imports: [
    PlayerIconComponent,
    NgForOf,
    KeyValuePipe
  ],
  templateUrl: './tournament-dashboard.component.html',
  styleUrl: './tournament-dashboard.component.css'
})
export class TournamentDashboardComponent {

  @Input() players: string[];
  @Input() capacity: number;
  @Input() tournamentMap!: TournamentMap;

  constructor() {
    this.players = [];
    this.capacity = 0;
    this.tournamentMap = {};
  }

}
