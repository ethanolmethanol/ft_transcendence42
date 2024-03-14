import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import {Router, RouterLink} from "@angular/router";


@Component({
  selector: 'app-sign-up',
  standalone: true,
  imports: [CommonModule,
    ReactiveFormsModule,
    RouterLink,
  ],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.css'
})
export class SignUpComponent implements OnInit {
  signupForm!: FormGroup;
  
  constructor(private formBuilder: FormBuilder) {}

  ngOnInit() {
    this.signupForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(20)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      c_password: ['', Validators.required]
    }, { validator: this.checkPasswords.bind(this) });
  }

  checkPasswords(group: FormGroup) {
    let pass = group.get('password')?.value;
    let confirmPass = group.get('c_password')?.value;

    return pass === confirmPass ? null : { notSame: true }
  }

  onSubmit() {
    if (this.signupForm.valid) {
      console.log('Form Data: ', this.signupForm.value);
      // Here you can handle your form submission further, e.g., sending it to a server
    } else {
      console.log('Form is not valid.');
      this.signupForm.markAllAsTouched(); // Helps to trigger validation messages on submit
    }
  }
}
