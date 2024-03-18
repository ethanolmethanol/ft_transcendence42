import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AbstractControl } from '@angular/forms';
import {TestStatusIconComponent} from "../../../../components/test-status-icon/test-status-icon.component";

interface ErrorMessagesMap {
  [key: string]: string;
}

@Component({
  selector: 'app-username-error',
  standalone: true,
  imports: [CommonModule, TestStatusIconComponent],
  templateUrl: './username-error.component.html',
  styleUrl: './username-error.component.css'
})
export class UsernameErrorComponent {
  @Input() control: AbstractControl | null = null;
  errorMessagesMap : ErrorMessagesMap = {
    required: 'Username is required',
    minlength: 'Username must be at least 3 characters long.',
    maxlength: 'Username cannot be more than 20 characters long.'
  };

  allTestsPassed(): boolean {
    // Add all your test conditions here
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
