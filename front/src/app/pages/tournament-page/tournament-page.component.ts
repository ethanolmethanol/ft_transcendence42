import { Component, OnInit, OnDestroy } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import { ConnectionService } from '../../services/connection/connection.service';
import {NgForOf, NgIf} from "@angular/common";
import {VariableMapping} from "../../interfaces/mapping.interface";
import {TournamentPlayer} from "../../interfaces/tournament.interface";
import {UserService} from "../../services/user/user.service";
import {CopyButtonComponent} from "../../components/copy-button/copy-button.component";
import {GameComponent} from "../../components/gameplay/game/game.component";
import {PlayerIconComponent} from "../../components/player-icon/player-icon.component";
import {WebSocketService} from "../../services/web-socket/web-socket.service";

@Component({
  selector: 'app-tournament-page',
  standalone: true,
  imports: [
    NgIf,
    NgForOf,
    CopyButtonComponent,
    GameComponent,
    PlayerIconComponent
  ],
  templateUrl: './tournament-page.component.html',
  styleUrl: './tournament-page.component.css'
})
export class TournamentPageComponent implements OnInit, OnDestroy {
  private channelID?: string;
  public players: string[] = [];
  public isLoading: boolean = true;

  constructor(
    private _route: ActivatedRoute,
    private _connectionService: ConnectionService,
    private _userService: UserService,
    private _router: Router,
    private _webSocketService: WebSocketService
  ) {}

  async ngOnInit(): Promise<void> {
    await this._userService.whenUserDataLoaded();
    this.channelID = this._route.snapshot.params['channel_id'];
    this._connectionService.establishConnection(this.handleGameUpdate.bind(this), this.channelID, null);
    this._connectionService.listenToWebSocketMessages(
      this.handleGameUpdate.bind(this),
      this.handleGameError.bind(this)
    );
  }

  ngOnDestroy() {
    this._connectionService.endConnection();
  }

  private handleGameUpdate(update: any) {
    const variableMapping : VariableMapping = {
      'channel_players': (value: TournamentPlayer[]) => this.updateConnectedPlayers(value),
    };

    for (const variable in update) {
      if (variable in variableMapping) {
        variableMapping[variable](update[variable]);
      }
    }
    this.isLoading = false;
  }

  private async updateConnectedPlayers(players: TournamentPlayer[]) {
    this.players = await Promise.all(
      players.map(async player => await this._userService.getUsername(player.user_id)));
  }

  private handleGameError(error: any) {
    console.error('WebSocket error:', error);
    this.isLoading = false;
  }

  public confirmGiveUp() {
    this._router.navigate(['/home']);
    this._webSocketService.disconnect();
  }
}
