import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-copy-button',
  standalone: true,
  imports: [],
  templateUrl: './copy-button.component.html',
  styleUrls: ['./copy-button.component.css']
})
export class CopyButtonComponent implements AfterViewInit {

  @ViewChild('defaultMessage') defaultMessage!: ElementRef;
  @ViewChild('successMessage') successMessage!: ElementRef;
  @ViewChild('contentToCopy') contentToCopy!: ElementRef;

  ngAfterViewInit() {
    // No need for FlowbiteInstances here
  }

  showSuccess() {
    this.defaultMessage.nativeElement.classList.add('hidden');
    this.successMessage.nativeElement.classList.remove('hidden');
  }

  resetToDefault() {
    this.defaultMessage.nativeElement.classList.remove('hidden');
    this.successMessage.nativeElement.classList.add('hidden');
  }

  copyToClipboard() {
    const textToCopy = this.contentToCopy.nativeElement.innerText;
    navigator.clipboard.writeText(textToCopy).then(() => {
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
