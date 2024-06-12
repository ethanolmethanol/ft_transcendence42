import { Component, Input, Output, OnChanges, SimpleChanges, Renderer2, ElementRef, EventEmitter } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-slider',
  standalone: true,
  imports: [NgFor],
  templateUrl: './slider.component.html',
  styleUrl: './slider.component.css'
})
export class SliderComponent implements OnChanges {
  @Input() options: (string)[] = [];
  @Input() optionIndex: number = 0;
  @Output() selectedOption: EventEmitter<number> = new EventEmitter<number>();
  @Output() optionIndexChange: EventEmitter<number> = new EventEmitter<number>();
  min: number = 0;
  max: number = 0;
  value: string = '';

  constructor(private renderer: Renderer2, private el: ElementRef) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.options && this.options) {
      this.max = this.options.length - 1;
      this.value = this.options[this.optionIndex];
      console.log("New slider: ", this.options, " with default value: ", this.options[this.optionIndex]);
    }
    if (changes.optionIndex) {
      this.value = this.options[this.optionIndex];
      console.log("New value: ", this.options[this.optionIndex]);
    }
  }

  onInput(event: any): void {
    this.optionIndex = Number(event.target.value);
    this.selectedOption.emit(this.optionIndex);
    this.optionIndexChange.emit(this.optionIndex);
    console.log("valIndex: ", this.optionIndex, " | val: ", this.options[this.optionIndex]);
  }

  onMouseMove(event: MouseEvent): void {
    const sliderRect = this.el.nativeElement.getBoundingClientRect();
    const cursorPos = event.clientX - sliderRect.left;

    this.options.forEach((option, index) => {
      const optionEl = this.el.nativeElement.querySelector(`option:nth-child(${index + 1})`);
      const optionRect = optionEl.getBoundingClientRect();
      const optionPos = optionRect.left - sliderRect.left;
  
      if (cursorPos >= optionPos && cursorPos <= optionPos + optionRect.width) {
        this.renderer.setStyle(optionEl, 'color', '#e5f25a');  // Yellow when the cursor is over the option
      } else {
        this.renderer.setStyle(optionEl, 'color', 'white');  // White when the cursor is not over the option
      }
    });
  }
}
