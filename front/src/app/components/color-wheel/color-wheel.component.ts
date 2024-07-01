import { Component, Output, Input, EventEmitter, HostBinding } from '@angular/core';
import { NgFor } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-color-wheel',
  standalone: true,
  imports: [
    NgFor,
    FormsModule,
  ],
  templateUrl: './color-wheel.component.html',
  styleUrl: './color-wheel.component.css'
})
export class ColorWheelComponent {
  @Input() previewColor: string = '';
  @Output() colorSelected = new EventEmitter<string>();
  @HostBinding('style.--brightness') brightness = 50;

  colors: string[] = this.generateColorArray(15);
  selectedBrightness: number = 50;

  generateColorArray(n: number): string[] {
    let colors: string[] = [];
    for(let i = 0; i < n; i++) {
      let hue = Math.floor(360 * i / n);
      colors.push(`hsl(${hue}, 100%, 50%)`);
    }
    return colors;
  }

  selectColor(color: string) {
    this.previewColor = this.adjustBrightness(color);
    this.colorSelected.emit(this.previewColor);
  }

  getTransform(index: number): string {
    const angle = index * (360 / this.colors.length);
    return `rotate(${angle}deg) translate(100px) rotate(-${angle}deg)`;
  }

  getGradient(i: number) {
    const nextIndex = (i + 1) % this.colors.length;
    const color = this.colors[i];
    const nextColor = this.colors[nextIndex];
    return `linear-gradient(${nextColor}, ${color})`;
  }

  parseHsl(hsl: string): [number, number, number] {
    const match = hsl.match(/hsl\((\d+),\s*(\d+)%,\s*(\d+)%\)/);
    if (!match) {
      throw new Error('Invalid HSL color');
    }
    return [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];
  }

  adjustBrightness(hslColor: string): string {
    try {
      const hsl = this.parseHsl(hslColor);
      hsl[2] = this.selectedBrightness;
      return `hsl(${hsl[0]}, ${hsl[1]}%, ${hsl[2]}%)`;
    } catch (e) {
      return hslColor;
    }
  }
}
