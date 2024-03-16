import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AbstractControl } from '@angular/forms';

@Component({
  selector: 'app-c-password-error',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './c-password-error.component.html',
  styleUrl: './c-password-error.component.css'
})
export class CPasswordErrorComponent {
  @Input() control: AbstractControl | null = null;
}
