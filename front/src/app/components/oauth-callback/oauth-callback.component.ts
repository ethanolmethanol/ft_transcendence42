import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import { NgIf } from "@angular/common"
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';
import { UsernameErrorComponent } from "../sign-up/username-error/username-error.component";
import { ErrorMessageComponent } from "../error-message/error-message.component";
import { usernameValidator } from '../../validators/username.validator';

@Component({
  selector: 'app-oauth-callback',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgIf,
    ErrorMessageComponent,
    UsernameErrorComponent,
  ],
  templateUrl: './oauth-callback.component.html',
  styleUrl: './oauth-callback.component.css'
})
export class OauthCallbackComponent implements OnInit {
  pickUsernameForm!: FormGroup;
  errorMessage: string = "";
  userID: string = "";

  constructor(
    private _route: ActivatedRoute,
    private _authService: AuthService,
    private _router: Router,
    private _formBuilder: FormBuilder,
  ) {}
  ngOnInit(): void {
    this.pickUsernameForm = this._formBuilder.group({
      username: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(20), usernameValidator()]],
      updateOn: 'blur'
    });
    this._route.queryParams.subscribe(params => {
      const code = params["code"];
      if (code) {
        console.log("Code received: ", code);
        this._authService.exchangeCodeForUserID(code).subscribe({
          next: response => {
            this.userID = response;
          },
          error: (err): void => {
            console.error("Error exchanging code", err);
            this._router.navigate(["/sign-in"]);
          }
        });
      } else {
        console.error("No code received");
        this._router.navigate(["/sign-in"]);
      }
    });
  }

  onSubmit(): void {
    if (this.pickUsernameForm.valid) {
      const username = this.pickUsernameForm.value.username;
      console.log(username);
      this._authService.setUsername(username, this.userID).subscribe({
        next: (response) => {
          console.log("Account created: ", response);
          this._router.navigate(["/home"]);
        },
        error: (err): void => {
          console.error("Invalid username: ", err);
          this.errorMessage = err.message;
        }
      });
    }
  }

  hasUserCreationFailed(): boolean {
    return this.errorMessage !== "";
  }
}
