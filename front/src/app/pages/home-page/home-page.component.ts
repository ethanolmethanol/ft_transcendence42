import { Component } from '@angular/core';
import {RouterLink} from "@angular/router";
import {BannerComponent} from "./banner/banner.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    BannerComponent,
    RouterLink
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent {

}
