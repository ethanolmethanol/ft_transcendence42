import { Component, ElementRef, Renderer2, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-leaderboard',
  standalone: true,
  imports: [],
  templateUrl: './leaderboard.component.html',
  styleUrl: './leaderboard.component.css'
})
export class LeaderboardComponent implements AfterViewInit {
  constructor(private el: ElementRef, private renderer: Renderer2) {}

  ngAfterViewInit() {
     const leaderboard = this.el.nativeElement.querySelector('.leaderboard');
     const leaderboardContainer = this.el.nativeElement.querySelector('.leaderboard-container');
     const leaderboardHeight = leaderboard.offsetHeight;

     this.renderer.setStyle(leaderboardContainer, 'padding-top', `${leaderboardHeight}px`);
  }
 }
