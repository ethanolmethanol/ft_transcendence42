import { Component } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-online-game-selector-page',
  standalone: true,
  imports: [
    HeaderComponent,
    RouterLink,
  ],
  templateUrl: './online-game-selector-page.component.html',
  styleUrl: './online-game-selector-page.component.css'
})

export class OnlineGameSelectorPageComponent {

}
