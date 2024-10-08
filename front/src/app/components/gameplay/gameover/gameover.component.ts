import { Component, Input } from '@angular/core';
import {NgIf} from "@angular/common";
import { WebSocketService } from '../../../services/web-socket/web-socket.service';
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
  time: number | null = null;
  message: string = "";
  show: boolean = false;

  constructor (private webSocketService: WebSocketService, private router: Router) {}

  public backToHomePage() {
    this.webSocketService.giveUp();
    this.redirectToHome();
  }

  private redirectToHome() {
    this.router.navigate(['/home']);
  }
}
