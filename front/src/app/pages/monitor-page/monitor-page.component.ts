import {Component, OnInit} from '@angular/core';
import {MonitorService} from "../../services/monitor/monitor.service";
import {ActivatedRoute, Router, RouterLink} from "@angular/router";
import {UserService} from "../../services/user/user.service";
import {ErrorMessageComponent} from "../../components/error-message/error-message.component";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-monitor-page',
  standalone: true,
  imports: [
    ErrorMessageComponent,
    NgIf,
    RouterLink
  ],
  templateUrl: './monitor-page.component.html',
  styleUrl: './monitor-page.component.css'
})
export class MonitorPageComponent implements OnInit {
  private gameType: string = "local";
  public errorMessage: string | null = null;

  constructor(private userService: UserService, private router: Router, private route: ActivatedRoute, private monitorService: MonitorService) {}

  private getGameUrl(channel_id: string, arena_id: string): string {
    return `/${this.gameType}/${channel_id}/${arena_id}`;
  }

  private getPostData(): string {
    const mode: 0 | 1 = this.gameType === "local" ? 0 : 1;
    const user_id: number = this.userService.getUserID();
    return JSON.stringify({
      "user_id": user_id,
      "players_specs": {"nb_players": 2, "mode": mode}
    });
  }

  private handleResponse(response: {isInChannel: boolean}, postData: string): void {
    if (response.isInChannel) {
      this.monitorService.joinWebSocketUrl(postData).subscribe(response => {
        this.navigateToGame(response.channel_id, response.arena.id);
      }, error => this.handleError(error));
    } else {
      this.monitorService.createWebSocketUrl(postData).subscribe(response => {
        this.navigateToGame(response.channel_id, response.arena.id);
      }, error => this.handleError(error));
    }
  }

  private handleError(error: any): void {
    this.errorMessage = error.error.error;
  }

  async ngOnInit() : Promise<void> {
    this.gameType = this.route.snapshot.data['gameType'];
    await this.userService.whenUserDataLoaded();
    const postData = this.getPostData();
    this.monitorService.isUserInGame(postData).subscribe(
      response => this.handleResponse(response, postData),
      error => this.handleError(error)
    )
  }

  private navigateToGame(channelID: string, arenaID : number): void {
    const gameUrl = this.getGameUrl(channelID, arenaID.toString());
    this.router.navigateByUrl(gameUrl);
  }
}
