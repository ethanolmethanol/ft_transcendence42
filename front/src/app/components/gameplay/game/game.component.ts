import {
  OnDestroy,
  AfterViewInit,
  Component,
  HostListener,
  QueryList,
  ViewChildren,
  Input,
  Renderer2,
  ElementRef, EventEmitter, Output, OnInit,
} from '@angular/core';
import {
  NOT_JOINED,
  INVALID_ARENA,
  INVALID_LOBBY,
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
import { AsyncPipe, NgForOf, NgIf } from "@angular/common";
import { ConnectionService } from "../../../services/connection/connection.service";
import { UserService } from "../../../services/user/user.service";
import { PlayerIconComponent } from "../../player-icon/player-icon.component";
import { StartTimerComponent } from "../start-timer/start-timer.component";
import * as Constants from "../../../constants";
import { CopyButtonComponent } from "../../copy-button/copy-button.component";
import { GameStateService } from "../../../services/game-state/game-state.service";
import { map, Subscription } from "rxjs";
import { ActivatedRoute, Router } from "@angular/router";
import { AssignationsResponse } from "../../../interfaces/assignation.interface";
import { User } from "../../../interfaces/user";
import { isEmptyObject } from "../../../utils/object";
import { AvatarComponent } from "../../avatar/avatar.component";

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

interface LobbyPlayersResponse {
  user_id: number[];
  capacity: number;
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
    AvatarComponent,
  ],
  templateUrl: './game.component.html',
  styleUrl: './game.component.css'
})
export class GameComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChildren(BallComponent) ball!: QueryList<BallComponent>;
  @ViewChildren(PaddleComponent) paddles!: QueryList<PaddleComponent>;
  @ViewChildren(StartTimerComponent) startTimer!: QueryList<StartTimerComponent>;
  @ViewChildren(GameOverComponent) gameOver!: QueryList<GameOverComponent>;
  @ViewChildren(AvatarComponent) avatars!: QueryList<AvatarComponent>;
  @Input() arenaID: number = -1;
  private playerName: string | null = null;
  private isRemote: boolean = false;
  private isTournament: boolean = false;
  private lobbyID: string = '';
  private lobbySubscription: Subscription | null = null;
  private activePlayersSubscription: Subscription | null = null;
  readonly lineThickness: number = LINE_THICKNESS;
  gameWidth: number = GAME_WIDTH;
  gameHeight: number = GAME_HEIGHT;
  player1Score: number = 0;
  player2Score: number = 0;
  bots: string[] = [];
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
    [INVALID_LOBBY]: this.redirectToHome.bind(this),
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
    private route: ActivatedRoute,
    private router: Router,
    public gameStateService: GameStateService,
  ) {}

  public updateScale(): void {
    const gameContainer = this.el.nativeElement.querySelector('.game-container');
    const scale = Math.min(window.innerWidth / 1800, window.innerHeight / 1000);
    gameContainer.style.transform = `scale(${scale})`;
  }

  async ngOnInit(): Promise<void> {
    this.gameStateService.isRemote$.subscribe(isRemote => {
      this.isRemote = isRemote;
    });
    this.gameStateService.isTournament$.subscribe(isTournament => {
      this.isTournament = isTournament;
    });
    this.gameStateService.lobbyID$.subscribe(lobbyID => {
      this.lobbyID = lobbyID;
    });
    if (this.isRemote) {
      await this.userService.whenUserDataLoaded();
      this.playerName = await this.userService.getUsername();
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
    this.paddles.forEach((paddle, index) => {
      // console.log("Index = ", index);
      const paddleData = arena.paddles.find(p => p.slot === paddle.id);
      if (paddleData) {
        paddle.playerName = paddleData.player_name;
        paddle.positionX = paddleData.position.x;
        paddle.positionY = paddleData.position.y;
        paddle.width = paddleData.width;
        paddle.height = paddleData.height;
        paddle.afkLeftTime = null;
        const avatar = this.avatars.toArray()[index];
        if (avatar) {
          avatar.updateAvatar(paddle.playerName);
        }
      }
    });
    this.ball.first.positionX = arena.ball.position.x;
    this.ball.first.positionY = arena.ball.position.y;
    this.ball.first.ballSize = 2 * arena.ball.radius;
    this.ball.first.gameHeight = arena.map.height;
    this.ball.first.gameWidth = arena.map.width;
    this.gameHeight = arena.map.height;
    this.gameWidth = arena.map.width;
    this.player1Score = arena.scores[0];
    this.player2Score = arena.scores[1];
    this.gameStateService.setMaxPlayers(arena.players_specs.nb_players)
    this.updateStatus(arena.status)
    this.gameStateService.setActivePlayers(arena.players);
    this.gameStateService.setDataLoaded(true);
    this.bots = arena.players_specs.bots;
    this.startTimer.first.show = false;
  }

  private async handleGameUpdate(gameState: any) {
    const variableMappingArena : VariableMapping = {
        'paddle': (value: PaddleUpdateResponse) => this.updatePaddle(value),
        'ball': (value: BallUpdateResponse) => { this.updateBall(value) },
        'score': (value: ScoreUpdateResponse) => { this.updateScore(value) },
        'start_timer': (value: StartTimerResponse) => { this.updateStartTimer(value) },
        'game_over': (value: GameOverUpdateResponse) => { this.updateGameOver(value) },
        'arena': (value: ArenaResponse) => { this.setArena(value) },
        'status': (value: number) => { this.updateStatus(value) },
        'give_up': (value: number) => { this.giveUp(value) },
        'kicked_players': (value: Array<AFKResponse>) => { this.updateInactivity(value) },
    };
    const variableMappingLobby : VariableMapping = {
      'lobby_players': async (value: LobbyPlayersResponse) => {
        await this.updateLobbyPlayers(value);
      },
      'assignations': (value: AssignationsResponse) => {
        this.handleRedirection(value);
      },
      'tournament_map': (value: any) => {
        this.gameStateService.setTournamentMap(value);
        console.log('Tournament map:', value);
      },
    };

    await this.__updateGameState(gameState, variableMappingLobby);
    if (gameState['arena_id'] !== this.arenaID) {
      return;
    }
    await this.__updateGameState(gameState, variableMappingArena);
  }

  private async updateLobbyPlayers(players: LobbyPlayersResponse) {
    let playerList: string[] = []
    for (const user_id of players.user_id) {
      const user: User = await this.userService.getUser(user_id)
      const player_name: string = user.username
      playerList.push(player_name)
    }
    if (players.capacity == playerList.length) {
      this.gameStateService.setCanGiveUp(false)
    }
    this.gameStateService.setLobbyPlayers(playerList)
    this.gameStateService.setLobbyCapacity(players.capacity)
    this.gameStateService.setDataLoaded(true)
  }

  private async __updateGameState(gameState: any, variableMapping: VariableMapping) {
    for (const variable in gameState) {
      if (variable in variableMapping) {
        await variableMapping[variable](gameState[variable]);
      }
    }
  }

  private handleRedirection(response: AssignationsResponse) {
    const { actionType } = this.route.snapshot.data;
    if (actionType !== 'tournament') return;

    if (isEmptyObject(response)) {
      console.log('Redirecting to home');
      this.redirectToHome();
    }

    console.log("Handle redirection", response);
    const userID = this.userService.getUserID();
    const arena = response[userID];
    if (arena && arena.status != DYING && arena.status != DEAD) {
        console.log('Redirecting to:', this.lobbyID, arena.id);
        this.router.navigate(['/online/tournament', this.lobbyID, arena.id]);
    }
  }

  private updateStartTimer(timer: StartTimerResponse) {
    this.gameStateService.setCanGiveUp(false);
    this.startTimer.first.message = timer.message;
    this.startTimer.first.time = timer.time;
    this.startTimer.first.show = true;
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
    this.gameStateService.setCanGiveUp(true);
  }

  private updateStatus(status: number) {
    let gameOverOverlay: GameOverComponent = this.gameOver.first;
    const isWaiting = status == CREATED || status == WAITING;
    this.gameStateService.setIsWaiting(isWaiting)
    if (status == STARTED) {
      this.handleStartCounterCompletion()
      gameOverOverlay.show = false;
    } else if (status == DYING || status == DEAD) {
      if (this.isTournament) {
        this.redirectToLobby();
        return;
      }
      if (status == DYING) {
        gameOverOverlay.show = true;
      } else if (status == DEAD) {
        this.redirectToHome();
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
    this.activePlayersSubscription = this.gameStateService.activePlayers$.pipe(
      map(players => players.find((name: string) => name === this.playerName))
    ).subscribe(foundPlayer => player = foundPlayer);
      if (info.winner === "") {
        gameOverOverlay.message = "It's a tie! " + info.message
      } else {
        gameOverOverlay.message = info.winner + " won! " + info.message
      }
      gameOverOverlay.time = info.time
      gameOverOverlay.show = true;
      // for online mode, use info.winner to update the user score db?

      if (info.time === 0) {
        this.redirectToHome();
      }
  }

  private redirectToHome() {
    this.gameStateService.reset();
    this.router.navigate(['/home']);
  }

  private redirectToLobby() {
    this.gameStateService.reset();
    const arenaID = this.route.snapshot.params['arena_id'];
    console.log('Arena ID:', arenaID)
    if (arenaID) {
      console.log('Redirecting to lobby');
      this.router.navigate(['/online/tournament/', this.connectionService.getLobbyID()]);
    }
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

    if ((isMovingUp && isMovingDown) || this.bots.includes(playerName)) {
      return;
    }
    const direction = isMovingUp ? -1 : isMovingDown ? 1 : 0;
    if (direction !== 0) {
      this.webSocketService.sendPaddleMovement(playerName, direction);
    }
  }

  async ngAfterViewInit() : Promise<void> {
    console.log('GameComponent created');
    await this.userService.whenUserDataLoaded();
    await this.connectionService.listenToWebSocketMessages(
      this.handleGameUpdate.bind(this), this.handleGameError.bind(this)
    );
    this.gameStateService.setLobbyID(this.connectionService.getLobbyID());
    this._setGameStyle();
    this.gameLoop()
  }

  ngOnDestroy() {
    if (this.lobbySubscription) {
      this.lobbySubscription.unsubscribe();
    }
    if (this.activePlayersSubscription) {
      this.activePlayersSubscription.unsubscribe();
    }
    this.gameStateService.restrictReset();
    console.log('GameComponent destroyed');
  }

  protected readonly length = length;
}

