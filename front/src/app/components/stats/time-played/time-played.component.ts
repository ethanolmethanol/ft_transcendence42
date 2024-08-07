import {Component, Input, OnInit} from '@angular/core';
import {ChartModule} from "primeng/chart";
import {NgIf} from "@angular/common";
import {Times} from "../../../interfaces/user";
import {formatTimePlayed} from "../../../utils/time";

@Component({
  selector: 'app-time-played',
  standalone: true,
  templateUrl: './time-played.component.html',
  imports: [
    ChartModule,
    NgIf
  ],
  styleUrl: './time-played.component.css'
})
export class TimePlayedComponent implements OnInit {
  @Input() timePlayed!: Times;
  totalTimePlayed: string = '';
  data: any;
  options: any;

  ngOnInit() {
    this.setChart();
    this.totalTimePlayed = formatTimePlayed(this.timePlayed.total);
  }

  private setChart() {

    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');

    this.data = {
      labels: ['Local', 'Online'],
      datasets: [
        {
          data: [this.timePlayed.local, this.timePlayed.remote],
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
        },
        tooltip: {
          enabled: true,
          callbacks: {
            label: (context: { dataIndex: number }) => {
              const timePlayedKey = context.dataIndex === 0 ? 'local' : 'remote';
              return formatTimePlayed(this.timePlayed[timePlayedKey]);
            }
          }
        }
      }
    };
  }
}
