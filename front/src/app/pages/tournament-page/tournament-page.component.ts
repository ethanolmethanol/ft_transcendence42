import {
  AfterViewInit, ChangeDetectorRef,
  Component,
  ElementRef,
  HostListener,
  OnDestroy,
  OnInit,
  QueryList,
  ViewChildren
} from '@angular/core';
import {GameComponent} from "../../components/gameplay/game/game.component";
import {ActivatedRoute, Router} from "@angular/router";
import {WebSocketService} from "../../services/web-socket/web-socket.service";
import {ConnectionService} from "../../services/connection/connection.service";
import {AsyncPipe, NgForOf, NgIf} from "@angular/common";
import {PlayerIconComponent} from "../../components/player-icon/player-icon.component";
import {GameStateService} from "../../services/game-state/game-state.service";
import {TournamentDashboardComponent} from "../../components/tournament-dashboard/tournament-dashboard.component";

@Component({
  selector: 'app-tournament-page',
  standalone: true,
  imports: [
    GameComponent,
    NgIf,
    AsyncPipe,
    NgForOf,
    PlayerIconComponent,
    TournamentDashboardComponent
  ],
  templateUrl: './tournament-page.component.html',
  styleUrl: './tournament-page.component.css'
})
export class TournamentPageComponent implements OnInit, AfterViewInit, OnDestroy {
  canGiveUp: boolean = true;
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
    public gameStateService: GameStateService
  ) {
    console.log('TournamentPageComponent created')
  }

  public ngOnInit() {
    this.gameStateService.setIsRemote(this._route.snapshot.data['gameType'] === 'online');
    this.gameStateService.setIsTournament(true);
  }

  public ngAfterViewInit()  {
    this.updateGameContainerScale();
    this._route.params.subscribe(params => {
      const channel_id = params['channel_id'];
      const arena_id = params['arena_id'];
      this.arenaID = arena_id;
      this.cdr.detectChanges();
      this._connectionService.establishConnection(this.game.first.setArena.bind(this), channel_id, arena_id, true);
    });
    this.game.first.startCounterStarted.subscribe(() => {
      this.canGiveUp = false;
    });
    this.game.first.hasStarted.subscribe(() => {
      this.canGiveUp = true;
    });
  }

  public ngOnDestroy() {
    console.log('TournamentPageComponent destroyed')
    this._connectionService.endConnection();
  }

  private updateGameContainerScale() {
    const gameContainer = this._elementRef.nativeElement.querySelector('.game-container');
    const scale = Math.min(window.innerWidth / 1000, window.innerHeight / 1000);
    gameContainer.style.transform = `scale(${scale})`;
  }

  public confirmGiveUp() {
    this._router.navigate(['/home']);
    this._webSocketService.giveUp();
  }
}