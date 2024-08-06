import { Component } from '@angular/core';
import {WebSocketService} from "../../../services/web-socket/web-socket.service";
import {Router} from "@angular/router";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-start-timer',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './start-timer.component.html',
  styleUrl: './start-timer.component.css'
})
export class StartTimerComponent {
  time: number | null = null;
  message: string = "";
  show: boolean = false;

  constructor (private router: Router) {}
}
