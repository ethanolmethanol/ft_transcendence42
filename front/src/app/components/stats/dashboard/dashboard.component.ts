import {Component, OnInit} from '@angular/core';
import {UserService} from "../../../services/user/user.service";
import {DatePipe, NgIf} from "@angular/common";
import {formatTimePlayed} from "../../../utils/time";
import {TimePlayedComponent} from "../time-played/time-played.component";
import {LoadingSpinnerComponent} from "../../loading-spinner/loading-spinner.component";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    TimePlayedComponent,
    LoadingSpinnerComponent,
    NgIf
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent implements OnInit {

  isWaiting = true;
  timePlayed: string = '';

  constructor(private userService: UserService) {
    console.log('DashboardComponent created');
  }

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    setTimeout(() => {
      this.initTimePlayed();
      this.isWaiting = false;
    }, 1000);
  }


  initTimePlayed(): void {
    const timePlayedInSeconds = this.userService.getTimePlayed();
    this.timePlayed = formatTimePlayed(timePlayedInSeconds)
  }
}
