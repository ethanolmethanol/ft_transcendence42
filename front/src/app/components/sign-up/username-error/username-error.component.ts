import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AbstractControl } from '@angular/forms';
import { StatusIconComponent } from "../../status-icon/status-icon.component";

interface ErrorMessagesMap {
  [key: string]: string;
}

@Component({
  selector: 'app-username-error',
  standalone: true,
  imports: [CommonModule,
    StatusIconComponent,
  ],
  templateUrl: './username-error.component.html',
  styleUrl: './username-error.component.css'
})
export class UsernameErrorComponent {
  @Input() control: AbstractControl | null = null;
  @Input() isTouched: boolean = false;
  errorMessagesMap : ErrorMessagesMap = {
    required: 'Username is required.',
    minlength: 'Username must be at least 3 characters long.',
    maxlength: 'Username cannot be more than 20 characters long.',
    invalidUsername: 'Username can only contain letters and @/./+/-/_.'
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
