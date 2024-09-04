import { Component, OnInit } from '@angular/core';
import { AvatarComponent } from "../../components/avatar/avatar.component";
import { HeaderComponent } from "../../components/header/header.component";
import { UserService } from "../../services/user/user.service";
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators, FormControl, AbstractControl, ValidationErrors} from '@angular/forms';
import { usernameValidator } from "../../validators/username.validator";
import { UsernameErrorComponent } from "../../components/sign-up/username-error/username-error.component";
import { ErrorMessageComponent } from "../../components/error-message/error-message.component";
import { Router } from '@angular/router';
import { AuthService } from "../../services/auth/auth.service";
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-account-page',
  standalone: true,
  imports: [
    AvatarComponent,
    HeaderComponent,
    ReactiveFormsModule,
    UsernameErrorComponent,
    ErrorMessageComponent,
  ],
  templateUrl: './account-page.component.html',
  styleUrl: './account-page.component.css'
})
export class AccountPageComponent implements OnInit {
  username: string = "";
  usernameForm!: FormGroup;
  deleteForm!: FormGroup;
  errorMessage: string = "";

  constructor(
    private userService: UserService,
    private router: Router,
    private authService: AuthService,
  ) {
    this.usernameForm = new FormGroup({
      username: new FormControl('', [Validators.required, Validators.minLength(3), Validators.maxLength(20), usernameValidator()]),
    });
    this.deleteForm = new FormGroup({
      delete: new FormControl('', [Validators.required, this.deleteValidator]),
    });
  }

  async ngOnInit(): Promise<void> {
    await this.userService.whenUserDataLoaded();
    this.username = this.userService.getUsername();
  }

  private deleteValidator(control: AbstractControl): ValidationErrors | null {
    return control.value === "delete" ? null : { deleteError: true };
  }

  public updateUsername() {
    this.errorMessage = "";
    if (this.usernameForm.valid) {
      const newUsername: string = this.usernameForm.get('username')?.value;
      this.userService.updateUsername(newUsername).subscribe({
        next: (response: any): void => {
          console.log(response);
          this.username = newUsername;
        },
        error: (error: HttpErrorResponse) => {
          console.error("Failed to update username: ", error);
          this.errorMessage = error.error?.error || "An unknown error occurred.";
        }
      });
    } else {
      this.updateUsernameError();
    }
  }

  private updateUsernameError() {
    const control = this.usernameForm.get('username');
    if (control)
      this.errorMessage = this.getUsernameErrorMessage(control);
  }

  public deleteAccount() {
    if (!this.deleteForm.valid)
      return;
    this.authService.deleteAccount().subscribe({
      next: (response: any): void => {
        console.log(response);
        this.router.navigate(['/sign-in']);
      },
      error: (error: Error) => {
        console.error("Failed to delete account: ", error);
      }
    });
  }

  hasUpdateFailed(): boolean {
    return this.errorMessage !== "";
  }

  private getUsernameErrorMessage(control: AbstractControl | null): string {
    const errorMessagesMap: { [key: string]: string } = {
      required: 'Username is required.',
      minlength: 'Username must be at least 3 characters long.',
      maxlength: 'Username cannot be more than 20 characters long.',
      invalidUsername: 'Username can only contain letters and @/./+/-/_.'
    };

    for (const errorType in control?.errors) {
      if (errorMessagesMap.hasOwnProperty(errorType)) {
        return errorMessagesMap[errorType];
      }
    }
    return '';
  }
}