import {
  Component,
  HostListener,
  ElementRef,
  OnInit,
  OnDestroy,
  ViewChildren,
  QueryList,
  AfterViewInit
} from '@angular/core';
import { PaddleComponent } from "../../components/paddle/paddle.component";
import { ActivatedRoute, Router, RouterLink } from "@angular/router";
import { GameComponent } from "../../components/game/game.component";
import { WebSocketService } from '../../services/web-socket/web-socket.service';
import { LoadingSpinnerComponent } from "../../components/loading-spinner/loading-spinner.component";
import { ConnectionService } from "../../services/connection/connection.service";
import { NgIf } from "@angular/common";

@Component({
  selector: 'app-game-page',
  standalone: true,
  imports: [
    PaddleComponent,
    RouterLink,
    GameComponent,
    LoadingSpinnerComponent,
    NgIf,
  ],
  templateUrl: './game-page.component.html',
  styleUrl: './game-page.component.css'
})

export class GamePageComponent implements OnInit, AfterViewInit, OnDestroy {

  isRemote: boolean | null = null;
  hasGameStarted: boolean = false;

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
    private _connectionService: ConnectionService
  ) {}

  public ngOnInit() {
    this.isRemote = this._route.snapshot.data['gameType'] === 'online';
  }

  public ngAfterViewInit() {
    this.updateGameContainerScale();
    this._route.params.subscribe(params => {
      const channel_id = params['channel_id'];
      const arena_id = params['arena_id'];
      console.log('Channel ID:', channel_id);
      this._connectionService.establishConnection(this.game.first.setArena.bind(this), channel_id, arena_id);
    });
    this.game.first.gameStarted.subscribe(() => {
      this.hasGameStarted = true;
    });
  }

  public ngOnDestroy() {
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
