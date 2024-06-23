import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import {NgOptimizedImage} from "@angular/common";
import {HeaderComponent} from "../../components/header/header.component";

@Component({
  selector: 'app-not-found-page',
  standalone: true,
  imports: [
    RouterLink,
    NgOptimizedImage,
    HeaderComponent
  ],
  templateUrl: './not-found-page.component.html',
  styleUrl: './not-found-page.component.css'
})
export class NotFoundPageComponent {

}
