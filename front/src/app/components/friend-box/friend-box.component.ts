import { Component, Input } from '@angular/core';
import { ONLINE } from "../../constants";
import { FriendCardComponent } from "../friend-card/friend-card.component";
import { NgIf, NgFor, CommonModule } from "@angular/common"

@Component({
  selector: 'app-friend-box',
  standalone: true,
  imports: [
    FriendCardComponent,
    NgFor,
    NgIf,
    CommonModule,
  ],
  templateUrl: './friend-box.component.html',
  styleUrl: './friend-box.component.css'
})
export class FriendBoxComponent {
  @Input() friendStatus: number = ONLINE;
  @Input() friendList: string[] = [];
  @Input() sectionName: string = "";

}
