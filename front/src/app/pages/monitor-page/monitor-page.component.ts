import {Component, OnDestroy} from '@angular/core';
import {Subscription} from "rxjs";
import {MonitorService} from "../../services/monitor/monitor.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-monitor-page',
  standalone: true,
  imports: [],
  templateUrl: './monitor-page.component.html',
  styleUrl: './monitor-page.component.css'
})
export class MonitorPageComponent implements OnDestroy {
  private postData = JSON.stringify({
    "username": "Player_name",
    "playerSpecs": {"nbPlayers": 2, "mode": 0}
  })
  webSocketSubscription?: Subscription;

  constructor(private router: Router, private monitorService: MonitorService) {
    this.webSocketSubscription = monitorService.getWebSocketUrl(this.postData).subscribe(response => {
      const gameUrl = this.getGameUrl(response.channelID, response.arena.id);
      this.router.navigateByUrl(gameUrl);
  })}

  private getGameUrl(channelID: string, arenaID: string): string {
    return `/local-game/${channelID}/${arenaID}`;
  }

  ngOnDestroy() {
    this.webSocketSubscription?.unsubscribe();
  }
}
