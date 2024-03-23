import { Component } from '@angular/core';
import {PaddleComponent} from "../../components/paddle/paddle.component";

@Component({
  selector: 'app-game-page',
  standalone: true,
  imports: [
    PaddleComponent
  ],
  templateUrl: './game-page.component.html',
  styleUrl: './game-page.component.css'
})
export class GamePageComponent {

}
