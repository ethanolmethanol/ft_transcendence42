import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ReactiveFormsModule, AsyncValidatorFn, ValidationErrors, AbstractControl } from '@angular/forms';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../services/auth.service';
import { Router, RouterLink} from "@angular/router";


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
  
  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router) {}

  ngOnInit() {
    this.signupForm = this.formBuilder.group({
      username: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(20)], this.usernameValidator()],
      email: ['', [Validators.required, Validators.email], [this.emailValidator()]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      c_password: ['', Validators.required]
    }, { validator: this.checkPasswords.bind(this) });
  }

  checkPasswords(group: FormGroup) {
    let pass = group.get('password')?.value;
    let confirmPass = group.get('c_password')?.value;

    return pass === confirmPass ? null : { notSame: true }
  }

  private usernameValidator(): AsyncValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      return this.authService.checkUsernameAvailability(control.value).pipe(
        map(isAvailable => (isAvailable ? null : { usernameTaken: true }))
      );
    };
  }

  private emailValidator(): AsyncValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      return this.authService.checkEmailAvailability(control.value).pipe(map(isAvailable => (isAvailable ? null : { emailTaken: true }))
      );
    };
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
        }
      )
    }
  }
}
