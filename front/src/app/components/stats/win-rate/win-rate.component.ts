import {Component, Input, OnInit} from '@angular/core';
import {ChartModule} from "primeng/chart";
import {Wins} from "../../../interfaces/user";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-win-rate',
  standalone: true,
  imports: [
    ChartModule,
    NgIf
  ],
  templateUrl: './win-rate.component.html',
  styleUrl: './win-rate.component.css'
})
export class WinRateComponent implements OnInit {
  @Input() winDict!: Wins;
  winRate: number = 0;
  data: any;
  options: any;

  ngOnInit() {
    this.setChart();
    this.winRate = this.calculateWinRate();
  }

  private calculateWinRate(): number {
    const total = this.winDict.win + this.winDict.loss + this.winDict.tie;
    return Math.round((this.winDict.win / total) * 100);
  }

  private setChart() {

    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');

    this.data = {
      labels: ['Wins', 'Losses', 'Ties'],
      datasets: [
        {
          data: [this.winDict.win, this.winDict.loss, this.winDict.tie],
          backgroundColor: [
            documentStyle.getPropertyValue('--green-500'),
            documentStyle.getPropertyValue('--red-500'),
            documentStyle.getPropertyValue('--yellow-500')
          ],
          hoverBackgroundColor: [
            documentStyle.getPropertyValue('--green-400'),
            documentStyle.getPropertyValue('--red-400'),
            documentStyle.getPropertyValue('--yellow-400')
          ]
        }
      ]
    };


    this.options = {
      cutout: '60%',
      plugins: {
        legend: {
          labels: {
            color: textColor
          }
        }
      }
    };
  }
}
