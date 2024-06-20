import {Component, ElementRef, ViewChild, AfterViewInit, input, Input} from '@angular/core';
import {NgClass} from "@angular/common";

@Component({
  selector: 'app-copy-button',
  standalone: true,
  imports: [
    NgClass
  ],
  templateUrl: './copy-button.component.html',
  styleUrls: ['./copy-button.component.css']
})
export class CopyButtonComponent implements AfterViewInit {

  isActivated = false;
  @ViewChild('defaultMessage') defaultMessage!: ElementRef;
  @ViewChild('successMessage') successMessage!: ElementRef;
  @Input () textToCopy: string = '';

  ngAfterViewInit() {
    // No need for FlowbiteInstances here
  }

  showSuccess() {
    this.isActivated = true;
    this.defaultMessage.nativeElement.classList.add('hidden');
    this.successMessage.nativeElement.classList.remove('hidden');
  }

  resetToDefault() {
    this.isActivated = false;
    this.defaultMessage.nativeElement.classList.remove('hidden');
    this.successMessage.nativeElement.classList.add('hidden');
  }

  copyToClipboard() {
    navigator.clipboard.writeText(this.textToCopy).then(() => {
      this.showSuccess();

      // reset to default state
      setTimeout(() => {
        this.resetToDefault();
      }, 2000);
    }).catch(err => {
      console.error('Could not copy text: ', err);
    });
  }
}
