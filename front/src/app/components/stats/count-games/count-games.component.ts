import {Component, Input, OnInit} from '@angular/core';
import {GameCounter} from "../../../interfaces/user";
import {ChartModule} from "primeng/chart";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-count-games',
  standalone: true,
  imports: [
    ChartModule,
    NgIf
  ],
  templateUrl: './count-games.component.html',
  styleUrl: './count-games.component.css'
})
export class CountGamesComponent implements OnInit {
  @Input() gameCounter!: GameCounter;
  totalCount: number = 0;

  data: any;
  options: any;

  ngOnInit() {
    this.setChart();
    this.totalCount = this.gameCounter.total;
  }

  private setChart() {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');

    this.data = {
      labels: ['Local', 'Online'],
      datasets: [
        {
          data: [this.gameCounter.local, this.gameCounter.remote],
          backgroundColor: [
            documentStyle.getPropertyValue('--blue-500'),
            documentStyle.getPropertyValue('--yellow-500')
          ],
          hoverBackgroundColor: [
            documentStyle.getPropertyValue('--blue-400'),
            documentStyle.getPropertyValue('--yellow-400')
          ]
        }
      ]
    };

    this.options = {
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
