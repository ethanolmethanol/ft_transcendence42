import { Component, Input } from '@angular/core';
import {NgIf} from "@angular/common";
import { WebSocketService } from '../../services/web-socket/web-socket.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-gameover',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './gameover.component.html',
  styleUrl: './gameover.component.css'
})
export class GameOverComponent {
  @Input() show: boolean = false;
  @Input() message: string = "";

  constructor (private webSocketService: WebSocketService, private router: Router) {

  }

  backToHomePage() {
    this.webSocketService.giveUp();
    this.router.navigate(['/home']);
  }

  reMatch() {
    this.webSocketService.rematch();
    this.show = false;
  }
}
