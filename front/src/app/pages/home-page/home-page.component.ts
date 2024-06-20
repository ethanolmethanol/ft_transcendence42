import { Component, OnInit } from '@angular/core';
import { RouterLink } from "@angular/router";
import { HeaderComponent } from "../../components/header/header.component";
import { LeaderboardComponent } from "../../components/leaderboard/leaderboard.component";
import { UserService } from '../../services/user/user.service';
import { LoadingSpinnerComponent } from "../../components/loading-spinner/loading-spinner.component";
import {NgStyle} from "@angular/common";
import {ButtonWithIconComponent} from "../../components/button-with-icon/button-with-icon.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    RouterLink,
    HeaderComponent,
    LeaderboardComponent,
    LoadingSpinnerComponent,
    NgStyle,
    ButtonWithIconComponent,
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

}
