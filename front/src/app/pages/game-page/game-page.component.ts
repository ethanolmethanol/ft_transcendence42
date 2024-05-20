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
import {PaddleComponent} from "../../components/paddle/paddle.component";
import {ActivatedRoute, Router, RouterLink} from "@angular/router";
import {GameComponent} from "../../components/game/game.component";
import { WebSocketService } from '../../services/web-socket/web-socket.service';
import {LoadingSpinnerComponent} from "../../components/loading-spinner/loading-spinner.component";
import {ConnectionService} from "../../services/connection/connection.service";
import {LOADING_BUTTON_TIME} from "../../constants";

@Component({
  selector: 'app-game-page',
  standalone: true,
  imports: [
    PaddleComponent,
    RouterLink,
    GameComponent,
    LoadingSpinnerComponent
  ],
  templateUrl: './game-page.component.html',
  styleUrl: './game-page.component.css'
})

export class GamePageComponent implements OnInit, AfterViewInit, OnDestroy {

  charging = true;
  chargeStart = 0;
  chargeTimeout: any;
  chargeTimeRemaining = LOADING_BUTTON_TIME; // 5000 ms = 5 s

  @ViewChildren(GameComponent) game!: QueryList<GameComponent>;
  @HostListener('window:resize', ['$event'])
  public onResize(event: Event) {
    this.updateGameContainerScale();
  }

  constructor(
    private elementRef: ElementRef,
    private router: Router,
    private webSocketService: WebSocketService,
    private route: ActivatedRoute,  // Inject ActivatedRoute
    private connectionService: ConnectionService  // Inject connectionServiceComponent
  ) {}

  ngOnInit() {
    this.updateGameContainerScale();
  }

  ngAfterViewInit() {
    // Now you can safely access this.game.first
    this.route.params.subscribe(params => {
      const channel_id = params['channel_id'];
      const arena_id = params['arena_id'];
      console.log('Channel ID:', channel_id);
      this.connectionService.establishConnection(this.game.first.setArena.bind(this), channel_id, arena_id);
    });
  }

  ngOnDestroy() {
    this.connectionService.endConnection();
  }

  private updateGameContainerScale() {
    const gameContainer = this.elementRef.nativeElement.querySelector('.game-container');
    const scale = Math.min(window.innerWidth / 1000, window.innerHeight / 1000);
    gameContainer.style.transform = `scale(${scale})`;
  }

  confirmGiveUp() {
    this.router.navigate(['/home']);
    this.webSocketService.giveUp();
  }

  startCharging() {
    console.log("Start charging!")
    if (this.charging == false) {
      this.chargeTimeRemaining -= Date.now() - this.chargeStart
    }
    this.charging = true;
    this.chargeStart = Date.now();
    this.chargeTimeout = setTimeout(() => {
      this.confirmGiveUp();
      this.chargeTimeRemaining = LOADING_BUTTON_TIME; // Reset the remaining time if the button is fully charged
    }, this.chargeTimeRemaining);
  }

  stopCharging() {
    console.log("Stop charging!")
    this.charging = false;
    clearTimeout(this.chargeTimeout);
  }
}
