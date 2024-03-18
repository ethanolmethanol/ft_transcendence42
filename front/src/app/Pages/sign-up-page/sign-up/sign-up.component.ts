import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ReactiveFormsModule, AsyncValidatorFn, ValidationErrors, AbstractControl } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../services/auth.service';
import { Router, RouterLink} from "@angular/router";
import { CPasswordErrorComponent } from "./c-password-error/c-password-error.component";
import { PasswordErrorComponent } from "./password-error/password-error.component";
import { EmailErrorComponent } from "./email-error/email-error.component";
import { UsernameErrorComponent } from "./username-error/username-error.component";
import { ErrorMessageComponent } from "../../../components/error-message/error-message.component";

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
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router) {}

  ngOnInit() {
    this.signupForm = this.formBuilder.group({
      username: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(20)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      c_password: ['', Validators.required],
      updateOn: 'blur'
    }, { validator: this.checkPasswords.bind(this) });
    this.signupForm.valueChanges.subscribe(() => {
      if (this.signupForm.errors?.notSame) {
        this.signupForm.controls.c_password.setErrors({ notSame: true });
      } else {
        // If there are no errors or if the notSame error has been resolved, clear the error.
        if (this.signupForm.controls.c_password.errors?.notSame) {
          let errors = {...this.signupForm.controls.c_password.errors};
          delete errors.notSame;
          if (Object.keys(errors).length > 0) {
            this.signupForm.controls.c_password.setErrors(errors);
          } else {
            this.signupForm.controls.c_password.setErrors(null);
          }
        }
      }
    });
  }

  checkPasswords(group: FormGroup) {
    let pass = group.get('password')?.value;
    let confirmPass = group.get('c_password')?.value;

    return pass === confirmPass ? null : { notSame: true }
  }

  onSubmit() {
    console.log('Form Value at Submission:', this.signupForm.value);
    if (this.signupForm.valid) {
      const {username, email, password} = this.signupForm.value;
      this.authService.signUp(username, email, password).subscribe(
        response => {
          console.log("Accout created: ", response);
          this.router.navigate(['sign-in']).then(r => console.log("Navigated to sign-in-page"));
        },
        error => {
          console.error("Account creation failed: ", error);
          this.errorMessage = error.error.username[0] || error.error.email[0] || 'An error occured.';
        }
      )
    }
  }

  hasUserCreationFailed(): boolean {
    return this.errorMessage !== "";
  }
}
