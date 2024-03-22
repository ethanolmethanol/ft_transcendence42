import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AbstractControl } from '@angular/forms';
import { StatusIconComponent } from "../../../../components/status-icon/status-icon.component";

interface ErrorMessagesMap {
  [key: string]: string;
}

@Component({
  selector: 'app-email-error',
  standalone: true,
  imports: [CommonModule,
    StatusIconComponent,
  ],
  templateUrl: './email-error.component.html',
  styleUrl: './email-error.component.css'
})
export class EmailErrorComponent {
  @Input() control: AbstractControl | null = null;
  @Input() isTouched: boolean = false;
  errorMessagesMap : ErrorMessagesMap = {
    required: 'Email is required.',
    email: 'Email is not valid.',
    invalidEmail: 'Email is not valid.'
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
