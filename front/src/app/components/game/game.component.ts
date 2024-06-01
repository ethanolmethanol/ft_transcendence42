import {
  OnDestroy,
  AfterViewInit,
  Component,
  HostListener,
  QueryList,
  ViewChildren,
  Input,
  SimpleChanges, OnChanges
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
  STARTED,
} from "../../constants";
import {PaddleComponent} from "../paddle/paddle.component";
import {BallComponent} from "../ball/ball.component";
import {WebSocketService} from "../../services/web-socket/web-socket.service";
import { ArenaResponse } from "../../interfaces/arena-response.interface";
import { Position } from "../../interfaces/position.interface";
import { ErrorResponse } from "../../interfaces/error-response.interface";
import { GameOverComponent } from '../gameover/gameover.component';
import { Router } from '@angular/router';
import {LoadingSpinnerComponent} from "../loading-spinner/loading-spinner.component";
import {NgIf} from "@angular/common";
import {ConnectionService} from "../../services/connection/connection.service";
import {UserService} from "../../services/user/user.service";

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

interface GameOverUpdateResponse {
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
    NgIf
  ],
  templateUrl: './game.component.html',
  styleUrl: './game.component.css'
})
export class GameComponent implements AfterViewInit, OnDestroy, OnChanges {
  @ViewChildren(BallComponent) ball!: QueryList<BallComponent>;
  @ViewChildren(PaddleComponent) paddles!: QueryList<PaddleComponent>;
  @ViewChildren(GameOverComponent) overlay!: QueryList<GameOverComponent>;
  @Input() is_remote: boolean = false;
  private playerName: string | null = null;
  readonly lineThickness: number = LINE_THICKNESS;
  gameWidth: number = GAME_WIDTH;
  gameHeight: number = GAME_HEIGHT;
  player1Score: number = 0;
  player2Score: number = 0;
  dataLoaded: boolean = false;
  isWaiting: boolean = true;
  waitingPlayers: string[] = [];

  private _paddleBinding = [
    { id: 1, upKey: 'w', downKey: 's' },
    { id: 2, upKey: 'ArrowUp', downKey: 'ArrowDown' },
  ];
  private readonly _errorMapping: ErrorMapping = {
    [NOT_JOINED]: this.redirectToHome.bind(this),
    [INVALID_ARENA]: this.redirectToHome.bind(this),
    [INVALID_CHANNEL]: this.redirectToHome.bind(this),
    [NOT_ENTERED]: this.redirectToHome.bind(this),
    [GIVEN_UP]: this.redirectToHome.bind(this),
  };
  private _pressedKeys = new Set<string>();
  constructor (private userService: UserService, private webSocketService: WebSocketService, private router: Router, private connectionService: ConnectionService) {}

  async ngOnChanges(changes: SimpleChanges) {
    if (changes.is_remote && this.is_remote) {
      await this.userService.whenUserDataLoaded();
      this.playerName = this.userService.getUsername();
    }
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
        console.log(paddle.playerName + " joined the game.");
      }
    });
    this.ball.first.positionX = arena.ball.position.x;
    this.ball.first.positionY = arena.ball.position.y;
    this.ball.first.ballSize = 2 * arena.ball.radius;
    this.gameHeight = arena.map.height;
    this.gameWidth = arena.map.width;
    this.player1Score = arena.scores[0];
    this.player2Score = arena.scores[1];
    this.updateStatus(arena.status)
    if (arena.status == WAITING) {
      this.waitingPlayers = arena.players;
    } else if (arena.status == STARTED) {
      this.overlay.first.hasRematched = false;
    }
    this.dataLoaded = true;
  }

  private handleGameUpdate(gameState: any) {
    const variableMapping : VariableMapping = {
        'paddle': (value: PaddleUpdateResponse) => this.updatePaddle(value),
        'ball': (value: BallUpdateResponse) => { this.updateBall(value) },
        'score': (value: ScoreUpdateResponse) => { this.updateScore(value) },
        'game_over': (value: GameOverUpdateResponse) => { this.gameOver(value) },
        'arena': (value: ArenaResponse) => { this.setArena(value) },
        'status': (value: number) => { this.updateStatus(value) },
        'give_up': (value: number) => { this.giveUp(value) },
        'kicked_players': (value: Array<AFKResponse>) => { this.updateInactivity(value) }
    };

    for (const variable in gameState) {
        if (variable in variableMapping) {
            variableMapping[variable](gameState[variable]);
        }
    }
  }

  private updateInactivity(kicked_players: Array<AFKResponse>) {
    kicked_players.forEach((afkResponse) => {
      const paddle = this.paddles.find(p => p.playerName === afkResponse.player_name);
      if (paddle) {
        if (afkResponse.time_left <= 0) {
          if (afkResponse.player_name === this.playerName) {
            console.log('You were kicked due to inactivity.');
            this.redirectToHome();
            this.webSocketService.giveUp();
          }
        } else {
          const left_time = afkResponse.time_left;
          console.log("Warning: " + afkResponse.player_name + " will be kicked in " + left_time + " seconds.");
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

  private updateStatus(status: number) {
    let gameOverOverlay = this.overlay.first;
    this.isWaiting = (status == WAITING)
    if (gameOverOverlay.hasRematched === false) {
      if (status == DYING) {
        gameOverOverlay.show = true;
      } else if (status == DEAD) {
        this.redirectToHome();
      } else {
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

  private gameOver(info: GameOverUpdateResponse) {
    let gameOverOverlay = this.overlay.first;
    if (gameOverOverlay.hasRematched === false) {
      gameOverOverlay.message = info.winner + " won! " + info.message
      gameOverOverlay.time = info.time
      gameOverOverlay.show = true
      // for online mode, use info.winner to update the user score db?

      if (info.time === 0) {
        this.redirectToHome();
      }
    }
  }

  private redirectToHome() {
    this.overlay.first.redirectToHome();
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
    this._paddleBinding.forEach(_paddleBinding => {
      const paddle = this.paddles.find(p => p.id === _paddleBinding.id);
      if (paddle) {
        this.movePaddle(paddle, _paddleBinding)
      }
    });

    // Call this function again on the next frame
    requestAnimationFrame(() => this.gameLoop());
  }

  private movePaddle(paddle: PaddleComponent, binding: { upKey: string; downKey: string }) {
    const isMovingUp = this._pressedKeys.has(binding.upKey) && !this._pressedKeys.has(binding.downKey);
    const isMovingDown = this._pressedKeys.has(binding.downKey) && !this._pressedKeys.has(binding.upKey);
    const direction = isMovingUp ? -1 : isMovingDown ? 1 : 0;
    if (direction !== 0) {
      let playerName;
      if (this.is_remote) {
        playerName = this.playerName!;
      } else {
        playerName = paddle.playerName;
      }
      this.webSocketService.sendPaddleMovement(playerName, direction);
    }
  }

  async ngAfterViewInit() : Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.connectionService.listenToWebSocketMessages(this.handleGameUpdate.bind(this), this.handleGameError.bind(this));
    this.gameLoop();
  }

  ngOnDestroy() {
    console.log('GameComponent destroyed');
  }
}

