import { Component, Output, EventEmitter } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-color-wheel',
  standalone: true,
  imports: [NgFor],
  templateUrl: './color-wheel.component.html',
  styleUrl: './color-wheel.component.css'
})
export class ColorWheelComponent {
  @Output() colorSelected = new EventEmitter<string>();

  colors: string[] = this.generateColorArray(120);

  generateColorArray(n: number): string[] {
    let colors: string[] = [];
    for(let i = 0; i < n; i++) {
      let hue = Math.floor(360 * i / n);
      colors.push(`hsl(${hue}, 100%, 50%)`);
    }
    return colors;
  }

  selectColor(color: string) {
    this.colorSelected.emit(color);
  }

  getTransform(index: number): string {
    const angle = index * (360 / this.colors.length);
    return `rotate(${angle}deg) translate(100px) rotate(-${angle}deg)`;
  }
}
