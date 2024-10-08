import { Component, OnInit } from '@angular/core';
import { RouterLink } from "@angular/router";
import { HeaderComponent } from '../../components/header/header.component';
import { GameboardComponent } from "../../components/gameboard/gameboard.component";
import { AppearanceSettingsComponent } from '../../components/appearance-settings/appearance-settings.component';
import * as Constants from '../../constants';
import { UserService } from '../../services/user/user.service';

@Component({
  selector: 'app-custom-page',
  standalone: true,
  imports: [
    RouterLink,
    HeaderComponent,
    GameboardComponent,
    AppearanceSettingsComponent,
  ],
  templateUrl: './custom-page.component.html',
  styleUrl: './custom-page.component.css'
})
export class CustomPageComponent implements OnInit{
  colors: string[] = Constants.DEFAULT_COLORS;

  constructor(private userService: UserService) {}

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
  }

  get gameboardColors(): string[] {
    const backend_colors = this.gameboardColorsFromBackend;
    if (backend_colors) {
      this.colors = backend_colors;
    }
    return this.colors;
  }

  get gameboardColorsFromBackend(): string[] {
    if (!this.userService) {
      return [];
    }
    return this.userService.getColorConfig();
  }

  public applyColors(colors: string[]) {
    this.colors = colors;
    this.userService.setColorConfig(colors);
  }
}
