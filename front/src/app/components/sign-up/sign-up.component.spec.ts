import { SignUpComponent } from './sign-up.component';
import {AuthService} from "../../services/auth/auth.service";
import {FormBuilder} from "@angular/forms";
import {Router} from "@angular/router";

describe('SignUpComponent', () => {
  let component: SignUpComponent;
  let formBuilder: FormBuilder;
  let authService: AuthService;
  let router: Router;



  beforeEach(async () => {
    component = new SignUpComponent(formBuilder, authService, router);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
