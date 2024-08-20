import {
  OnDestroy,
  AfterViewInit,
  Component,
  HostListener,
  QueryList,
  ViewChildren,
  Input,
  SimpleChanges,
  OnChanges,
  Renderer2,
  ElementRef, EventEmitter, Output, OnInit,
} from '@angular/core';
import {
  NOT_JOINED,
  INVALID_ARENA,
  INVALID_CHANNEL,
  NOT_ENTERED,
  GAME_HEIGHT,
  GAME_WIDTH,
  LINE_THICKNESS,
  WAITING,
  DYING,
  DEAD,
  GIVEN_UP,
  STARTED, CREATED,
} from "../../../constants";
import { PaddleComponent } from "../paddle/paddle.component";
import { BallComponent } from "../ball/ball.component";
import { WebSocketService } from "../../../services/web-socket/web-socket.service";
import { ArenaResponse } from "../../../interfaces/arena-response.interface";
import { Position } from "../../../interfaces/position.interface";
import { ErrorResponse } from "../../../interfaces/error-response.interface";
import { GameOverComponent } from '../gameover/gameover.component';
import { LoadingSpinnerComponent } from "../../loading-spinner/loading-spinner.component";
import {AsyncPipe, NgForOf, NgIf} from "@angular/common";
import { ConnectionService } from "../../../services/connection/connection.service";
import { UserService } from "../../../services/user/user.service";
import { PlayerIconComponent } from "../../player-icon/player-icon.component";
import { StartTimerComponent } from "../start-timer/start-timer.component";
import * as Constants from "../../../constants";
import { CopyButtonComponent } from "../../copy-button/copy-button.component";
import {GameStateService} from "../../../services/game-state/game-state.service";
import {map} from "rxjs";

interface PaddleUpdateResponse {
  slot: number;
  position: Position;
}

interface BallUpdateResponse {
  position: Position;
}

interface ScoreUpdateResponse {
  player_name: string;
}

interface StartTimerResponse {
  time: number;
  message: string;
}

interface GameOverUpdateResponse {
  players: string[];
  winner: string;
  time: number;
  message: string;
}

interface AFKResponse {
  player_name: string;
  time_left: number;
}

interface VariableMapping {
  [key: string]: (value: any) => void;
}

interface ErrorMapping {
  [key: number]: (value: ErrorResponse) => void;
}

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [
    PaddleComponent,
    BallComponent,
    GameOverComponent,
    LoadingSpinnerComponent,
    NgIf,
    NgForOf,
    PlayerIconComponent,
    StartTimerComponent,
    CopyButtonComponent,
    AsyncPipe,
  ],
  templateUrl: './game.component.html',
  styleUrl: './game.component.css'
})
export class GameComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChildren(BallComponent) ball!: QueryList<BallComponent>;
  @ViewChildren(PaddleComponent) paddles!: QueryList<PaddleComponent>;
  @ViewChildren(StartTimerComponent) startTimer!: QueryList<StartTimerComponent>;
  @ViewChildren(GameOverComponent) gameOver!: QueryList<GameOverComponent>;
  @Input() arenaID: number = -1;
  @Output() hasStarted = new EventEmitter<void>();
  @Output() startCounterStarted = new EventEmitter<void>();
  private playerName: string | null = null;
  private isRemote: boolean = false;
  readonly lineThickness: number = LINE_THICKNESS;
  gameWidth: number = GAME_WIDTH;
  gameHeight: number = GAME_HEIGHT;
  player1Score: number = 0;
  player2Score: number = 0;
  constants = Constants;

  private _localPaddleBinding = [
    { id: 1, upKey: 'w', downKey: 's' },
    { id: 2, upKey: 'ArrowUp', downKey: 'ArrowDown' },
  ];
  private _remotePaddleBinding = [
    { id: 1, upKey: 'w', downKey: 's' },
  ];
  private readonly _errorMapping: ErrorMapping = {
    [NOT_JOINED]: this.redirectToHome.bind(this),
    [INVALID_ARENA]: this.redirectToHome.bind(this),
    [INVALID_CHANNEL]: this.redirectToHome.bind(this),
    [NOT_ENTERED]: this.redirectToHome.bind(this),
    [GIVEN_UP]: this.redirectToHome.bind(this),
  };
  private _pressedKeys = new Set<string>();

  constructor (
    private userService: UserService,
    private webSocketService: WebSocketService,
    private connectionService: ConnectionService,
    private renderer: Renderer2,
    private el: ElementRef,
    public gameStateService: GameStateService,
  ) {}

  async ngOnInit(): Promise<void> {
    this.gameStateService.isRemote$.subscribe(isRemote => {
      this.isRemote = isRemote;
    });
    if (this.isRemote) {
      await this.userService.whenUserDataLoaded();
      this.playerName = this.userService.getUsername();
      console.log('Player name:', this.playerName);
    }
  }

  private _setGameStyle(): void {
    const gameBoardColors: string[] = this.userService.getColorConfig();

    this._setStyle('.game-area', 'background', `linear-gradient(${gameBoardColors[Constants.BACKGROUND_COLOR1]}, ${gameBoardColors[Constants.BACKGROUND_COLOR2]})`);
    this._setStyle('.game-area', 'border', `6px solid ${gameBoardColors[Constants.LINE_COLOR]}`);
    this._setStyle('.game', 'background', `linear-gradient(${gameBoardColors[Constants.BACKGROUND_COLOR1]}, ${gameBoardColors[Constants.BACKGROUND_COLOR2]})`);
    this._setStyle('.dotted-line', '--line-thickness', `${this.lineThickness}px`);
    this._setStyle('.dotted-line', 'background', `linear-gradient(to bottom, ${gameBoardColors[Constants.LINE_COLOR]} 60%, transparent 10%)`);
    this._setStyle('.dotted-line', 'background-size', '100% 40px');
    this._setStyle('.score-display', 'color', gameBoardColors[Constants.SCORE_COLOR]);

    this.paddles.forEach(paddle => {
      paddle.setColor(gameBoardColors[Constants.PADDLE_COLOR]);
    });
    this.ball.forEach(ball => {
      ball.setColor(gameBoardColors[Constants.BALL_COLOR]);
    });
  }

  private _setStyle(selector: string, styleName: string, styleValue: string) {
    const element = this.el.nativeElement.querySelector(selector);
    if (element)
      this.renderer.setStyle(element, styleName, styleValue);
  }

  public setArena(arena: ArenaResponse) {
    this.paddles.forEach(paddle => {
      const paddleData = arena.paddles.find(p => p.slot === paddle.id);
      if (paddleData) {
        paddle.playerName = paddleData.player_name;
        paddle.positionX = paddleData.position.x;
        paddle.positionY = paddleData.position.y;
        paddle.width = paddleData.width;
        paddle.height = paddleData.height;
        paddle.afkLeftTime = null;
      }
    });
    this.ball.first.positionX = arena.ball.position.x;
    this.ball.first.positionY = arena.ball.position.y;
    this.ball.first.ballSize = 2 * arena.ball.radius;
    this.gameHeight = arena.map.height;
    this.gameWidth = arena.map.width;
    this.player1Score = arena.scores[0];
    this.player2Score = arena.scores[1];
    this.gameStateService.setMaxPlayers(arena.players_specs.nb_players)
    this.updateStatus(arena.status)
    this.gameStateService.setActivePlayers(arena.players);
    this.gameStateService.setDataLoaded(true);
    this.startTimer.first.show = false;
    this.gameOver.first.hasRematched = false;
  }

  private handleGameUpdate(gameState: any) {
    const variableMapping : VariableMapping = {
        'paddle': (value: PaddleUpdateResponse) => this.updatePaddle(value),
        'ball': (value: BallUpdateResponse) => { this.updateBall(value) },
        'score': (value: ScoreUpdateResponse) => { this.updateScore(value) },
        'start_timer': (value: StartTimerResponse) => { this.updateStartTimer(value) },
        'game_over': (value: GameOverUpdateResponse) => { this.updateGameOver(value) },
        'arena': (value: ArenaResponse) => { this.setArena(value) },
        'status': (value: number) => { this.updateStatus(value) },
        'give_up': (value: number) => { this.giveUp(value) },
        'kicked_players': (value: Array<AFKResponse>) => { this.updateInactivity(value) }
    };

    if (gameState['arena_id'] !== this.arenaID) {
      return;
    }

    for (const variable in gameState) {
        if (variable in variableMapping) {
            variableMapping[variable](gameState[variable]);
        }
    }
  }

  private updateStartTimer(timer: StartTimerResponse) {
    this.startTimer.first.message = timer.message;
    this.startTimer.first.time = timer.time;
    this.startTimer.first.show = true;
    this.startCounterStarted.emit();
  }

  private updateInactivity(kicked_players: Array<AFKResponse>) {
    kicked_players.forEach((afkResponse) => {
      const paddle = this.paddles.find(p => p.playerName === afkResponse.player_name);
      if (paddle) {
        if (afkResponse.time_left <= 0) {
          if (!this.isRemote || afkResponse.player_name === this.playerName) {
            this.redirectToHome();
            this.webSocketService.giveUp();
          }
        } else {
          const left_time = afkResponse.time_left;
          paddle.afkLeftTime = left_time;
        }
      }
    });
  }

  private handleGameError(error: ErrorResponse) {
    console.error('Game error:', error);
    if (error.code in this._errorMapping) {
      this._errorMapping[error.code](error);
    }
  }

  private giveUp(user_id: number) {
    if (user_id == this.userService.getUserID()) {
      this.redirectToHome();
    }
  }

  private handleStartCounterCompletion() {
    if (this.hasStarted.observed) {
      this.hasStarted.emit();
    }
  }

  private updateStatus(status: number) {
    let gameOverOverlay = this.gameOver.first;
    this.gameStateService.setIsWaiting(status == CREATED || status == WAITING)
    if (gameOverOverlay.hasRematched === false) {
      if (status == DYING) {
        gameOverOverlay.show = true;
      } else if (status == DEAD) {
        this.redirectToHome();
      } else if (status == STARTED) {
        this.handleStartCounterCompletion()
        gameOverOverlay.show = false;
      }
    }
  }

  private updatePaddle(paddle: PaddleUpdateResponse) {
    const paddleComponent = this.paddles.find(p => p.id === paddle.slot);
    if (paddleComponent) {
      paddleComponent.afkLeftTime = null;
      paddleComponent.updatePaddlePosition(paddle.position);
    }
  }

  private updateBall(ball: BallUpdateResponse) {
    this.ball.first.updateBallPosition(ball.position);
  }

  private updateScore(score: ScoreUpdateResponse) {
    const paddleComponent = this.paddles.find(p => p.playerName === score.player_name);
    if (paddleComponent) {
      if (paddleComponent.id === 1) {
        this.player1Score += 1;
      } else if (paddleComponent.id === 2) {
        this.player2Score += 1;
      }
    }
  }

  private updateGameOver(info: GameOverUpdateResponse) {
    let gameOverOverlay = this.gameOver.first;
    let player: string | undefined;
    this.gameStateService.activePlayers$.pipe(
      map(players => players.find((name: string) => name === this.playerName))
    ).subscribe(foundPlayer => player = foundPlayer);
    if (this.isRemote && player) {
      gameOverOverlay.hasRematched = true;
    }
    if (gameOverOverlay.hasRematched === false) {
      if (info.winner === "") {
        gameOverOverlay.message = "It's a tie! " + info.message
      } else {
        gameOverOverlay.message = info.winner + " won! " + info.message
      }
      gameOverOverlay.time = info.time
      gameOverOverlay.show = true
      // for online mode, use info.winner to update the user score db?

      if (info.time === 0) {
        this.redirectToHome();
      }
    }
  }

  private redirectToHome() {
    this.gameOver.first.redirectToHome();
  }

  @HostListener('window:keydown', ['$event'])
  private onKeyDown(event: KeyboardEvent) {
    this._pressedKeys.add(event.key);
  }

  @HostListener('window:keyup', ['$event'])
  private onKeyUp(event: KeyboardEvent) {
    this._pressedKeys.delete(event.key);
  }
  private gameLoop() {
    let bindingMap;
    if (this.isRemote) {
      bindingMap = this._remotePaddleBinding;
    } else {
      bindingMap = this._localPaddleBinding;
    }
    bindingMap.forEach(bindingMap => {
      const paddle = this.paddles.find(p => p.id === bindingMap.id);
      if (paddle) {
        let playerName;
        if (this.isRemote) {
          playerName = this.playerName!;
        } else {
          playerName = paddle.playerName;
        }
        this.movePaddle(playerName, bindingMap)
      }
    });

    // Call this function again on the next frame
    requestAnimationFrame(() => this.gameLoop());
  }

  private movePaddle(playerName: string, binding: { upKey: string; downKey: string }) {
    const isMovingUp = this._pressedKeys.has(binding.upKey);
    const isMovingDown = this._pressedKeys.has(binding.downKey);

    if (isMovingUp && isMovingDown) {
      return;
    }
    const direction = isMovingUp ? -1 : isMovingDown ? 1 : 0;
    if (direction !== 0) {
      this.webSocketService.sendPaddleMovement(playerName, direction);
    }
  }

  async ngAfterViewInit() : Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.connectionService.listenToWebSocketMessages(this.handleGameUpdate.bind(this), this.handleGameError.bind(this));
    this.gameStateService.setChannelID(this.connectionService.getChannelID());
    this._setGameStyle();
    this.gameLoop()
  }

  ngOnDestroy() {
    console.log('GameComponent destroyed');
  }

  protected readonly length = length;
}

