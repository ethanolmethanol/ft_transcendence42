import { Component } from '@angular/core';
import {PaddleComponent} from "../../components/paddle/paddle.component";
import {RouterLink} from "@angular/router";

@Component({
  selector: 'app-game-page',
  standalone: true,
  imports: [
    PaddleComponent,
    RouterLink
  ],
  templateUrl: './game-page.component.html',
  styleUrl: './game-page.component.css'
})
export class GamePageComponent {
}
