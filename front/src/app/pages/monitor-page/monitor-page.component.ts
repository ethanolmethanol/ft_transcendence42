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
  constructor(private userService: UserService, private router: Router, private route: ActivatedRoute, private monitorService: MonitorService) {
/*     const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras.state) {
      const state = navigation.extras.state as {options: any};
      console.log("Selected options: ", state.options);
    } else {
      console.log('No options were passed.');
    } */
  }

  private getGameUrl(channel_id: string, arena_id: string): string {
    return `/${this.gameType}/${channel_id}/${arena_id}`;
  }

  async ngOnInit() : Promise<void> {
    this.gameType = this.route.snapshot.data['gameType'];
    await this.userService.whenUserDataLoaded();
    const mode: 0 | 1 = this.gameType === "local" ? 0 : 1;
    const user_id: number = this.userService.getUserID();
    const postData: string = JSON.stringify({
      "user_id": user_id,
      "players_specs": {"nb_players": 2, "mode": mode}
    });
    this.monitorService.isUserInGame(postData).subscribe(response => {
        console.log(response);
        if (response.isInChannel) {
          this.monitorService.joinWebSocketUrl(postData).subscribe(response => {
            this.navigateToGame(response.channel_id, response.arena.id);
          })
        } else {
          this.monitorService.createWebSocketUrl(postData).subscribe(response => {
            this.navigateToGame(response.channel_id, response.arena.id);
          });
        }
    })
  }

  private navigateToGame(channelID: string, arenaID : number): void {
      const gameUrl = this.getGameUrl(channelID, arenaID.toString());
      this.router.navigateByUrl(gameUrl);
  }
}
