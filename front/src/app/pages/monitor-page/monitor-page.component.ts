import {Component, OnDestroy, OnInit} from '@angular/core';
import {MonitorService} from "../../services/monitor/monitor.service";
import {ActivatedRoute, Router, RouterLink} from "@angular/router";
import {UserService} from "../../services/user/user.service";
import {ErrorMessageComponent} from "../../components/error-message/error-message.component";
import {NgIf} from "@angular/common";
import {LoadingSpinnerComponent} from "../../components/loading-spinner/loading-spinner.component";
import {
  catchError,
  Observable,
  of, repeat, Subject,
  switchMap, takeUntil,
  tap,
  throwError
} from "rxjs";
import {JOIN_GAME_RETRY_DELAY_MS} from "../../constants";

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
export class MonitorPageComponent implements OnInit, OnDestroy {
  private readonly optionsDict: any = {};
  private gameType: string = "local";
  private actionType: string = "join";
  private destroy$ = new Subject<void>();
  public errorMessage: string | null = null;
  public isLoading: boolean = false;

  constructor(private userService: UserService, private router: Router, private route: ActivatedRoute, private monitorService: MonitorService) {
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras.state) {
      const state = navigation.extras.state as {options: any};
      this.optionsDict = {
        "ball_speed": state.options[0],
        "paddle_size": state.options[1],
        "number_players": state.options[2]
      }
      console.log("Selected options: ", state.options);
    } else {
      console.log('No options were passed.');
    }

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

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private getGameUrl(channel_id: string, arena_id: number): string {
    return `/${this.gameType}/${channel_id}/${arena_id}`;
  }

  private getPostData(): string {
    const mode: 0 | 1 = this.gameType === "local" ? 0 : 1;
    const user_id: number = this.userService.getUserID();
    return JSON.stringify({
      "user_id": user_id,
      "players_specs": {"nb_players": 2, "mode": mode, "options": this.optionsDict}
    });
  }

  private joinLocalGame(postData: string): Observable<any> {
    return this.monitorService.joinWebSocketUrl(postData).pipe(
      tap(response => {
        this.navigateToGame(response.channel_id, response.arena.id);
      }),
      catchError((error) => {
        this.handleError(error);
        return throwError(error);
      }),
    );
  }

  private joinRemoteGame(postData: string): Observable<any> {
    this.isLoading = true;
    return of(null).pipe(
      repeat({delay: JOIN_GAME_RETRY_DELAY_MS}),
      switchMap(() =>
        this.monitorService.joinWebSocketUrl(postData).pipe(
          tap(response => {
            this.navigateToGame(response.channel_id, response.arena.id);
          }),
          catchError((error) => {
            if (error.error.error === 'No available channel') {
              console.log('No available channel. Retrying...');
              return of(null); // Signal to retry
            } else {
              this.handleError(error);
              return throwError(error); // Propagate error
            }
          }),
        )
      ),
      takeUntil(this.destroy$)
    );
  }

  private joinGame(postData: string): Observable<any> {
    if (this.gameType === "local") {
      return this.joinLocalGame(postData);
    } else {
      return this.joinRemoteGame(postData);
    }
  }

  private createGame(postData: string): void {
    this.monitorService.createWebSocketUrl(postData).subscribe(response => {
      this.navigateToGame(response.channel_id, response.arena.id);
    }, error => this.handleError(error));
  }

  private async requestRemoteWebSocketUrl(postData: string): Promise<void> {
    if (this.actionType == "join") {
      this.joinGame(postData).subscribe();
    } else if (this.actionType == "create") {
      this.createGame(postData);
    }
  }

  private requestLocalWebSocketUrl(postData: string): void {
    this.createGame(postData);
  }

  private handleError(error: any): void {
    this.errorMessage = error.error.error;
    console.log('Error joining game: ' + this.errorMessage);
  }

  private navigateToGame(channelID: string, arenaID : number): void {
    const gameUrl: string = this.getGameUrl(channelID, arenaID);
    this.router.navigateByUrl(gameUrl);
  }
}
