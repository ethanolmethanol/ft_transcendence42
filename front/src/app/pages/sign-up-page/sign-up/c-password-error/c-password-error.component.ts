import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AbstractControl } from '@angular/forms';
import { StatusIconComponent } from "../../../../components/status-icon/status-icon.component";

interface ErrorMessagesMap {
  [key: string]: string;
}

@Component({
  selector: 'app-c-password-error',
  standalone: true,
  imports: [CommonModule,
    StatusIconComponent,
  ],
  templateUrl: './c-password-error.component.html',
  styleUrl: './c-password-error.component.css'
})
export class CPasswordErrorComponent {
  @Input() control: AbstractControl | null = null;
  @Input() isTouched: boolean = false;
  errorMessagesMap : ErrorMessagesMap = {
    required: 'Confirm Password is required.',
    matching: 'Passwords must match.',
  };
  allTestsPassed(): boolean {
    return !(this.control?.errors);
  }
  getErrorMessage(): string {
    for (let errorType in this.control?.errors) {
      if (this.errorMessagesMap.hasOwnProperty(errorType)) {
        return this.errorMessagesMap[errorType];
      }
    }
    return '';
  }
}
