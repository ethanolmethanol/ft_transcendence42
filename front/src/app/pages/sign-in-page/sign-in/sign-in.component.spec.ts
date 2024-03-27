import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SignInComponent } from './sign-in.component';
import {FormBuilder} from "@angular/forms";
import {AuthService} from "../../../services/auth/auth.service";
import {Router} from "@angular/router";

describe('SignInComponent', () => {
  let component: SignInComponent;
  let formBuilder: FormBuilder;
  let authService: AuthService;
  let router: Router;

  beforeEach(async () => {
    component = new SignInComponent(formBuilder, authService, router);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
