import { Component } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import { GameboardComponent } from "../../components/gameboard/gameboard.component";
import { AppearanceSettingsComponent } from '../../components/appearance-settings/appearance-settings.component';
import * as Constants from '../../constants';

@Component({
  selector: 'app-profile-page',
  standalone: true,
  imports: [
    HeaderComponent,
    GameboardComponent,
    AppearanceSettingsComponent,
  ],
  templateUrl: './profile-page.component.html',
  styleUrl: './profile-page.component.css'
})
export class ProfilePageComponent {
  gameboardColors: string[] = Constants.DEFAULT_COLORS;

  applyColors(colors: string[]) {
    this.gameboardColors = colors;
  }
}
