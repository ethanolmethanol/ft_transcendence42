import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ReactiveFormsModule} from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth/auth.service';
import { Router, RouterLink} from "@angular/router";
import { CPasswordErrorComponent } from "./c-password-error/c-password-error.component";
import { PasswordErrorComponent } from "./password-error/password-error.component";
import { EmailErrorComponent } from "./email-error/email-error.component";
import { UsernameErrorComponent } from "./username-error/username-error.component";
import { ErrorMessageComponent } from "../error-message/error-message.component";
import { usernameValidator } from '../../validators/username.validator';
import { emailValidator } from '../../validators/email.validator';
import { matchValidator } from '../../validators/match.validator';

@Component({
  selector: 'app-sign-up',
  standalone: true,
  imports: [CommonModule,
    ReactiveFormsModule,
    RouterLink,
    CPasswordErrorComponent,
    PasswordErrorComponent,
    EmailErrorComponent,
    UsernameErrorComponent,
    ErrorMessageComponent,
  ],
  templateUrl: './sign-up.component.html',
  styleUrl: './sign-up.component.css'
})
export class SignUpComponent implements OnInit {
  signupForm!: FormGroup;
  errorMessage: string = "";

  constructor(
    private _formBuilder: FormBuilder,
    private _authService: AuthService,
    private _router: Router) {}

  ngOnInit() {
    this.signupForm = this._formBuilder.group({
      username: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(20), usernameValidator()]],
      email: ['', [Validators.required, Validators.email, emailValidator()]],
      password: ['', [Validators.required, Validators.minLength(8), matchValidator('c_password', true)]],
      c_password: ['', [Validators.required, matchValidator('password')]],
      updateOn: 'blur'
    });
  }

  onSubmit() {
    console.log('Form Value at Submission:', this.signupForm.value);
    if (this.signupForm.valid) {
      this.signUp();
    }
  }

  private signUp() {
    const { username, email, password } = this.signupForm.value;

    this._authService.signUp(username, email, password).subscribe({
      next: (response) => {
        console.log("Account created: ", response);
        this.signIn();
      },
      error: (error) => this.handleSignUpError(error)
    });
  }

  private signIn() {
    this._router.navigate(['/sign-in']);
  }

  private handleSignUpError(signUpError: any) {
    console.error("Account creation failed: ", signUpError);
    this.errorMessage = "An error occurred. Please try again.";
    this.extractErrorMessage(signUpError);
  }

  private extractErrorMessage(signUpError: any) {
    if (signUpError && signUpError.error) {
      const errors = signUpError.error;
      for (const key in errors) {
        if (Object.hasOwnProperty.call(errors, key) && errors[key].length > 0) {
          this.errorMessage = errors[key][0];
          break; // Use the first error message found
        }
      }
    }
  }

  hasUserCreationFailed(): boolean {
    return this.errorMessage !== "";
  }
}
