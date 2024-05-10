import { Component, OnInit } from '@angular/core';
import {RouterLink} from "@angular/router";
import {BannerComponent} from "../../components/banner/banner.component";
import {LeaderboardComponent} from "../../components/leaderboard/leaderboard.component";
import { UserService } from '../../services/user/user.service';
import {LoadingSpinnerComponent} from "../../components/loading-spinner/loading-spinner.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    RouterLink,
    BannerComponent,
    LeaderboardComponent,
    LoadingSpinnerComponent,
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent implements OnInit {
  welcome: string = '';

  constructor(private userService: UserService) { }

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.welcome = `Welcome, ${this.userService.getUsername()}`;
 }

 public getLocalGameUrl(): string {
    return '/local-game';
 }
}
