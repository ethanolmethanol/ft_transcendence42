import {Component, OnInit} from '@angular/core';
import {MonitorService} from "../../services/monitor/monitor.service";
import {ActivatedRoute, Router, RouterLink} from "@angular/router";
import {UserService} from "../../services/user/user.service";
import {ErrorMessageComponent} from "../../components/error-message/error-message.component";
import {NgIf} from "@angular/common";
import {LoadingSpinnerComponent} from "../../components/loading-spinner/loading-spinner.component";

@Component({
  selector: 'app-monitor-page',
  standalone: true,
  imports: [
    ErrorMessageComponent,
    NgIf,
    RouterLink,
    LoadingSpinnerComponent
  ],
  templateUrl: './monitor-page.component.html',
  styleUrl: './monitor-page.component.css'
})
export class MonitorPageComponent implements OnInit {
  private gameType: string = "local";
  private actionType: string = "join";
  public errorMessage: string | null = null;
  public isLoading: boolean = false;
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

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private async joinGame(postData: string): Promise<void> {
    this.isLoading = true;
    let errorOccurred: boolean = true;

    while (errorOccurred) {
      errorOccurred = false;

      const response = await this.monitorService.joinWebSocketUrl(postData).toPromise().catch(async (error) => {
        if (error.error.error === "No available channel") {
          errorOccurred = true;
          console.log("No available channel. Retrying in 5 seconds...");
          await this.delay(5000);
        } else {
          this.handleError(error);
        }
      });

      if (!errorOccurred && response) {
        this.navigateToGame(response.channel_id, response.arena.id);
      }
    }
    this.isLoading = false;
  }

  private createGame(postData: string): void {
    this.monitorService.createWebSocketUrl(postData).subscribe(response => {
      this.navigateToGame(response.channel_id, response.arena.id);
    }, error => this.handleError(error));
  }

  private async requestRemoteWebSocketUrl(postData: string): Promise<void> {
    if (this.actionType == "join") {
      await this.joinGame(postData);
    } else if (this.actionType == "create") {
      this.createGame(postData);
    }
  }

  private requestLocalWebSocketUrl(postData: string): void {
    this.monitorService.isUserInGame(postData).subscribe(response => {
      if (response.isInChannel) {
        this.joinGame(postData);
      } else {
        this.createGame(postData);
      }
    });
  }

  private handleError(error: any): void {
    this.errorMessage = error.error.error;
  }

  async ngOnInit() : Promise<void> {
    this.gameType = this.route.snapshot.data['gameType'];
    this.actionType = this.route.snapshot.data['actionType'];
    await this.userService.whenUserDataLoaded();
    const postData: string = this.getPostData();
    if (this.gameType === "local") {
      this.requestLocalWebSocketUrl(postData);
    } else {
      await this.requestRemoteWebSocketUrl(postData)
    }
  }

  private navigateToGame(channelID: string, arenaID : number): void {
    const gameUrl: string = this.getGameUrl(channelID, arenaID.toString());
    this.router.navigateByUrl(gameUrl);
  }
}
