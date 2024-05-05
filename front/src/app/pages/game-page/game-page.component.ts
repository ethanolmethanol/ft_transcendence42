import {Component, HostListener, ElementRef, OnInit, AfterViewInit, ViewChildren, QueryList} from '@angular/core';
import {PaddleComponent} from "../../components/paddle/paddle.component";
import {ActivatedRoute, Router, RouterLink} from "@angular/router";
import {GameComponent} from "../../components/game/game.component";
import { WebSocketService } from '../../services/web-socket/web-socket.service';
import {ConnectionComponent} from "../../components/game/connection.component";

@Component({
  selector: 'app-game-page',
  standalone: true,
  imports: [
    PaddleComponent,
    RouterLink,
    GameComponent
  ],
  templateUrl: './game-page.component.html',
  styleUrl: './game-page.component.css'
})
export class GamePageComponent implements OnInit, AfterViewInit {

  @ViewChildren(GameComponent) game!: QueryList<GameComponent>;
  @HostListener('window:resize', ['$event'])
  private onResize(event: Event) {
    this.updateGameContainerScale();
  }

  constructor(
    private elementRef: ElementRef,
    private router: Router,
    private webSocketService: WebSocketService,
    private route: ActivatedRoute,  // Inject ActivatedRoute
    private connection: ConnectionComponent  // Inject ConnectionComponent
  ) {}

  ngOnInit() {
    this.updateGameContainerScale();
  }

  ngAfterViewInit() {
    this.updateGameContainerScale();
    this.route.params.subscribe(params => {
      const channelID = params['channelID'];
      const arenaID = params['arenaID'];
      console.log('Channel ID:', channelID);
      this.connection.establishConnection(this.game.first.setArena.bind(this), channelID, arenaID);
    });
  }

  private updateGameContainerScale() {
    const gameContainer = this.elementRef.nativeElement.querySelector('.game-container');
    const scale = Math.min(window.innerWidth / 1000, window.innerHeight / 1000);
    gameContainer.style.transform = `scale(${scale})`;
  }

  confirmGiveUp() {
    if (confirm('Are you sure you want to give up?')) {
      this.router.navigate(['/home']);
      this.webSocketService.giveUp();
    }
  }
}
