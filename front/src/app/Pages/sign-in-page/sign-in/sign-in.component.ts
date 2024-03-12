import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {NgIf} from "@angular/common";
import {Router, RouterLink} from "@angular/router";
import { AuthService } from '../../../services/auth.service';
import {ErrorMessageComponent} from "../../../components/error-message/error-message.component";

@Component({
  selector: 'app-sign-in',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgIf,
    RouterLink,
    ErrorMessageComponent,
  ],
  templateUrl: './sign-in.component.html',
  styleUrl: './sign-in.component.css'
})

export class SignInComponent implements OnInit {
  signInForm!: FormGroup;
  errorMessage: string = "";
  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router) {}

  ngOnInit(): void {
    this.signInForm = this.formBuilder.group({
      login: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }

  onSubmit(): void {
    if (this.signInForm.valid) {
      const {login, password} = this.signInForm.value;
      this.authService.signIn(login, password).subscribe(
        response => {
          console.log("Valid authentication : ", response);
          this.router.navigate(['home']).then(r => console.log("Navigated to home"));
        },
        error => {
          console.error("Authentication failed: ", error);
          // Assuming the backend sends back an error object with a message property
          if (error.status === 401) {
            this.errorMessage = "Invalid username or password";
          } else {
            this.errorMessage = "An error occurred while authenticating";
          }
        }
      );
    }
  }

  hasAuthenticationFailed(): boolean {
    return this.errorMessage !== "";
  }
}
