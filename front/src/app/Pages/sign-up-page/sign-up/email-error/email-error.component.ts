import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AbstractControl } from '@angular/forms';

@Component({
  selector: 'app-email-error',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './email-error.component.html',
  styleUrl: './email-error.component.css'
})
export class EmailErrorComponent {
  @Input() control: AbstractControl | null = null;
}
