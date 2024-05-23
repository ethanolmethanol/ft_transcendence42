import { Component, Input } from '@angular/core';
import { LOADING_BUTTON_TIME } from '../../constants';

@Component({
  selector: 'app-loading-button',
  standalone: true,
  imports: [],
  templateUrl: './loading-button.component.html',
  styleUrls: ['./loading-button.component.css'] // Note: Use styleUrls instead of styleUrl for Angular 12+
})
export class LoadingButtonComponent {
  @Input() callback: () => void = () => {};
  @Input() title: string = "Click me!";
  charging = false;
  chargeStart = 0;
  chargeTimeout: any;
  chargeTimeRemaining = LOADING_BUTTON_TIME; // 5000 ms = 5 s

  startCharging(): void {
    if (!this.charging) {
      this.chargeStart = Date.now(); // Reset chargeStart on restart
    }
    this.charging = true;

    const elapsedTime = Date.now() - this.chargeStart;
    this.chargeTimeRemaining -= elapsedTime > 0? elapsedTime : 0; // Ensure we don't go below 0

    if (this.chargeTimeRemaining <= 0) {
      this.chargeTimeRemaining = 0; // Prevent negative values
      this.callback();
    } else {
      this.chargeTimeout = setTimeout(() => {
        this.startCharging(); // Recursively call startCharging until fully charged
      }, Math.max(0, this.chargeTimeRemaining));
    }
  }

  stopCharging() {
    this.charging = false;
    clearTimeout(this.chargeTimeout);
    this.chargeStart = 0; // Reset chargeStart when stopping
  }
}
