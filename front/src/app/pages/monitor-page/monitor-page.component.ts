import {Component, OnDestroy, OnInit} from '@angular/core';
import {Subscription} from "rxjs";
import {MonitorService} from "../../services/monitor/monitor.service";
import {Router} from "@angular/router";
import {UserService} from "../../services/user/user.service";

@Component({
  selector: 'app-monitor-page',
  standalone: true,
  imports: [],
  templateUrl: './monitor-page.component.html',
  styleUrl: './monitor-page.component.css'
})
export class MonitorPageComponent implements OnInit, OnDestroy {
  webSocketSubscription?: Subscription;

  constructor(private userService: UserService, private router: Router, private monitorService: MonitorService) {}

  private getGameUrl(channelID: string, arenaID: string): string {
    return `/local-game/${channelID}/${arenaID}`;
  }

  async ngOnInit() : Promise<void> {
    await this.userService.whenUserDataLoaded();
    const postData = JSON.stringify({
      "username": this.userService.getUsername(),
      "playerSpecs": {"nbPlayers": 2, "mode": 0}
    });
    this.webSocketSubscription = this.monitorService.getWebSocketUrl(postData).subscribe(response => {
      const gameUrl = this.getGameUrl(response.channelID, response.arena.id);
      this.router.navigateByUrl(gameUrl);
    })}

  ngOnDestroy() {
    this.webSocketSubscription?.unsubscribe();
  }
}
