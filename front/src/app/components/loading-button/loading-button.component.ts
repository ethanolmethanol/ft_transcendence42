import {Component, Input} from '@angular/core';
import {LOADING_BUTTON_TIME} from "../../constants";

@Component({
  selector: 'app-loading-button',
  standalone: true,
  imports: [],
  templateUrl: './loading-button.component.html',
  styleUrl: './loading-button.component.css'
})
export class LoadingButtonComponent {

  @Input() callback: () => void = () => {};
  @Input() title: string = "Click me!";
  charging = false;
  chargeStart = 0;
  chargeTimeout: any;
  chargeTimeRemaining = LOADING_BUTTON_TIME; // 5000 ms = 5 s

  startCharging(callback: () => void): void {
    console.log("Start charging!")
    if (this.charging == false) {
      this.chargeTimeRemaining -= Date.now() - this.chargeStart
    }
    this.charging = true;
    this.chargeStart = Date.now();
    this.chargeTimeout = setTimeout(() => {
      callback();
      this.chargeTimeRemaining = LOADING_BUTTON_TIME; // Reset the remaining time if the button is fully charged
    }, this.chargeTimeRemaining);
  }

  stopCharging() {
    console.log("Stop charging!")
    this.charging = false;
    clearTimeout(this.chargeTimeout);
  }
}
