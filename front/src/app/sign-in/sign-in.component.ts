import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-sign-in',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgIf
  ],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})

export class SignInComponent implements OnInit {
  signInForm!: FormGroup;

  constructor(private formBuilder: FormBuilder) { }

  ngOnInit(): void {
    this.signInForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]]
    });
  }

  onSubmit(): void {
    if (this.signInForm.valid) {
      console.log("Valid authentication : " + JSON.stringify(this.signInForm.value));
    }
  }
}
