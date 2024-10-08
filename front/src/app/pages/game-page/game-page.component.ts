import {
  Component,
  HostListener,
  ElementRef,
  OnInit,
  OnDestroy,
  ViewChildren,
  QueryList,
  AfterViewInit, ChangeDetectorRef
} from '@angular/core';
import { PaddleComponent } from "../../components/gameplay/paddle/paddle.component";
import { ActivatedRoute, Router, RouterLink } from "@angular/router";
import { GameComponent } from "../../components/gameplay/game/game.component";
import { WebSocketService } from '../../services/web-socket/web-socket.service';
import { LoadingSpinnerComponent } from "../../components/loading-spinner/loading-spinner.component";
import { ConnectionService } from "../../services/connection/connection.service";
import {AsyncPipe, NgForOf, NgIf} from "@angular/common";
import {GameStateService} from "../../services/game-state/game-state.service";
import {CopyButtonComponent} from "../../components/copy-button/copy-button.component";
import {PlayerIconComponent} from "../../components/player-icon/player-icon.component";

@Component({
  selector: 'app-game-page',
  standalone: true,
  imports: [
    PaddleComponent,
    RouterLink,
    GameComponent,
    LoadingSpinnerComponent,
    NgIf,
    AsyncPipe,
    CopyButtonComponent,
    NgForOf,
    PlayerIconComponent,
  ],
  templateUrl: './game-page.component.html',
  styleUrl: './game-page.component.css'
})

export class GamePageComponent implements OnInit, AfterViewInit, OnDestroy {

  arenaID: number | null = null;

  @ViewChildren(GameComponent) game!: QueryList<GameComponent>;
  @HostListener('window:resize', ['$event'])
  public onResize(event: Event) {
    this.updateGameContainerScale();
  }

  constructor(
    private _elementRef: ElementRef,
    private _router: Router,
    private _webSocketService: WebSocketService,
    private _route: ActivatedRoute,
    private _connectionService: ConnectionService,
    private cdr: ChangeDetectorRef,
    public gameStateService: GameStateService,
  ) {}

  public ngOnInit() {
    this.gameStateService.setIsRemote(this._route.snapshot.data['gameType'] === 'online');
    this.gameStateService.setIsTournament(false);
  }

  public ngAfterViewInit() {
    this.updateGameContainerScale();
    this._route.params.subscribe(params => {
      const lobby_id = params['lobby_id'];
      const arena_id = params['arena_id'];
      this.arenaID = arena_id;
      this.cdr.detectChanges();
      console.log('Lobby ID:', lobby_id);
      console.log('Arena ID:', arena_id);
      this._connectionService.establishConnection(this.game.first.setArena.bind(this), lobby_id, arena_id);
    });
  }

  public ngOnDestroy() {
    this._connectionService.endConnection();
  }

  private updateGameContainerScale() {
    this.game.first.updateScale();
  }

  public confirmGiveUp() {
    this._router.navigate(['/home']);
    this._webSocketService.giveUp();
  }
}
