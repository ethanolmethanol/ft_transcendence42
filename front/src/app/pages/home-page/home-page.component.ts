import { Component, OnInit } from '@angular/core';
import {RouterLink} from "@angular/router";
import {BannerComponent} from "../../components/banner/banner.component";
import {LeaderboardComponent} from "../../components/leaderboard/leaderboard.component";
import { UserService } from '../../services/user/user.service';

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
export class HomePageComponent implements OnInit {
  welcome: string = '';

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.userService.getUsername().subscribe(data => {
      this.welcome = `Welcome, ${data.username}!`;
    });
 }

 public getLocalGameUrl(): string {
    return '/local-game';
 }
}
