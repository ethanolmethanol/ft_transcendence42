import { SignInComponent } from './sign-in.component';
import { FormBuilder } from '@angular/forms';
import {AuthService} from "../../services/auth/auth.service";
import {Router} from "@angular/router";
import {of, throwError} from "rxjs";

describe('SignInComponent', () => {
  let component: SignInComponent;
  let authServiceMock: jasmine.SpyObj<AuthService>;
  let routerMock: jasmine.SpyObj<Router>;
  let formBuilder: FormBuilder;

  beforeEach(() => {
    authServiceMock = jasmine.createSpyObj('AuthService', ['signIn']);
    routerMock = jasmine.createSpyObj('Router', ['navigate']);
    formBuilder = new FormBuilder();
    component = new SignInComponent(formBuilder, authServiceMock, routerMock);

    const mockSignInResponse = { detail: 'moke detail' };
    authServiceMock.signIn.and.returnValue(of(mockSignInResponse));
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize form with empty fields', () => {
    component.ngOnInit();
    expect(component.signInForm.value).toEqual({ login: '', password: '' });
  });

  it('should call onSubmit method', () => {
      spyOn(component, 'onSubmit');
      component.onSubmit();
      expect(component.onSubmit).toHaveBeenCalled();
    });

  it('should not submit if form is invalid', () => {
    component.ngOnInit();
    component.onSubmit();
    expect(authServiceMock.signIn).not.toHaveBeenCalled();
  });

  it('should set error message on authentication failure', () => {
    authServiceMock.signIn.and.returnValue(throwError({ status: 401 }));
    component.ngOnInit();
    component.signInForm.setValue({ login: 'test', password: 'test' });
    component.onSubmit();
    expect(component.errorMessage).toBe('Invalid username or password');
  });

  it('should navigate to home on successful authentication', () => {
    authServiceMock.signIn.and.returnValue(of( { detail: 'mock detail' }));
    component.ngOnInit();
    component.signInForm.setValue({ login: 'test', password: 'test' });
    component.onSubmit();
    expect(routerMock.navigate).toHaveBeenCalledWith(['home']);
  });
});
