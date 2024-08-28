import { Component } from '@angular/core';
import {HeaderComponent} from "../../components/header/header.component";

@Component({
  selector: 'app-rules-page',
  standalone: true,
  imports: [
    HeaderComponent
  ],
  templateUrl: './rules-page.component.html',
  styleUrl: './rules-page.component.css'
})
export class RulesPageComponent {

}
