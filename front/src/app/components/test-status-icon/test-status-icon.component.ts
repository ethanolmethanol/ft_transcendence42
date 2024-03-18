import {Component, Input} from '@angular/core';
import {CommonModule, NgStyle} from "@angular/common";

@Component({
  selector: 'app-test-status-icon',
  standalone: true,
  imports: [
    NgStyle,
    CommonModule
  ],
  templateUrl: './test-status-icon.component.html',
  styleUrl: './test-status-icon.component.css'
})
export class TestStatusIconComponent {
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
