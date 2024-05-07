import { OnDestroy, AfterViewInit, Component, HostListener, QueryList, ViewChildren} from '@angular/core';
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
} from "../../constants";
import {PaddleComponent} from "../paddle/paddle.component";
import {BallComponent} from "../ball/ball.component";
import {WebSocketService} from "../../services/web-socket/web-socket.service";
import { MonitorService } from "../../services/monitor/monitor.service";
import { ArenaResponse } from "../../interfaces/arena-response.interface";
import { Position } from "../../interfaces/position.interface";
import { ErrorResponse } from "../../interfaces/error-response.interface";
import { VariableBinding } from '@angular/compiler';
import { GameOverComponent } from '../gameover/gameover.component';
import { Router } from '@angular/router';
import {LoadingSpinnerComponent} from "../loading-spinner/loading-spinner.component";
import {NgIf} from "@angular/common";
import {ConnectionService} from "../../services/connection/connection.service";

interface PaddleUpdateResponse {
  slot: number;
  position: Position;
}

interface BallUpdateResponse {
  position: Position;
}

interface ScoreUpdateResponse {
  username: string;
}

interface GameOverUpdateResponse {
  winner: string;
  time: number;
  message: string;
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
export class GameComponent implements AfterViewInit, OnDestroy {
  gameWidth = GAME_WIDTH;
  gameHeight = GAME_HEIGHT;
  readonly lineThickness = LINE_THICKNESS;
  @ViewChildren(BallComponent) ball!: QueryList<BallComponent>;
  @ViewChildren(PaddleComponent) paddles!: QueryList<PaddleComponent>;
  @ViewChildren(GameOverComponent) overlay!: QueryList<GameOverComponent>;
  player1Score = 0;
  player2Score = 0;
  dataLoaded = false;

  private paddleBinding = [
    { id: 1, upKey: 'w', downKey: 's' },
    { id: 2, upKey: 'ArrowUp', downKey: 'ArrowDown' },
  ];
  private readonly errorMapping: ErrorMapping = {
    [NOT_JOINED]: this.redirectToHome.bind(this),
    [INVALID_ARENA]: this.redirectToHome.bind(this),
    [INVALID_CHANNEL]: this.redirectToHome.bind(this),
    [NOT_ENTERED]: this.redirectToHome.bind(this),
  };
  private pressedKeys = new Set<string>();
  constructor (private monitorService: MonitorService, private webSocketService: WebSocketService, private router: Router, private connectionService: ConnectionService) {}

  public setArena(arena: ArenaResponse) {
    this.paddles.forEach(paddle => {
      const paddleData = arena.paddles.find(p => p.slot === paddle.id);
      if (paddleData) {
        paddle.positionX = paddleData.position.x;
        paddle.positionY = paddleData.position.y;
        paddle.width = paddleData.width;
        paddle.height = paddleData.height;
        paddle.gameHeight = arena.map.height;
        paddle.gameWidth = arena.map.width;
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
    console.log('data loaded')
    this.dataLoaded = true;
  }

  private handleGameUpdate(gameState: any) {
    const variableMapping : VariableMapping = {
        'paddle': (value: PaddleUpdateResponse) => this.updatePaddle(value),
        'ball': (value: BallUpdateResponse) => { this.updateBall(value) },
        'score': (value: ScoreUpdateResponse) => { this.updateScore(value) },
        'gameover': (value: GameOverUpdateResponse) => { this.gameOver(value) },
        'arena': (value: ArenaResponse) => { this.setArena(value) },
        'status': (value: number) => { this.updateStatus(value) },
        'give_up': (value: string) => { this.giveUp(value) }
    };

    for (const variable in gameState) {
        if (variable in variableMapping) {
            variableMapping[variable](gameState[variable]);
        }
    }
  }

  private handleGameError(error: ErrorResponse) {
    console.error('Game error:', error);
    if (error.code in this.errorMapping) {
      this.errorMapping[error.code](error);
    }
  }

  private giveUp(player: string) {
    if (player == "Player_name")
      this.redirectToHome();
  }

  private updateStatus(status: number) {
    if (status == WAITING || status == DYING) {
      this.overlay.first.show = true;
    } else if (status == DEAD) {
      this.redirectToHome();
    } else {
      this.overlay.first.show = false;
    }
  }

  private updatePaddle(paddle: PaddleUpdateResponse) {
    const paddleComponent = this.paddles.find(p => p.id === paddle.slot);
    if (paddleComponent) {
      paddleComponent.updatePaddlePosition(paddle.position);
    }
  }

  private updateBall(ball: BallUpdateResponse) {
    this.ball.first.updateBallPosition(ball.position);
  }

  private updateScore(score: ScoreUpdateResponse) {
    if (this.paddles.length == 2) {
      if (score.username == "Player1")
        this.player1Score += 1;
      else this.player2Score += 1;
    }
  }

  private gameOver(info: GameOverUpdateResponse) {
    this.overlay.first.message = info.winner + " won! " + info.message
    this.overlay.first.time = info.time
    this.overlay.first.show = true
    // for online mode, use info.winner to update the user score db?

    if (info.time === 0) {
      this.redirectToHome();
    }
  }

  private redirectToHome() {
    this.overlay.first.redirectToHome();
  }

  @HostListener('window:keydown', ['$event'])
  private onKeyDown(event: KeyboardEvent) {
    this.pressedKeys.add(event.key);
  }

  @HostListener('window:keyup', ['$event'])
  private onKeyUp(event: KeyboardEvent) {
    this.pressedKeys.delete(event.key);
  }
  private gameLoop() {
    this.paddleBinding.forEach(paddleBinding => {
      const paddle = this.paddles.find(p => p.id === paddleBinding.id);
      if (paddle) {
        this.movePaddle(paddle, paddleBinding)
      }
    });

    // Call this function again on the next frame
    requestAnimationFrame(() => this.gameLoop());
  }

  private movePaddle(paddle: PaddleComponent, binding: { upKey: string; downKey: string }) {
    const isMovingUp = this.pressedKeys.has(binding.upKey) && !this.pressedKeys.has(binding.downKey);
    const isMovingDown = this.pressedKeys.has(binding.downKey) && !this.pressedKeys.has(binding.upKey);
    const direction = isMovingUp ? -1 : isMovingDown ? 1 : 0;
    if (direction !== 0) {
      const playerName = paddle.id === 1 ? "Player1" : "Player2";
      this.webSocketService.sendPaddleMovement(playerName, direction);
    }
  }

  ngAfterViewInit() {
    this.connectionService.listenToWebSocketMessages(this.handleGameUpdate.bind(this), this.handleGameError.bind(this));
    this.gameLoop();
  }

  ngOnDestroy() {
    console.log('GameComponent destroyed');
  }
}
