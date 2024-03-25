import {Component, HostListener, OnInit, QueryList, ViewChildren, AfterViewInit} from '@angular/core';
import {PaddleComponent} from "../../components/paddle/paddle.component";
import {RouterLink} from "@angular/router";
import {GAME_HEIGHT, GAME_WIDTH, LINE_THICKNESS} from "../../constants";
import {GameComponent} from "./game/game.component";

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
export class GamePageComponent {

}
