import {AfterViewInit, Component, HostListener, QueryList, ViewChildren, OnDestroy} from '@angular/core';
import {GAME_HEIGHT, GAME_WIDTH, LINE_THICKNESS, PADDLE_HEIGHT, PADDLE_WIDTH} from "../../constants";
import {PaddleComponent} from "../paddle/paddle.component";
import {BallComponent} from "../ball/ball.component";
import {WebSocketService} from "../../services/web-socket/web-socket.service";
import { ArenaResponse, MonitorService, WebSocketUrlResponse} from "../../services/monitor/monitor.service";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [
    PaddleComponent,
    BallComponent
  ],
  templateUrl: './game.component.html',
  styleUrl: './game.component.css'
})
export class GameComponent implements AfterViewInit, OnDestroy {
  readonly gameWidth = GAME_WIDTH;
  readonly gameHeight = GAME_HEIGHT;
  readonly lineThickness = LINE_THICKNESS;
  @ViewChildren(BallComponent) ball!: QueryList<BallComponent>;
  @ViewChildren(PaddleComponent) paddles!: QueryList<PaddleComponent>;
  // players!: string[];
  player1Score = 0;
  player2Score = 0;
  private postData = JSON.stringify({
    "username": "placeholder",
    "playerSpecs": {"nbPlayers": 2, "mode": 0}
  })
  private paddleBinding = [
    { id: 1, upKey: 'w', downKey: 's' },
    { id: 2, upKey: 'ArrowUp', downKey: 'ArrowDown' },
  ];
  private pressedKeys = new Set<string>();
  private connectionOpenedSubscription?: Subscription;
  private WebSocketSubscription?: Subscription;
  private WebSocketMessagesSubscription?: Subscription;

  constructor(private monitorService: MonitorService, private webSocketService: WebSocketService) {
    this.establishConnection();
  }

  public ngOnDestroy() {
    this.endConnection();
    this.connectionOpenedSubscription?.unsubscribe();
    this.WebSocketSubscription?.unsubscribe();
    this.WebSocketMessagesSubscription?.unsubscribe();
  }

  private establishConnection() {
    this.WebSocketSubscription = this.monitorService.getWebSocketUrl(this.postData).subscribe(response => {
      console.log(response);
      this.webSocketService.connect(response.channelID);
      this.handleWebSocketConnection(response.arena);
    });
  }

  private handleWebSocketConnection(arena: ArenaResponse) {
    this.connectionOpenedSubscription = this.webSocketService.getConnectionOpenedEvent().subscribe(() => {
      console.log('WebSocket connection opened');
      this.webSocketService.join(arena.id);
      this.setArena(arena);
    });
  }

  private listenToWebSocketMessages() {
    this.WebSocketMessagesSubscription = this.webSocketService.getMessages().subscribe(message => {
      console.log('Received WebSocket message:', message);
      // Perform actions based on the received message
      // For example, if the message is a JSON string representing a game state, you can parse it and update your game state
      // const data = JSON.parse(message);
      // if (data.type === 'game_state') {
      //   this.updateGameState(data.message);
      // }
    });
  }

  public endConnection() {
    console.log('WebSocket connection closed');
    this.webSocketService.disconnect();
  }

  private setArena(arena: ArenaResponse) {
    this.paddles.forEach(paddle => {
      const paddleData = arena.paddles.find(p => p.slot === paddle.id);
      if (paddleData) {
        paddle.positionX = paddleData.position.x;
        paddle.positionY = paddleData.position.y;
        paddle.width = paddleData.width;
        paddle.height = paddleData.height;
      }
    });
    this.ball.first.positionX = arena.ball.position.x;
    this.ball.first.positionY = arena.ball.position.y;
    this.ball.first.ballSize = 2 * arena.ball.radius;
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
    const initialPosition = paddle.positionY;

    if (isMovingUp) {
      paddle.moveUp();
    } else if (isMovingDown) {
      paddle.moveDown();
    }
    if (initialPosition !== paddle.positionY) {
      const playerName = paddle.id === 1 ? "Player1" : "Player2";
      this.webSocketService.sendPaddleMovement(playerName, 0.3);
      console.log(`Paddle ${paddle.id} position updated:`, paddle.positionX, paddle.positionY);
    }
  }

  ngAfterViewInit() {
    this.listenToWebSocketMessages();
    this.gameLoop();
  }
}
