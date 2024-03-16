import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AbstractControl } from '@angular/forms';

@Component({
  selector: 'app-password-error',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './password-error.component.html',
  styleUrl: './password-error.component.css'
})
export class PasswordErrorComponent {
  @Input() control: AbstractControl | null = null;
}
