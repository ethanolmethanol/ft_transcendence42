import { Component } from '@angular/core';
import {RouterLink} from "@angular/router";
import {BannerComponent} from "./banner/banner.component";
import {LeaderboardComponent} from "./leaderboard/leaderboard.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    RouterLink,
    BannerComponent,
    LeaderboardComponent,
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {

}
