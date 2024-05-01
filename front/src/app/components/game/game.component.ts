import { OnDestroy, AfterViewInit, Component, HostListener, QueryList, ViewChildren} from '@angular/core';
import {GAME_HEIGHT, GAME_WIDTH, LINE_THICKNESS, WAITING, STARTED, OVER, DYING, DEAD} from "../../constants";
import {PaddleComponent} from "../paddle/paddle.component";
import {BallComponent} from "../ball/ball.component";
import {WebSocketService} from "../../services/web-socket/web-socket.service";
import { MonitorService } from "../../services/monitor/monitor.service";
import { ConnectionComponent } from "./connection.component";
import { ArenaResponse } from "../../interfaces/arena-response.interface";
import { Position } from "../../interfaces/position.interface";
import { VariableBinding } from '@angular/compiler';
import { GameOverComponent } from '../gameover/gameover.component';
import { Router } from '@angular/router';

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

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [
    PaddleComponent,
    BallComponent,
    GameOverComponent
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
  private connection!: ConnectionComponent;
  // players!: string[];
  player1Score = 0;
  player2Score = 0;

  private paddleBinding = [
    { id: 1, upKey: 'w', downKey: 's' },
    { id: 2, upKey: 'ArrowUp', downKey: 'ArrowDown' },
  ];
  private pressedKeys = new Set<string>();

  constructor (private monitorService: MonitorService, private webSocketService: WebSocketService, private router: Router) {
    this.connection = new ConnectionComponent(monitorService, webSocketService);
    this.connection.establishConnection(this.setArena.bind(this));
  }

  private setArena(arena: ArenaResponse) {
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
    this.overlay.first.show = (arena.status != STARTED)
  }

  private handleGameUpdate(gameState: any) {
    const variableMapping : VariableMapping = {
        'paddle': (value: PaddleUpdateResponse) => this.updatePaddle(value),
        'ball': (value: BallUpdateResponse) => { this.updateBall(value) },
        'score': (value: ScoreUpdateResponse) => { this.updateScore(value) },
        'gameover': (value: GameOverUpdateResponse) => { this.gameOver(value) },
        'arena': (value: ArenaResponse) => { this.setArena(value) },
        'status': (value: number) => { this.updateStatus(value) }
    };

    for (const variable in gameState) {
        if (variable in variableMapping) {
            variableMapping[variable](gameState[variable]);
        }
    }
  }

  private updateStatus(status: number) {
    if (status == STARTED) {
      this.overlay.first.show = false;
    }
    // this.overlay.first.show = (status == WAITING || status == DYING)
    // if (status == STARTED) {
    //   this.overlay.first.time = 10;
    // }
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
      this.overlay.first.backToHomePage();
    }
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
    this.connection.listenToWebSocketMessages(this.handleGameUpdate.bind(this));
    this.gameLoop();
  }

  ngOnDestroy() {
    this.connection.ngOnDestroy();
    console.log('GameComponent destroyed');
  }
}
