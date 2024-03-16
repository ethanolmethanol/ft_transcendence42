import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AbstractControl } from '@angular/forms';

@Component({
  selector: 'app-username-error',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './username-error.component.html',
  styleUrl: './username-error.component.css'
})
export class UsernameErrorComponent {
  @Input() control: AbstractControl | null = null;
}
