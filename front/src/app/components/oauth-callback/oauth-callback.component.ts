import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import { CommonModule, NgStyle } from "@angular/common"
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';
import { UsernameErrorComponent } from "../sign-up/username-error/username-error.component";
import { ErrorMessageComponent } from "../error-message/error-message.component";
import { usernameValidator } from '../../validators/username.validator';

@Component({
  selector: 'app-oauth-callback',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgStyle,
    CommonModule,
    ErrorMessageComponent,
    UsernameErrorComponent,
    RouterLink,
  ],
  templateUrl: './oauth-callback.component.html',
  styleUrl: './oauth-callback.component.css'
})
export class OauthCallbackComponent implements OnInit {
  pickUsernameForm: FormGroup;
  errorMessage: string = "";
  userID: number = 0;
  displayForm: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private authService: AuthService,
    private router: Router,
    private formBuilder: FormBuilder
  ) {
    this.pickUsernameForm = this.createForm();
  }

  ngOnInit(): void {
    this.handleOAuthCallback();
  }

  private createForm(): FormGroup {
    return this.formBuilder.group({
      username: ['', [
        Validators.required,
        Validators.minLength(3),
        Validators.maxLength(20),
        usernameValidator()
      ]],
      updateOn: 'blur'
    });
  }

  private handleOAuthCallback(): void {
    this.route.queryParams.subscribe(params => {
      const code = params["code"];
      if (code) {
        this.exchangeCodeForUserId(code);
      } else {
        this.redirectToSignInWithError("No code received");
      }
    });
  }

  private exchangeCodeForUserId(code: string): void {
    this.authService.exchangeCodeForUserID(code).subscribe({
      next: response => this.handleCodeExchangeResponse(response),
      error: err => this.redirectToSignInWithError("Error exchanging code")
    });
  }

  private handleCodeExchangeResponse(response: any): void {
    if (response.new_user_created) {
      this.userID = response.user_id;
      this.displayForm = true;
    } else {
      this.router.navigate(["/home"]);
    }
  }

  private redirectToSignInWithError(message: string): void {
    console.error(message);
    this.router.navigate(["/sign-in"]);
  }

  public onSubmit(): void {
    if (this.pickUsernameForm.valid) {
      const username = this.pickUsernameForm.value.username;
      this.setUsername(username);
    }
  }

  private setUsername(username: string): void {
    this.authService.setUsername42(username, this.userID).subscribe({
      next: response => this.handleUsernameSetResponse(response),
      error: err => this.handleUsernameSetError(err)
    });
  }

  private handleUsernameSetResponse(response: any): void {
    console.log("Account created: ", response);
    this.router.navigate(["/home"]);
  }

  private handleUsernameSetError(err: any): void {
    console.error("Invalid username: ", err);
    this.errorMessage = err.message;
  }

  public hasUserCreationFailed(): boolean {
    return this.errorMessage !== "";
  }
}
