import {Component, HostListener, ElementRef, OnInit, AfterViewInit} from '@angular/core';
import {PaddleComponent} from "../../components/paddle/paddle.component";
import {Router, RouterLink} from "@angular/router";
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
export class GamePageComponent implements OnInit, AfterViewInit {
  constructor(private elementRef: ElementRef, private router: Router) {}

  @HostListener('window:resize', ['$event'])
  private onResize(event: Event) {
    this.updateGameContainerScale();
  }

  ngOnInit() {
    this.updateGameContainerScale();
  }

  ngAfterViewInit() {
    this.updateGameContainerScale();
  }

  private updateGameContainerScale() {
    const gameContainer = this.elementRef.nativeElement.querySelector('.game-container');
    const scale = Math.min(window.innerWidth / 1000, window.innerHeight / 1000);
    gameContainer.style.transform = `scale(${scale})`;
  }

  confirmGiveUp() {
    if (confirm('Are you sure you want to give up?')) {
      this.router.navigate(['/home']).then(r => {});
    }
  }
}
