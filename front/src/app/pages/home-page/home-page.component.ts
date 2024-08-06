import {AfterViewInit, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import { Router, RouterLink } from "@angular/router";
import { HeaderComponent } from "../../components/header/header.component";
import { UserService } from '../../services/user/user.service';
import { LoadingSpinnerComponent } from "../../components/loading-spinner/loading-spinner.component";
import {AsyncPipe, NgForOf, NgIf, NgStyle} from "@angular/common";
import {ButtonWithIconComponent} from "../../components/button-with-icon/button-with-icon.component";
import {GameSummaryComponent} from "../../components/stats/game-summary/game-summary.component";
import {GameSummaryListComponent} from "../../components/stats/game-summary-list/game-summary-list.component";
import {DashboardComponent} from "../../components/stats/dashboard/dashboard.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    RouterLink,
    HeaderComponent,
    LoadingSpinnerComponent,
    NgStyle,
    ButtonWithIconComponent,
    NgForOf,
    GameSummaryComponent,
    AsyncPipe,
    NgIf,
    GameSummaryListComponent,
    DashboardComponent,
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent implements AfterViewInit {
  welcome: string = '';
  userID: number | undefined;
  @ViewChild('gameSummaryList') gameSummaryListComponent!: GameSummaryListComponent;
  @ViewChild('homePageContainer') homePageContainer!: ElementRef;

  constructor(private userService: UserService, private router: Router) { }

  async ngAfterViewInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.welcome = `Welcome, ${this.userService.getUsername()}`;
    this.userID = this.userService.getUserID();
  }

  scrollToTop(): void {
    this.homePageContainer.nativeElement.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  }
}
