import { Component } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import {Router, RouterLink} from '@angular/router';
import { FormsModule } from "@angular/forms";
import { ButtonWithIconComponent } from "../../components/button-with-icon/button-with-icon.component";
import { CopyButtonComponent } from "../../components/copy-button/copy-button.component";
import {CHANNEL_ID_LENGTH} from "../../constants";

@Component({
  selector: 'app-online-game-selector-page',
  standalone: true,
  imports: [
    HeaderComponent,
    RouterLink,
    FormsModule,
    ButtonWithIconComponent,
    CopyButtonComponent,
  ],
  templateUrl: './online-game-selector-page.component.html',
  styleUrl: './online-game-selector-page.component.css'
})

export class OnlineGameSelectorPageComponent {
  gameID: string | null = null;

  constructor(private router: Router) {}

  public joinGame() {
    console.log("Joining game with ID: " + this.gameID);
    const url = `/online/classic/${this.gameID}`;
    console.log("Navigating to: " + url);
    this.router.navigate([url]);
  }

  public preventSpaces(event: KeyboardEvent | InputEvent): void {
    if (event instanceof KeyboardEvent && (event.key === ' ' || event.key === 'Enter')) {
      event.preventDefault();
    } else if (event instanceof InputEvent) {
      this.gameID = this.gameID?.replace(/\s/g, '')!;
    }
  }

    protected readonly CHANNEL_ID_LENGTH = CHANNEL_ID_LENGTH;
}
