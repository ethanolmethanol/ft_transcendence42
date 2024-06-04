import { Component } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import { SliderComponent } from '../../components/slider/slider.component';

@Component({
  selector: 'app-create-online-game-page',
  standalone: true,
  imports: [
    HeaderComponent,
    SliderComponent,
  ],
  templateUrl: './create-online-game-page.component.html',
  styleUrl: './create-online-game-page.component.css'
})
export class CreateOnlineGamePageComponent {
}
