import {Component, OnInit} from '@angular/core';
import {MonitorService} from "../../services/monitor/monitor.service";
import {ActivatedRoute, Router} from "@angular/router";
import {UserService} from "../../services/user/user.service";

@Component({
  selector: 'app-monitor-page',
  standalone: true,
  imports: [],
  templateUrl: './monitor-page.component.html',
  styleUrl: './monitor-page.component.css'
})
export class MonitorPageComponent implements OnInit {
  private gameType: string = "local";
  constructor(private userService: UserService, private router: Router, private route: ActivatedRoute, private monitorService: MonitorService) {}

  private getGameUrl(channel_id: string, arena_id: string): string {
    return `/${this.gameType}/${channel_id}/${arena_id}`;
  }

  async ngOnInit() : Promise<void> {
    this.gameType = this.route.snapshot.data['gameType'];
    await this.userService.whenUserDataLoaded();
    const mode: 0 | 1 = this.gameType === "local" ? 0 : 1;
    const postData = JSON.stringify({
      "user_id": this.userService.getUserID(),
      "players_specs": {"nb_players": 2, "mode": mode}
    });
    this.monitorService.getWebSocketUrl(postData).subscribe(response => {
      const gameUrl = this.getGameUrl(response.channel_id, response.arena.id);
      this.router.navigateByUrl(gameUrl);
    })}
}
