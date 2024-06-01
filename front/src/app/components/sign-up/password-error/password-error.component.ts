import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AbstractControl } from '@angular/forms';
import { StatusIconComponent } from "../../status-icon/status-icon.component";

interface ErrorMessagesMap {
  [key: string]: string;
}

@Component({
  selector: 'app-password-error',
  standalone: true,
  imports: [CommonModule,
    StatusIconComponent,
  ],
  templateUrl: './password-error.component.html',
  styleUrl: './password-error.component.css'
})
export class PasswordErrorComponent {
  @Input() control: AbstractControl | null = null;
  @Input() isTouched: boolean = false;
  errorMessageMap : ErrorMessagesMap = {
    required: 'Password is required.',
    minlength: 'Password must be at least 8 characters long.',
  };
  allTestsPassed(): boolean {
    return !(this.control?.errors);
  }
  getErrorMessage(): string {
    for (let errorType in this.control?.errors) {
      if (this.errorMessageMap.hasOwnProperty(errorType)) {
        return this.errorMessageMap[errorType];
      }
    }
    return '';
  }
}
