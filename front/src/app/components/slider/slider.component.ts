import { Component, Input, OnChanges, SimpleChanges, Renderer2, ElementRef } from '@angular/core';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-slider',
  standalone: true,
  imports: [NgFor],
  templateUrl: './slider.component.html',
  styleUrl: './slider.component.css'
})
export class SliderComponent implements OnChanges {
  @Input() options: (string | number)[] = [];
  max = 0;
  min = 0;
  val = 0;

  constructor(private renderer: Renderer2, private el: ElementRef) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.options && this.options) {
      console.log(this.options);
      this.max = this.options.length - 1;
    }
  }

  onInput(event: any): void {
    this.val = event.target.value;
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






  
// export class SliderComponent implements OnChanges {
//   @Input() options: (string | number)[] = [];
//   max = 0;
//   min = 0;
//   val = 0;
//   selectedOption: number | string = null;  // New property to keep track of the selected option

//   constructor(private renderer: Renderer2, private el: ElementRef) {}

//   ngOnChanges(changes: SimpleChanges): void {
//     if (changes.options && this.options) {
//       this.max = this.options.length - 1;
//     }
//   }

//   onInput(event: any): void {
//     this.val = event.target.value;
//     this.selectedOption = this.options[this.val];  // Update the selected option when the slider value changes
//   }
  
//   onMouseMove(event: MouseEvent): void {
//     const sliderRect = this.el.nativeElement.getBoundingClientRect();
//     const cursorPos = event.clientX - sliderRect.left;
  
//     this.options.forEach((option, index) => {
//       const optionEl = this.el.nativeElement.querySelector(`option:nth-child(${index + 1})`);
//       const optionRect = optionEl.getBoundingClientRect();
//       const optionPos = optionRect.left - sliderRect.left;
  
//       if (cursorPos >= optionPos && cursorPos <= optionPos + optionRect.width) {
//         this.renderer.setStyle(optionEl, 'color', option === this.selectedOption ? 'white' : '#e5f25a');  // Yellow when the cursor is over the option, unless it's the selected option
//         this.renderer.setStyle(optionEl, 'font-weight', option === this.selectedOption ? 'bold' : 'normal');  // Bold when the cursor is over the option, unless it's the selected option
//       } else {
//         this.renderer.setStyle(optionEl, 'color', option === this.selectedOption ? 'white' : 'grey');  // Grey when the cursor is not over the option, unless it's the selected option
//         this.renderer.setStyle(optionEl, 'font-weight', option === this.selectedOption ? 'bold' : 'normal');  // Normal when the cursor is not over the option, unless it's the selected option
//       }
//     });
//   }
// }