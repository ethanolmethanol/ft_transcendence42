import {Component, Input} from '@angular/core';
import {CommonModule, NgStyle} from "@angular/common";

@Component({
  selector: 'app-status-icon',
  standalone: true,
  imports: [
    NgStyle,
    CommonModule
  ],
  templateUrl: './status-icon.component.html',
  styleUrl: './status-icon.component.css'
})
export class StatusIconComponent {
  @Input() testPassed: boolean = false;
  @Input() errorMessage: string = '';
  showError: boolean = false;

  onMouseOver() {
    this.showError = true;
  }

  onMouseOut() {
    this.showError = false;
  }
}
